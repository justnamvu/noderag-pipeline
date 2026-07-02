from opensearchpy import OpenSearch
from app.core.config import settings

_client: OpenSearch | None = None


def get_client() -> OpenSearch:
    global _client
    if _client is None:
        _client = OpenSearch(
            hosts=[settings.opensearch_url],
            use_ssl=False,
            verify_certs=False,
        )
    return _client
