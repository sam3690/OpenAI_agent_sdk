from duckduckgo_search import DDGS
from agents import function_tool

@function_tool
def WebsearchTools(query):
    try:
        with DDGS() as ddgs:
              results = list(ddgs.text(query, max_results=5))
              if not results:
                   return print("no reasult found for : {query}")
        result_format =[]
        for results in results:
             tittle = results.get('title', '')
             body = results.get('body', '')
             result_format.append(f"tittle: {tittle}\nDescription: {body}\n")
                   
    except Exception as e:
        print('error')

