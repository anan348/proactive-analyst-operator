from pathlib import Path

import asyncio
from agents import Runner
from agents import set_tracing_disabled

from src.core.prompt_manager import prompt_manager
from src.core.logger import apllog, init_apl_logger

# 初期化
## traceを無効化
set_tracing_disabled(True)

## ロガーの初期化
init_apl_logger('./logs/apl.log')

## プロンプトマネージャーの初期化
root_dir = Path(__file__).parent.parent
prompt_dir = root_dir / "config" / "prompt"
prompt_manager.initialize(prompt_dir)

## Agentのインスタンス化/レジストリに登録
import src.ai_agents
from ai_agents.registry import agent_registry
from ai_agents.context import AgentContext


async def main() -> None:

    context = AgentContext()
    context.history = []  
    first_agent = agent_registry.get_agent("triage_agent")

    try:
        while True:
            # 1️⃣ ユーザー入力を取得
            user_input = input("👤> ").strip()
            if user_input == "":
                continue  # 空行ならスキップ

            # 2️⃣ history に追加（ユーザー側）
            context.history.append({"role": "user", "content": user_input})

            # 3️⃣ Runner で推論（同期版なので普通の関数呼び出し）
            result = await Runner.run(
                starting_agent=first_agent,
                input=context.history,   # ← 過去ログごと渡す
                context=context,
            )

            # 4️⃣ 最終出力を取り出して表示
            ai_reply: str = result.final_output  # type: ignore
            print("🤖>", ai_reply)

            # 5️⃣ history に追加（アシスタント側）
            context.history.append({"role": "assistant", "content": ai_reply})

    except KeyboardInterrupt:
        # Ctrl+C を受け取ったら優雅に終了
        print("\n🛑 チャットを終了しました。履歴は ctx.history に残っています。")

if __name__ == "__main__":
    asyncio.run(main())
