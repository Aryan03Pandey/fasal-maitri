from duckduckgo_search import DDGS  # Change from 'ddg' to 'DDGS'

def web_search(query: str, max_results: int = 3) -> list[str]:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [result['body'] for result in results]
