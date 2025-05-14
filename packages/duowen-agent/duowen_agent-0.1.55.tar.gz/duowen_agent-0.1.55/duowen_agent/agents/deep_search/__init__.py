import logging
import re
from typing import Callable, Optional, Any, Literal

from pydantic import BaseModel, Field

from duowen_agent.llm import OpenAIChat
from .prompts import (
    BEGIN_SEARCH_QUERY,
    BEGIN_SEARCH_RESULT,
    END_SEARCH_RESULT,
    END_SEARCH_QUERY,
    REASON_PROMPT,
    RELEVANT_EXTRACTION_PROMPT,
    SELF_LLM_ANSWER,
)
from ...llm.utils import format_messages
from ...tools.entity import ToolSearchResult
from ...utils.core_utils import remove_think, generate_unique_id


def extract_between(text: str, start_tag: str, end_tag: str) -> list[str]:
    pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    return re.findall(pattern, text, flags=re.DOTALL)


# def extract_think_result(content: str):
#     pattern = r"<think_result>(.*?)</think_result>"
#     match = re.search(pattern, content, flags=re.DOTALL)
#     return match.group(1).strip() if match else None


class DeepSearchThink(BaseModel):
    content: str
    cell_id: str


class DeepSearchAction(BaseModel):
    content: str
    cell_id: str
    sub_cell_id: Optional[str] = None


class DeepSearchObservation(BaseModel):
    result: str
    view: Optional[Any] = None
    ask_type: Literal["llm", "retrieval", "preset"] = Field(
        "retrieval",
        description="llm:模型回答 retrieval:检索回答 preset:系统预设回答",
    )
    cell_id: str
    sub_cell_id: Optional[str] = None


class DeepSearch:
    def __init__(
        self,
        llm_plann_instance: OpenAIChat,
        retrieval: Callable[[str], ToolSearchResult],
        max_search_limit: int = 15,
        llm_answer_instance: OpenAIChat = None,
        self_qa_llm_instance: OpenAIChat = None,
    ):
        self.llm_plann_instance = llm_plann_instance
        self.llm_answer_instance = llm_answer_instance or llm_plann_instance
        self.retrieval = retrieval
        self.max_search_limit = max_search_limit
        self.self_qa_llm_instance = self_qa_llm_instance

    def run(self, question: str):

        def rm_query_tags(line):
            pattern = (
                re.escape(BEGIN_SEARCH_QUERY) + r"(.*?)" + re.escape(END_SEARCH_QUERY)
            )
            return re.sub(pattern, "", line, 1)

        def rm_result_tags(line):
            pattern = (
                re.escape(BEGIN_SEARCH_RESULT) + r"(.*?)" + re.escape(END_SEARCH_RESULT)
            )
            return re.sub(pattern, "", line, count=1)

        executed_search_queries = []
        msg_history = [{"role": "user", "content": f'Question:"{question}"\n'}]
        all_reasoning_steps = []

        for ii in range(self.max_search_limit + 1):
            cell_id = generate_unique_id("deepsearch")
            if ii == self.max_search_limit - 1:
                summary_think = f"\n{BEGIN_SEARCH_RESULT}\n当前操作已触发搜索次数上限，系统禁止继续执行搜索请求。\n{END_SEARCH_RESULT}\n"
                yield DeepSearchObservation(
                    result="当前操作已触发搜索次数上限，系统禁止继续执行搜索请求。",
                    ask_type="preset",
                    cell_id=cell_id,
                )
                all_reasoning_steps.append(summary_think)
                msg_history.append({"role": "assistant", "content": summary_think})
                break

            if msg_history[-1]["role"] != "user":
                msg_history.append(
                    {
                        "role": "user",
                        "content": "基于新信息持续执行推理链路。\n",
                    }
                )
            else:
                msg_history[-1]["content"] += "\n\n基于新信息持续执行推理链路。\n"

            query_think = ""
            _prompt = format_messages(
                [
                    {
                        "role": "system",
                        "content": REASON_PROMPT.replace(
                            "{{MAX_SEARCH_LIMIT}}", str(self.max_search_limit)
                        ),
                    }
                ]
                + msg_history
            )
            logging.debug(_prompt.get_format_messages())

            ans = self.llm_plann_instance.chat(_prompt)

            ans = remove_think(ans)

            if not ans:
                continue

            query_think += ans

            yield DeepSearchThink(content=rm_query_tags(query_think), cell_id=cell_id)

            queries = extract_between(query_think, BEGIN_SEARCH_QUERY, END_SEARCH_QUERY)
            if not queries:
                if ii > 0:
                    break
                queries = [question]

            all_reasoning_steps.append(query_think)

            for search_query in queries:
                sub_cell_id = generate_unique_id("deepsearch")
                yield DeepSearchAction(
                    content=f"{search_query}\n",
                    cell_id=cell_id,
                    sub_cell_id=sub_cell_id,
                )
                msg_history.append(
                    {
                        "role": "assistant",
                        "content": f"\n\n{BEGIN_SEARCH_QUERY}{search_query}{END_SEARCH_QUERY}\n\n",
                    }
                )

                if search_query in executed_search_queries:
                    yield DeepSearchObservation(
                        result="检测到重复查询请求，直接调用历史搜索结果。",
                        ask_type="preset",
                        cell_id=cell_id,
                        sub_cell_id=sub_cell_id,
                    )
                    summary_think = f"\n{BEGIN_SEARCH_RESULT}\n检测到重复查询请求，请直接调用历史搜索结果。\n{END_SEARCH_RESULT}\n"
                    all_reasoning_steps.append(summary_think)
                    msg_history.append({"role": "user", "content": summary_think})

                    continue

                truncated_prev_reasoning = ""
                for i, step in enumerate(all_reasoning_steps):
                    truncated_prev_reasoning += f"Step {i + 1}: {step}\n\n"

                prev_steps = truncated_prev_reasoning.split("\n\n")
                if len(prev_steps) <= 5:
                    truncated_prev_reasoning = "\n\n".join(prev_steps)
                else:
                    truncated_prev_reasoning = ""
                    for i, step in enumerate(prev_steps):
                        if (
                            i == 0
                            or i >= len(prev_steps) - 4
                            or BEGIN_SEARCH_QUERY in step
                            or BEGIN_SEARCH_RESULT in step
                        ):
                            truncated_prev_reasoning += step + "\n\n"
                        else:
                            if (
                                truncated_prev_reasoning[-len("\n\n...\n\n") :]
                                != "\n\n...\n\n"
                            ):
                                truncated_prev_reasoning += "...\n\n"
                truncated_prev_reasoning = truncated_prev_reasoning.strip("\n")

                _doc = self.retrieval(search_query)

                _prompt = format_messages(
                    [
                        {
                            "role": "system",
                            "content": RELEVANT_EXTRACTION_PROMPT.format(
                                prev_reasoning=truncated_prev_reasoning,
                                search_query=search_query,
                                document=_doc.content_with_weight,
                            ),
                        },
                        {
                            "role": "user",
                            "content": f'请基于当前搜索词"{search_query}"并结合已有推理步骤，逐一分析网页内容并提取有效信息。',
                        },
                    ]
                )

                logging.debug(_prompt.get_format_messages())

                if not _doc.result:
                    if self.self_qa_llm_instance:
                        ans = self.self_qa_llm_instance.chat(
                            format_messages(
                                [
                                    {"role": "system", "content": SELF_LLM_ANSWER},
                                    {
                                        "role": "user",
                                        "content": f"问题: {search_query}",
                                    },
                                ]
                            )
                        )

                        yield DeepSearchObservation(
                            result=remove_think(ans),
                            ask_type="llm",
                            cell_id=cell_id,
                            sub_cell_id=sub_cell_id,
                        )
                        ans = "大语言模型回答:\n\n" + remove_think(ans)
                    else:

                        yield DeepSearchObservation(
                            result="未检索到有效信息",
                            ask_type="preset",
                            cell_id=cell_id,
                            sub_cell_id=sub_cell_id,
                        )
                        ans = "未检索到有效信息"
                else:
                    ans = self.llm_answer_instance.chat(_prompt)
                    ans = remove_think(ans)
                    yield DeepSearchObservation(
                        result=ans,
                        view=_doc,
                        ask_type="retrieval",
                        cell_id=cell_id,
                        sub_cell_id=sub_cell_id,
                    )

                summary_think = ""

                if not ans:
                    continue

                summary_think += ans

                all_reasoning_steps.append(summary_think)
                msg_history.append(
                    {
                        "role": "user",
                        "content": f"\n\n{BEGIN_SEARCH_RESULT}{summary_think}{END_SEARCH_RESULT}\n\n",
                    }
                )
