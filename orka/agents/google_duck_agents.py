import os
import json
from .agent_base import BaseAgent
from googleapiclient.discovery import build
from duckduckgo_search import DDGS

# Google config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

class GoogleSearchAgent(BaseAgent):
    def run(self, input_data):
        if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
            raise EnvironmentError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID")
        try:
            service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
            result = service.cse().list(q=input_data, cx=GOOGLE_CSE_ID, num=3).execute()
            items = result.get("items", [])
            return [item.get("snippet", "") for item in items if isinstance(item, dict)]
        except Exception as e:
            return [f"Google API error: {e}"]


class DuckDuckGoAgent(BaseAgent):
    def run(self, input_data):
        query = input_data["input"]
        if not query:
            return ["No query provided"]
        try:
            with DDGS() as ddgs:
                results = [r["body"] for r in ddgs.text(query, max_results=5)]
            return results
        except Exception as e:
            return [f"DuckDuckGo search failed: {str(e)}"]
        