"""
プロンプトテンプレートを表示するコマンドラインツール。
テンプレート名を指定すると、そのプロンプトの全内容が表示されます。
"""
import argparse
import sys
import yaml
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.prompt_manager import prompt_manager, get_prompt
from src.core.logger import init_apl_logger, apllog

def debug_yaml_structure(prompt_dir, template_name):
    """指定されたテンプレートのYAML構造をデバッグ出力"""
    parts = template_name.split('/')
    filename = f"{parts[-1]}.yaml"
    
    # ディレクトリ検索
    template_path = None
    for root, _, files in os.walk(prompt_dir):
        if filename in files:
            if len(parts) > 1:
                # パスの一部がディレクトリ構造と一致するか確認
                rel_path = Path(root).relative_to(prompt_dir)
                dir_parts = str(rel_path).split(os.sep)
                if dir_parts == parts[:-1]:
                    template_path = Path(root) / filename
                    break
            else:
                template_path = Path(root) / filename
                break
    
    if not template_path:
        print(f"警告: '{template_name}' のYAMLファイルが見つかりません")
        return
    
    # YAMLファイルの内容を表示
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            yaml_content = yaml.safe_load(f)
        
        print(f"\nYAML構造 ({template_path}):")
        print("="*50)
        print(yaml.dump(yaml_content, allow_unicode=True, default_flow_style=False))
        print("="*50)
        
        # 継承関係を確認
        for key, value in yaml_content.items():
            if isinstance(value, dict) and "_extends" in value:
                extends = value["_extends"]
                print(f"継承関係: '{key}' は '{extends}' を継承しています")
                # 継承先も確認
                debug_yaml_structure(prompt_dir, extends)
    except Exception as e:
        print(f"YAMLデバッグエラー: {e}")

def main():
    """メイン実行関数"""
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="プロンプトテンプレートビューア")
    parser.add_argument("template_name", nargs='?', help="表示するテンプレート名（例：triage/triage_agent）")
    parser.add_argument("--vars", nargs="+", help="変数値をkey=value形式で指定（例：context=テストコンテキスト）")
    parser.add_argument("--list", action="store_true", help="利用可能なテンプレート一覧を表示")
    parser.add_argument("--debug", action="store_true", help="デバッグ情報を表示")
    
    args = parser.parse_args()
    
    # ロガー初期化
    init_apl_logger('./logs')
    
    # プロンプトマネージャーの初期化
    root_dir = Path(__file__).parent.parent
    prompt_dir = root_dir / "config" / "prompt"
    prompt_manager.initialize(prompt_dir)
    
    # テンプレート名が必要
    if not args.template_name:
        parser.print_help()
        return
    
    # 変数の解析
    variables = {}
    if args.vars:
        for var in args.vars:
            if "=" in var:
                key, value = var.split("=", 1)
                variables[key.strip()] = value.strip()
    
    # プロンプトの取得と表示
    try:
        prompt = get_prompt(args.template_name, variables)
        
        print("="*50)
        print(f"テンプレート: {args.template_name}")
        print("="*50)
        print(prompt)
        print("="*50 + "\n")
    except Exception as e:
        apllog().error(f"プロンプト表示エラー: {e}")
        print(f"エラー: {e}")
        if not args.debug:
            print("詳細情報を確認するには --debug オプションを使用してください")

if __name__ == "__main__":
    main()