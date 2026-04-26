from langchain.tools import tool
from app.core.llm_router import fast_llm


def _safe_retrieve(query: str) -> str:
    """Safely attempts to retrieve from vector store, returns empty string on failure."""
    try:
        from app.rag.vector_db import retrieve
        result = retrieve(query)
        return result if result else ""
    except Exception as e:
        return ""


@tool
def rag_tool(query: str) -> str:
    """
    Retrieves relevant information from uploaded PDF documents using semantic vector search.
    Input should be a specific question or topic relevant to the product domain.
    Use this to extract insights from research papers, market reports, or product docs uploaded by the user.
    Only use this if the user has uploaded documents — if retrieval returns nothing, report that and move on.
    """
    raw_result = _safe_retrieve(query)

    if not raw_result or raw_result.strip() == "":
        return "No relevant documents found in the knowledge base. Either no PDFs were uploaded, or the uploaded documents don't contain information relevant to this query. Proceeding without RAG context."

    # Use LLM to synthesize raw chunks into useful insights
    llm = fast_llm()
    synthesis_prompt = f"""
You are analyzing content retrieved from uploaded documents to answer a product research question.

QUERY: {query}

RETRIEVED DOCUMENT CONTENT:
{raw_result}

Synthesize the most relevant insights from these documents:

## DOCUMENT INSIGHTS FOR: {query}

### Key Points Found
[List the most relevant facts, data, or insights from the documents]

### Quotes or Data Worth Noting
[Any specific numbers, findings, or quotes that are directly relevant]

### Implications for Product Development
[How does this document knowledge apply to building the product?]

### Gaps
[What important questions does this document NOT answer?]

Only include information actually present in the retrieved content. Do not hallucinate.
"""
    return llm.invoke(synthesis_prompt).content