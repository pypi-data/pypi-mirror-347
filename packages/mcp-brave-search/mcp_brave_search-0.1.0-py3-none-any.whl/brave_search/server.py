#!/usr/bin/env python3

import asyncio
import os
import time
from typing import Any, Dict, List, Optional, TypedDict, Union
from urllib.parse import urlencode
import logging
from dotenv import load_dotenv

import httpx
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Brave Search Server")

# Tool definitions
WEB_SEARCH_TOOL = {
    "name": "brave_web_search",
    "description": (
        "Performs a web search using the Brave Search API, ideal for general queries, news, articles, and online content. "
        "Use this for broad information gathering, recent events, or when you need diverse web sources. "
        "Supports pagination, content filtering, and freshness controls. "
        "Maximum 20 results per request, with offset for pagination."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (max 400 chars, 50 words)"
            },
            "count": {
                "type": "number",
                "description": "Number of results (1-20, default 10)",
                "default": 10
            },
            "offset": {
                "type": "number",
                "description": "Pagination offset (max 9, default 0)",
                "default": 0
            },
        },
        "required": ["query"],
    },
}

LOCAL_SEARCH_TOOL = {
    "name": "brave_local_search",
    "description": (
        "Searches for local businesses and places using Brave's Local Search API. "
        "Best for queries related to physical locations, businesses, restaurants, services, etc. "
        "Returns detailed information including:\n"
        "- Business names and addresses\n"
        "- Ratings and review counts\n"
        "- Phone numbers and opening hours\n"
        "Use this when the query implies 'near me' or mentions specific locations. "
        "Automatically falls back to web search if no local results are found."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Local search query (e.g. 'pizza near Central Park')"
            },
            "count": {
                "type": "number",
                "description": "Number of results (1-20, default 5)",
                "default": 5
            },
        },
        "required": ["query"]
    }
}

# Type definitions
class BraveWebResult(TypedDict):
    title: str
    description: str
    url: str
    language: Optional[str]
    published: Optional[str]
    rank: Optional[int]

class BraveWebResponse(TypedDict):
    web: Optional[Dict[str, List[BraveWebResult]]]
    locations: Optional[Dict[str, List[Dict[str, str]]]]

class BraveLocation(TypedDict):
    id: str
    name: str
    address: Dict[str, Optional[str]]
    coordinates: Optional[Dict[str, float]]
    phone: Optional[str]
    rating: Optional[Dict[str, Union[float, int]]]
    openingHours: Optional[List[str]]
    priceRange: Optional[str]

class BravePoiResponse(TypedDict):
    results: List[BraveLocation]

class BraveDescription(TypedDict):
    descriptions: Dict[str, str]

# Rate limiting
class RateLimit:
    def __init__(self, per_second: int = 1, per_month: int = 15000):
        self.per_second = per_second
        self.per_month = per_month
        self.request_count = {
            "second": 0,
            "month": 0,
            "last_reset": time.time()
        }

    def check(self) -> None:
        now = time.time()
        if now - self.request_count["last_reset"] > 1:
            self.request_count["second"] = 0
            self.request_count["last_reset"] = now
        
        if (self.request_count["second"] >= self.per_second or 
            self.request_count["month"] >= self.per_month):
            raise Exception("Rate limit exceeded")
        
        self.request_count["second"] += 1
        self.request_count["month"] += 1

# Initialize rate limiter and client
rate_limit = RateLimit()
Brasilapi_key = os.getenv("BRAVE_API_KEY")
if not api_key:
    raise ValueError("BRAVE_API_KEY environment variable is required")

client = httpx.AsyncClient(
    headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
)

async def perform_web_search(
    query: str, count: int = 10, offset: int = 0
) -> str:
    rate_limit.check()
    
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset
    }
    
    response = await client.get(
        "https://api.search.brave.com/res/v1/web/search",
        params=params
    )
    response.raise_for_status()
    
    data = response.json()["web"]["results"]
    results = [
        {
            "title": result.get("title", ""),
            "description": result.get("description", ""),
            "url": result.get("url", "")
        }
        for result in data
    ]
    
    results_text = "\n\n".join(
        f"Title: {r['title']}\nDescription: {r['description']}\nURL: {r['url']}"
        for r in results
    )
    
    # Add tool usage pills
    tools_used = """
---
**Tools Used:**
- `brave_web_search`: Performs web search with pagination support"""
    
    return results_text + tools_used

async def perform_local_search(query: str, count: int = 5) -> str:
    rate_limit.check()
    
    # Initial search to get location IDs
    params = {
        "q": query,
        "search_lang": "en",
        "result_filter": "locations",
        "count": min(count, 20)
    }
    
    response = await client.get(
        "https://api.search.brave.com/res/v1/web/search",
        params=params
    )
    response.raise_for_status()
    
    data = response.json()
    location_ids = [
        r["id"] for r in data.get("locations", {}).get("results", [])
        if r.get("id")
    ]
    
    if not location_ids:
        return await perform_web_search(query, count)
    
    # Get POI details and descriptions in parallel
    pois_data, descriptions_data = await asyncio.gather(
        get_pois_data(location_ids),
        get_descriptions_data(location_ids)
    )
    
    return format_local_results(pois_data, descriptions_data)

async def get_pois_data(ids: List[str]) -> BravePoiResponse:
    rate_limit.check()
    
    params = {"ids": ids}
    response = await client.get(
        "https://api.search.brave.com/res/v1/local/pois",
        params=params
    )
    response.raise_for_status()
    
    return response.json()

async def get_descriptions_data(ids: List[str]) -> BraveDescription:
    rate_limit.check()
    
    params = {"ids": ids}
    response = await client.get(
        "https://api.search.brave.com/res/v1/local/descriptions",
        params=params
    )
    response.raise_for_status()
    
    return response.json()

def format_local_results(
    pois_data: BravePoiResponse, desc_data: BraveDescription
) -> str:
    results = []
    for poi in pois_data["results"]:
        address_parts = [
            poi["address"].get("streetAddress", ""),
            poi["address"].get("addressLocality", ""),
            poi["address"].get("addressRegion", ""),
            poi["address"].get("postalCode", "")
        ]
        address = ", ".join(part for part in address_parts if part) or "N/A"
        
        rating = poi.get("rating", {})
        rating_str = (
            f"{rating.get('ratingValue', 'N/A')} "
            f"({rating.get('ratingCount', 0)} reviews)"
        )
        
        result = f"""Name: {poi['name']}
Address: {address}
Phone: {poi.get('phone', 'N/A')}
Rating: {rating_str}
Price Range: {poi.get('priceRange', 'N/A')}
Hours: {', '.join(poi.get('openingHours', [])) or 'N/A'}
Description: {desc_data['descriptions'].get(poi['id'], 'No description available')}"""
        results.append(result)
    
    results_text = "\n---\n".join(results) if results else "No local results found"
    
    # Add tool usage pills
    tools_used = """
---
**Tools Used:**
- `brave_local_search`: Searches for local businesses and places
- `brave_web_search`: Fallback for general web search when no local results found"""
    
    return results_text + tools_used

@mcp.tool(
    "brave_web_search",
    "Performs a web search using the Brave Search API, ideal for general queries, news, articles, and online content. "
    "Use this for broad information gathering, recent events, or when you need diverse web sources. "
    "Supports pagination, content filtering, and freshness controls. "
    "Maximum 20 results per request, with offset for pagination."
)
async def brave_web_search(
    query: str,
    count: int = 10,
    offset: int = 0
) -> str:
    """
    Perform a web search using Brave Search API
    
    Args:
        query: Search query (max 400 chars, 50 words)
        count: Number of results (1-20, default 10)
        offset: Pagination offset (max 9, default 0)
        
    Returns:
        str: Formatted search results
    """
    try:
        return await perform_web_search(query, count, offset)
    except Exception as e:
        logger.error(f"Error performing web search: {e}")
        return f"Error performing web search: {str(e)}"

@mcp.tool(
    "brave_local_search",
    "Searches for local businesses and places using Brave's Local Search API. "
    "Best for queries related to physical locations, businesses, restaurants, services, etc. "
    "Returns detailed information including:\n"
    "- Business names and addresses\n"
    "- Ratings and review counts\n"
    "- Phone numbers and opening hours\n"
    "Use this when the query implies 'near me' or mentions specific locations. "
    "Automatically falls back to web search if no local results are found."
)
async def brave_local_search(
    query: str,
    count: int = 5
) -> str:
    """
    Perform a local search using Brave Search API
    
    Args:
        query: Local search query (e.g. 'pizza near Central Park')
        count: Number of results (1-20, default 5)
        
    Returns:
        str: Formatted local search results
    """
    try:
        return await perform_local_search(query, count)
    except Exception as e:
        logger.error(f"Error performing local search: {e}")
        return f"Error performing local search: {str(e)}"

async def cleanup():
    await client.aclose()

def main():
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise

if __name__ == '__main__':
    main()