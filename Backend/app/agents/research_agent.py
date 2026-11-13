from tavily import TavilyClient

from app.config import TAVILY_API_KEY


class ResearchAgent:
    def __init__(self):
        self.client = TavilyClient(
            api_key=TAVILY_API_KEY
        )

    def research(self, topic: str):
        response = self.client.search(
            query=topic,
            search_depth="advanced",
            max_results=5,
            include_answer=False,
            include_raw_content=True,
        )

        sources = []

        for result in response.get("results", []):
            sources.append(
                {
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "published_at": result.get(
                        "published_date"
                    ),
                    "content": result.get(
                        "raw_content"
                    ) or result.get("content"),
                }
            )

        return sources