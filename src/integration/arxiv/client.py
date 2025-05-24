import arxiv

from src.core.settings import Settings

class ArxivClient:

    st = Settings()

    @classmethod
    def arxiv_client(cls) -> arxiv.Client:
        """arXiv Client"""
        return arxiv.Client()
