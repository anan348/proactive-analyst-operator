from typing import Any

from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper

from ai_agents.context import AgentContext
from src.core.prompt_manager import get_prompt

class TriageAgent(Agent[AgentContext]):

    def __init__(self, model: OpenAIChatCompletionsModel, name: str = 'triage_agent'):
        super().__init__(name, model)
        self.name = name
        self.model = model
        self.instructions = self._set_prompt

    @staticmethod
    def _set_prompt(context: RunContextWrapper[AgentContext], agent: Any):
        return get_prompt('triage/triage_agent')