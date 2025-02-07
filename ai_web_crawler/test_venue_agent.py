import asyncio
import os

from crewai import LLM, Agent, Crew
from dotenv import load_dotenv


from ai_web_crawler.tasks.venue_research_task import VenueResearchTask
from ai_web_crawler.tools.venue_research_tool import VenueResearchTool

load_dotenv()
import nest_asyncio; nest_asyncio.apply() 
os.environ.pop("OPENAI_API_KEY", None)


async def test_venue_research():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment!")

    # Create an explicit LLM instance for Groq.
    groq_llm = LLM(
        model="groq/mixtral-8x7b-32768",  # Specify the Groq model
        api_key=groq_api_key,
        temperature=0.7,
        timeout=120,
    )

    # Initialize the researcher agent and pass the LLM instance directly.
    researcher = Agent(
        role="Venue Researcher",
        goal="Research and collect detailed information about wedding venues",
        backstory="Expert at collecting and analyzing venue information using Crawl4AI and Groq",
        verbose=True,
        allow_delegation=False,
        tools=[VenueResearchTool()],
        llm=groq_llm,  # Pass the instantiated LLM (instead of using llm_config)
    )

    # Create the research task
    research_task = VenueResearchTask(
        description="Research wedding venues and extract their details",
        agent=researcher,
    )

    # Create and run the crew
    crew = Crew(agents=[researcher], tasks=[research_task], verbose=True)

    result = await crew.kickoff()
    return result


if __name__ == "__main__":
    asyncio.run(test_venue_research())
