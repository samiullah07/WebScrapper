import os
from dotenv import load_dotenv
import httpx
import asyncio
import http.client
import json
from utils import clean_html_to_text
from fastmcp import FastMCP
load_dotenv()


mcp = FastMCP("docs")
#search on web

Super_URL = "https://google.serper.dev/search"
async def search_web(query) -> dict  | None:
    payload = {
        "q": query,
        "num": 2
    }
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            Super_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        return response.json()
 

# Open Official Documentation

async def fetch_url(url:str):
     async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            timeout=30
        )

        return clean_html_to_text(response.text)
     


docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
    "uv": "docs.astral.sh/uv",
}

@mcp.tool()
async def fetch_official_docs(query: str, library) -> str | None:
    """
    Search the latest docs for a given query and library.
    Supports langchain, openai, llama-index and uv.
    Args:
        query: The query to search for (e.g. "Publish a package with UV")
        library: The library to search in (e.g. "uv")

    Returns:
        Summarized text from the docs with source links.

    """

    if library not in docs_urls:
        return "Documentation for the specified topic is not available."

    # url = f"https://{docs_urls[query]}"
    content = await search_web(query)
    
    # handle cases where search_web returned None or an unexpected structure
    if not content or not isinstance(content, dict):
        return "No relevant documentation found in search results."
    
    results = content.get('organic')
    if not results or not isinstance(results, (list, tuple)) or len(results) == 0:
        return "No relevant documentation found in search results."
    
    text_part = []

    for result in results:
        url = result.get('link','')
        raw = await fetch_url(url)

        if raw:
            labeled = f"Source: {url}\nContent:\n{raw}\n"
            text_part.append(labeled)
    return "\n\n".join(text_part)



if __name__ == "__main__":
    mcp.run(transport="stdio")
    


