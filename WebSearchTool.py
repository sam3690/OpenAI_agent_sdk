from agents import function_tool
from duckduckgo_search import DDGS

@function_tool
def custom_web_search(query: str) -> str:
    """Search the web for the latest information on stocks or crypto markets.
    
    Args:
        query: The search query
        
    Returns:
        Formatted search results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return f"No results found for: {query}"
        
        # Format results properly
        formatted_results = []
        for result in results:
            title = result.get('title', '')
            body = result.get('body', '')
            formatted_results.append(f"Title: {title}\nDescription: {body}\n")
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"Search error: {str(e)}"
