import arxiv
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .client import ArxivClient


class SearchAPIResponse(BaseModel):
    title: str = Field(description="論文のタイトル")
    authors: List[str] = Field(description="著者のリスト")
    abstract: str = Field(description="論文の要約")
    pdf_url: str = Field(description="論文のPDFファイルのURL")
    published: str = Field(description="論文の公開日")
    categories: List[str] = Field(description="論文のカテゴリーリスト")
    doi: Optional[str] = Field(
        description="論文のDOI (Digital Object Identifier)、存在しない場合もある"
    )


def search_api(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[SearchAPIResponse]:
    """
    arXivで論文を検索する内部関数

    Args:
        query (str): 検索クエリ
        max_results (int): 取得する論文の最大数
        sort_by (str): ソート方法 ("relevance", "lastUpdatedDate", "submittedDate")
        start_date (datetime): 論文がpublishされた日で絞り込む場合の開始日（YYYY-MM-DD形式）
        end_date (datetime): 論文がpublishされた日で絞り込む場合の終了日（YYYY-MM-DD形式）

    Returns:
        List[SearchAPIResponse]: 検索結果のリスト
    """

    # 日付フィルターの構築
    date_filter = ""
    if start_date or end_date:
        start_str = start_date.strftime("%Y%m%d%H%M")
        end_str = end_date.strftime("%Y%m%d%H%M")
        date_filter = f"+AND+submittedDate:[{start_str}+TO+{end_str}]"

    # 検索クエリに日付フィルターを追加
    full_query = query + date_filter

    # ソート方法の設定
    sort_criterion = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }.get(sort_by, arxiv.SortCriterion.Relevance)

    # クライアントの作成
    client = ArxivClient.arxiv_client()

    # 検索の実行
    search = arxiv.Search(
        query=full_query, max_results=max_results, sort_by=sort_criterion
    )

    # 結果の取得と整形
    results = []
    for paper in client.results(search):
        results.append(
            ArxivPaper(
                title=paper.title,
                authors=[author.name for author in paper.authors],
                abstract=paper.summary,
                pdf_url=paper.pdf_url,
                published=paper.published.strftime("%Y-%m-%d"),
                categories=paper.categories,
                doi=paper.doi,
            )
        )

    return results
