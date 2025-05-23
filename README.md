# proactive-analyst-operator

## 概要

このプロジェクトは、ユーザークエリを分析し適切な処理を行う AI オペレーターシステムです。分析に特化した AI エージェントを活用し、ユーザーの要求に対して効率的な回答や解決策を提供します。

## 使用方法

1. リポジトリをクローンします

```
git clone https://github.com/yourusername/proactive-analyst-operator.git
cd proactive-analyst-operator
```

2. 必要な依存関係をインストールします

```
pip install -r requirements.txt
```

3. 環境変数の設定

```
# .env ファイルを作成して以下の変数を設定
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2023-05-15
```

4. システムを起動し、クエリを入力することで分析を開始できます
   Windows の場合:

```
$env:PYTHONPATH="."; python .\src\main.py
```

Linux/Mac の場合:

```
PYTHONPATH="." python ./src/main.py
```

## プロジェクト構造

proactive-analyst-operator/
├── config/ # 設定ファイル
│ └── prompt/ # プロンプトテンプレート
├── src/ # ソースコード
│ ├── ai_agents/ # AI エージェント実装
│ ├── core/ # コア機能
│ └── integration/ # 外部サービス連携
├── tools/ # ユーティリティツール
└── tests/ # テストコード
