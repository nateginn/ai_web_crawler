# ./ai_web_crawler/tasks/venue_research_task.py

from typing import List
from crewai import Task
from ai_web_crawler.tools.venue_research_tool import VenueResearchTool
from ai_web_crawler.models.venue import Venue


class VenueResearchTask(Task):
    """Task for researching wedding venues using Crawl4AI and Groq extraction."""

    def __init__(self, description: str, agent: any):
        super().__init__(
            description=description,
            agent=agent,
            expected_output="A list of wedding venues with their details including name, location, price, capacity, rating, reviews, and description."
        )

    async def execute(self) -> List[Venue]:
        """
        Executes the venue research task using Crawl4AI and Groq.
        
        Returns:
            List[Venue]: List of validated venue objects
        """
        research_tool = VenueResearchTool()
        
        self.agent.say("Starting venue research using Crawl4AI and Groq...")
        venues = await research_tool._arun(max_pages=5)
        
        if venues:
            self.agent.say(f"Successfully extracted {len(venues)} venues using Groq LLM.")
        else:
            self.agent.say("No venues were extracted during the crawl.")
            
        return venues
