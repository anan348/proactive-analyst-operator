from dataclasses import dataclass

@dataclass
class AgentContext:
    history: list| None = None