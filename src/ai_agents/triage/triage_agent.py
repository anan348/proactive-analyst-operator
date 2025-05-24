from typing import Any

from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper

from src.ai_agents.context import AgentContext
from src.ai_agents.identity_manager import AgentIdentityManager
from src.core.prompt_manager import get_prompt

class TriageAgent(Agent[AgentContext]):

    def __init__(self, model: OpenAIChatCompletionsModel, name: str = AgentIdentityManager.Triage.triage_agent):
        super().__init__(name, model)
        self.name = name
        self.model = model
        self.instructions = self._set_prompt

    @staticmethod
    def _set_prompt(context: RunContextWrapper[AgentContext], agent: Any):
        return get_prompt(f'{AgentIdentityManager.Triage.task_name}/{AgentIdentityManager.Triage.triage_agent}')