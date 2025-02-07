# ./ai_web_crawler/example_usage.py

import asyncio
import os
from ai_web_crawler.agents.research_agent import ResearchAgent


async def test_research_agent():
    """
    Test the research agent's crawling capabilities.
    """
    # Initialize the agent with custom parameters
    agent = ResearchAgent(max_pages=5, sleep_time=2)
    
    # Run the crawler process
    venues = await agent.run()
    
    # Verify results
    if os.path.exists("agent_venues.csv"):
        print(f"Success! Collected {len(venues)} venues.")
        print("Results saved to 'agent_venues.csv'")
    else:
        print("Error: agent_venues.csv file was not created.")

    return venues


if __name__ == "__main__":
    asyncio.run(test_research_agent())
