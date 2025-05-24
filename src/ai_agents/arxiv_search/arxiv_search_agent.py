from typing import Any

from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper
from agents.tool import FunctionTool
from ai_agents.context import AgentContext
from src.core.prompt_manager import get_prompt
from ai_agents.arxiv_search.tools.search import search_papers


class ArxivSearchAgent(Agent[AgentContext]):
    # TODO: ツールの型をAny以外にしたい
    def __init__(
        self,
        model: OpenAIChatCompletionsModel,
        name: str = "arxiv_search_agent",
        tools: list[FunctionTool] = [search_papers],
    ):
        super().__init__(name, model)
        self.name = name
        self.model = model
        self.instructions = self._set_prompt

    @staticmethod
    def _set_prompt(context: RunContextWrapper[AgentContext], agent: Any):
        return get_prompt("arxiv_search/arxiv_search_agent")
