from agents import Agent

from src.core.logger import apllog


class AgentRegistry:
    """エージェントインスタンスを管理するレジストリー"""

    def __init__(self):
        self.agents = {}
        apllog().debug("エージェントレジストリーを初期化しました。")

    def register_agent(self, agent: Agent):
        """エージェントをレジストリーに登録する"""
        if agent.name in self.agents:
            apllog().warning(f"エージェント {agent.name} はすでに登録されています。")
        else:
            self.agents[agent.name] = agent
            apllog().debug(f"エージェント {agent.name} をレジストリーに登録しました。")

    def get_agent(self, name: str) -> Agent:
        """レジストリーからエージェントを取得する"""
        if name in self.agents:
            apllog().debug(f"エージェント {name} をレジストリーから取得しました。")
            return self.agents[name]
        else:
            apllog().warning(f"エージェント {name} はレジストリーに登録されていません。")
            return None
        
    def list_agents(self) -> list[str]:
        """レジストリーに登録されているエージェントのリストを取得する"""
        agent_names = list(self.agents.keys())
        apllog().debug(f"レジストリーに登録されているエージェント: {agent_names}")
        return agent_names
    
    def get_agent_list(self) -> list[Agent]:
        """レジストリーに登録されているエージェントのリストを取得する"""
        agents = list(self.agents.values())
        apllog().debug(f"レジストリーに登録されているエージェント: {agents}")
        return agents
    
agent_registry = AgentRegistry()