from duckduckgo_search import ddg
from typing import List

def web_search(query: str, max_results: int = 5) -> List[str]:
    results = ddg(query, max_results=max_results) or []
    snippets = []
    for r in results:
        snippet = r.get("body") or r.get("title") or ""
        if snippet:
            snippets.append(snippet)
    return snippets
