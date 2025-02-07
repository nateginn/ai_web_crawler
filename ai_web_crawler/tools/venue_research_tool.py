# ./ai_web_crawler/tools/venue_research_tool.py

import asyncio
from typing import List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ai_web_crawler.agents.research_agent import ResearchAgent
from ai_web_crawler.models.venue import Venue


class VenueResearchTool(BaseTool):
    """Tool for researching venue information using Crawl4AI and Groq."""
    
    name: str = "Venue Research Tool"
    description: str = "Researches wedding venues using Crawl4AI and Groq LLM for extraction"
    max_pages: int = Field(default=5, description="Maximum number of pages to crawl")
    sleep_time: int = Field(default=2, description="Time to wait between requests")

    async def _arun(self, max_pages: int = 5, sleep_time: int = 2) -> List[Venue]:
        """
        Executes the venue research asynchronously using Crawl4AI.
        """
        agent = ResearchAgent(max_pages=max_pages, sleep_time=sleep_time)
        venues = await agent.run()
        return [Venue(**venue) for venue in venues]

    def _run(self, max_pages: int = 5, sleep_time: int = 2) -> List[Venue]:
        """
        Synchronous wrapper for the asynchronous execution.
        """
        return asyncio.run(self._arun(max_pages, sleep_time))
