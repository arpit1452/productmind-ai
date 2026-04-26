from langchain.tools import tool
from tavily import TavilyClient
from app.core.llm_router import fast_llm
import os


# ─── Initialize Tavily Client ──────────────────────────────────────────────────
def get_tavily_client():
    """Get Tavily client using key from Streamlit secrets or environment."""
    try:
        import streamlit as st
        tavily_key = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY", ""))
    except Exception:
        tavily_key = os.getenv("TAVILY_API_KEY", "")
    return TavilyClient(api_key=tavily_key)


@tool
def search_tool(query: str) -> str:
    """
    Searches the web for latest market trends, competitor info, and industry data.
    Input should be a specific, targeted search query related to the product idea.
    Returns a structured summary of the most relevant and recent findings.
    Use this FIRST to ground research in real market data before calling other tools.
    """
    try:
        client = get_tavily_client()
        res = client.search(query=query, max_results=5)

        raw_results = []
        for r in res.get("results", []):
            title = r.get("title", "")
            content = r.get("content", "")
            url = r.get("url", "")
            raw_results.append(f"SOURCE: {title}\nURL: {url}\nCONTENT: {content}")

        combined = "\n\n---\n\n".join(raw_results)

        # Use LLM to synthesize raw search results into structured insights
        llm = fast_llm()
        summary_prompt = f"""
You are a market research analyst. The following are raw web search results for the query: "{query}"

RAW RESULTS:
{combined}

Synthesize these into a clean, structured market intelligence report:

## SEARCH QUERY
{query}

## KEY FINDINGS
- [3-5 most important facts/data points found]

## MARKET TRENDS
- [2-3 clear trends visible in the data]

## COMPETITOR SIGNALS
- [Any competitor names, products, or strategies mentioned]

## RELEVANT STATISTICS
- [Any numbers, percentages, market sizes mentioned]

## IMPLICATIONS FOR PRODUCT DEVELOPMENT
- [What does this mean for building a product in this space?]

Be concise but comprehensive. Only include information actually found in the search results.
"""
        return llm.invoke(summary_prompt).content

    except Exception as e:
        return f"Search failed for query '{query}': {str(e)}. Proceeding with available knowledge."