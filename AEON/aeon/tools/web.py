
from duckduckgo_search import DDGS

def search_web(query: str) -> str:
    """Searches the web using DuckDuckGo."""
    try:
        results = DDGS().text(query, max_results=5)
        formatted_results = []
        for r in results:
            formatted_results.append(f"- [{r['title']}]({r['href']}): {r['body']}")
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Search Error: {e}"
