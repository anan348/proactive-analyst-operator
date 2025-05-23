import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from jinja2 import Template

from src.core.logger import apllog

class PromptManager:
    """
    継承機能を持つプロンプトテンプレート管理クラス。
    
    _extendsキーを使用して他のテンプレートを継承できるYAMLテンプレートをサポート
    Jinja2テンプレートを使用して、カスタム変数でレンダリング
    """
    
    # 初期化フラグ
    _is_initialized = False
    
    def initialize(self, prompt_dir: Union[str, Path]) -> None:
        """
        プロンプトマネージャーを初期化
        
        引数:
            prompt_dir: プロンプトテンプレートのディレクトリパス
        """
        if self._is_initialized:
            apllog().warning("プロンプトマネージャーは既に初期化されています")
            return
            
        self.prompt_dir = Path(prompt_dir)
        self.templates_cache: Dict[str, Dict[str, Any]] = {}
        self._is_initialized = True
        apllog().info(f"プロンプトマネージャーを初期化しました: {self.prompt_dir}")
        
    def _check_initialized(self) -> None:
        """初期化されているか確認し、されていなければ例外を発生"""
        if not self._is_initialized:
            apllog().error("プロンプトマネージャーが初期化されていません。initialize()を先に呼び出してください")
            raise RuntimeError("PromptManager not initialized. Call initialize() first")
        
    def _find_template_file(self, template_name: str) -> Optional[Path]:
        """
        サブディレクトリを検索してテンプレートファイルを検索
        
        引数:
            template_name: 検索するテンプレート名
            
        戻り値:
            見つかった場合はテンプレートファイルのPath、見つからなかった場合はNone
        """
        self._check_initialized()
        
        # まず直接テンプレート名を試す（完全なパスの可能性）
        if "/" in template_name or "\\" in template_name:
            path = self.prompt_dir / f"{template_name}.yaml"
            if path.exists() and path.is_file():
                return path
        
        # すべてのサブディレクトリを検索
        for root, _, files in os.walk(self.prompt_dir):
            for file in files:
                if file == f"{template_name}.yaml":
                    return Path(root) / file
                
                # "triage/triage_agent"のようなパスを処理
                path_parts = template_name.split("/")
                if len(path_parts) > 1 and file == f"{path_parts[-1]}.yaml":
                    rel_path = Path(root).relative_to(self.prompt_dir)
                    if str(rel_path) == "/".join(path_parts[:-1]):
                        return Path(root) / file
                    
        apllog().warning(f"テンプレートファイル '{template_name}' が見つかりません")
        return None
    
    # 残りのメソッドはほぼ同じですが、必要に応じて_check_initialized()を追加
    
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """YAMLファイルを辞書に読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            apllog().error(f"YAMLファイル {file_path} の読み込みエラー: {e}")
            return {}
    
    def _get_template_dict(self, template_name: str) -> Dict[str, Any]:
        """
        継承関係を解決したテンプレート辞書を取得
        
        引数:
            template_name: 読み込むテンプレート名
            
        戻り値:
            解決されたテンプレートデータを含む辞書
        """
        self._check_initialized()
        
        # キャッシュから利用可能な場合は返す
        if template_name in self.templates_cache:
            return self.templates_cache[template_name]
        
        template_path = self._find_template_file(template_name)
        if not template_path:
            apllog().error(f"テンプレート '{template_name}' が見つかりません")
            return {}
        
        yaml_data = self._load_yaml(template_path)
        if not yaml_data:
            return {}
        
        # テンプレートキーを見つける - 最初に完全一致を試す
        parts = template_name.split("/")
        template_key = parts[-1]  # パスの最後の部分
        
        # 読み込まれたYAMLでキーを見つけようとする
        if template_key not in yaml_data:
            # 見つからない場合は最初のキーを試す
            if yaml_data:
                template_key = list(yaml_data.keys())[0]
            else:
                apllog().error(f"'{template_name}' に有効なテンプレートが見つかりません")
                return {}
            
        template_data = yaml_data[template_key]
        
        # 継承関係の処理
        if "_extends" in template_data:
            parent_name = template_data["_extends"]
            parent_data = self._get_template_dict(parent_name)
            
            # 親データから始めて、現在のテンプレートで上書き
            resolved_data = self._merge_templates(parent_data, template_data)
        else:
            resolved_data = template_data
        
        # 結果をキャッシュ
        self.templates_cache[template_name] = resolved_data
        return resolved_data
    
    def _merge_templates(self, parent: Dict[str, Any], child: Dict[str, Any]) -> Dict[str, Any]:
        """
        親テンプレートと子テンプレートをマージ
        
        引数:
            parent: 親テンプレート辞書
            child: 子テンプレート辞書
            
        戻り値:
            マージされたテンプレート辞書
        """
        result = parent.copy()
        
        for key, value in child.items():
            # _extendsキーをスキップ
            if key == "_extends":
                continue
                
            # 親の値を上書き
            result[key] = value
        
        return result
    
    def get_prompt(self, template_name: str, variables: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """
        テンプレートから完全にレンダリングされたプロンプトを取得
        
        引数:
            template_name: レンダリングするテンプレート名
            variables: テンプレートに注入する変数の辞書
            **kwargs: テンプレートに注入する追加の変数
            
        戻り値:
            レンダリングされたプロンプト文字列
        """
        self._check_initialized()
        
        template_data = self._get_template_dict(template_name)
        if not template_data:
            return ""
        
        # テンプレートがtemplateフィールドを持っているか確認
        if "template" not in template_data:
            apllog().error(f"テンプレート '{template_name}' には 'template' フィールドがありません")
            return ""
        
        # すべてのテンプレート変数でコンテキストを作成
        context = {k: v for k, v in template_data.items() if k != "template"}
        
        # 辞書とkwargsから提供された変数で上書き
        if variables:
            context.update(variables)
        context.update(kwargs)
        
        # テンプレートをレンダリング
        template_str = template_data["template"]
        
        # Jinja2スタイル {{ var }} と単純スタイル {var} の両方をサポート
        # {var} を Jinja2 用の {{ var }} に変換
        template_str = re.sub(r'(?<!\{)\{([^{}]+)\}(?!\})', r'{{ \1 }}', template_str)
        
        template = Template(template_str)
        return template.render(**context)
    
    def list_available_templates(self) -> List[str]:
        """
        利用可能なすべてのテンプレートファイルを一覧表示
        
        戻り値:
            テンプレート名のリスト
        """
        self._check_initialized()
        
        templates = []
        for root, _, files in os.walk(self.prompt_dir):
            for file in files:
                if file.endswith('.yaml'):
                    path = Path(root) / file
                    relative_path = path.relative_to(self.prompt_dir)
                    template_name = str(relative_path.with_suffix(''))
                    templates.append(template_name)
        return templates

# グローバルにアクセス可能なインスタンスを作成
prompt_manager = PromptManager()

# 簡易アクセス関数（オプション）
def get_prompt(template_name: str, variables: Optional[Dict[str, Any]] = None, **kwargs) -> str:
    """
    テンプレート名から直接プロンプトを取得する簡易関数
    
    引数:
        template_name: テンプレート名
        variables: 変数辞書
        **kwargs: 追加の変数
        
    戻り値:
        レンダリングされたプロンプト
    """
    return prompt_manager.get_prompt(template_name, variables, **kwargs)