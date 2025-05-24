import os

from src.ai_agents.triage.triage_agent import TriageAgent
from ai_agents.registry import agent_registry
from src.core.model_factory import ModelFactory
from src.core.logger import apllog

# エージェントのインスタンスを作成
triage_agent = TriageAgent(ModelFactory.get_default_model())

# エージェントをレジストリに登録
agent_registry.register_agent(triage_agent)
apllog().info(f"エージェント {triage_agent.name} をレジストリに登録しました。")

# タスクの全エージェントをレジストリに登録したことを確認するためのログ
task_name: str = os.path.basename(os.path.dirname(__file__))
apllog().info(f"タスク '{task_name}' の全エージェントをレジストリに登録しました。")