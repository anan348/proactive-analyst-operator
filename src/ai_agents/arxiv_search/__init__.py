from ai_agents.arxiv_search.arxiv_search_agent import ArxivSearchAgent
from ai_agents.registry import agent_registry
from src.core.model_factory import ModelFactory
from src.core.logger import apllog

# エージェントのインスタンスを作成
arxiv_search_agent = ArxivSearchAgent(ModelFactory.get_default_model())

# エージェントをレジストリに登録
agent_registry.register_agent(arxiv_search_agent)
apllog().info(f"エージェント {arxiv_search_agent.name} をレジストリに登録しました。")
