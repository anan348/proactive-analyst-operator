import arxiv

from typing import List, Optional
from datetime import datetime
from pydantic import Field
from agents import function_tool
from integration.arxiv.search import search_api, SearchAPIResponse
from core.logger import apllog


@function_tool
def search_papers(
    query: str = Field(
        description="検索クエリ。以下のフィールドプレフィックスを使用できます：\n"
        "- ti: タイトル\n"
        "- au: 著者名\n"
        "- abs: アブストラクト\n"
        "- co: コメント\n"
        "- jr: ジャーナル参照\n"
        "- cat: サブジェクトカテゴリ\n"
        "- rn: レポート番号\n"
        "- all: すべてのフィールド\n"
        "例：'ti:machine learning'、'au:Smith'、'cat:cs.AI'"
    ),
    max_results: int = Field(
        default=10,
        ge=1,
        le=2000,
        description="取得する論文の最大数。1から2000の間で指定してください。",
    ),
    sort_by: str = Field(
        default="relevance",
        description="ソート方法。以下のいずれかを指定：\n"
        "- relevance: 関連度順（デフォルト）\n"
        "- lastUpdatedDate: 最終更新日順\n"
        "- submittedDate: 投稿日順",
    ),
    start_date: Optional[str] = Field(
        default=None,
        description="検索開始日。YYYY-MM-DD形式で指定。例：'2023-01-01'",
    ),
    end_date: Optional[str] = Field(
        default=None,
        description="検索終了日。YYYY-MM-DD形式で指定。例：'2023-12-31'",
    ),
) -> List[SearchAPIResponse]:
    """
    arXivで論文を検索する関数

    Args:
        query (str): 検索クエリ
        max_results (int): 取得する論文の最大数
        sort_by (str): ソート方法 ("relevance", "lastUpdatedDate", "submittedDate")
        start_date (str): 論文がpublishされた日で絞り込む場合の開始日（YYYY-MM-DD形式）
        end_date (str): 論文がpublishされた日で絞り込む場合の終了日（YYYY-MM-DD形式）

    Returns:
        List[SearchAPIResponse]: 検索結果のリスト。各論文は以下の情報を含む：
            - title: 論文タイトル
            - authors: 著者名のリスト
            - abstract: アブストラクト
            - pdf_url: PDFのURL
            - published: 公開日（YYYY-MM-DD形式）
            - categories: カテゴリのリスト
            - doi: DOI（存在する場合）
    """
    apllog().debug(
        f"""🪏search_papersが呼び出されました
        query: {query}
        max_results: {max_results}
        sort_by: {sort_by}
        start_date: {start_date}
        end_date: {end_date}
        """
    )
    # 日付フィルターの構築
    if start_date or end_date:
        start_date = (
            datetime.strptime(start_date, "%Y-%m-%d")
            if start_date
            else datetime(1991, 8, 14)
        )
        end_date = (
            datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now()
        )
    return search_api(
        query=query,
        max_results=max_results,
        sort_by=sort_by,
        start_date=start_date,
        end_date=end_date,
    )


# if __name__ == "__main__":
#     # 使用例（使用する場合はfunction_toolをコメントアウトする）
#     results = search_papers(
#         query="machine learning",
#         max_results=5,
#         sort_by="relevance",
#         start_date="2023-01-01",
#         end_date="2024-01-01",
#     )

#     # 結果の表示
#     print(json.dumps(results, indent=2, ensure_ascii=False))
