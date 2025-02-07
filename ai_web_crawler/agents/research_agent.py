# ./ai_web_crawler/agents/research_agent.py

import asyncio
import uuid

from crawl4ai import AsyncWebCrawler

from ai_web_crawler.config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from ai_web_crawler.utils.scraper_utils import (
    get_browser_config,
    get_llm_strategy,
    fetch_and_process_page,
)
from ai_web_crawler.utils.data_utils import save_venues_to_csv


class ResearchAgent:
    """
    Research Agent that leverages the crawling process from main.py.

    When invoked, this agent performs the same operations as running the main
    asynchronous crawler:
        - It iterates over pages using AsyncWebCrawler.
        - Applies the same logic for processing pages with fetch_and_process_page.
        - Saves the collected venue data to a CSV file.
    """

    def __init__(
        self, 
        max_pages: int = 5, 
        sleep_time: int = 2
    ):
        """
        Initialize the Research Agent.

        Args:
            max_pages (int): Maximum number of pages to crawl.
            sleep_time (int): Number of seconds to sleep between page requests.
        """
        self.max_pages = max_pages
        self.sleep_time = sleep_time

    async def run(self) -> list:
        """
        Run the crawling process.

        Returns:
            list: All collected venues from the crawl.
        """
        # Initialize state variables
        all_venues = []
        page_number = 1
        seen_names = set()
        session_id = uuid.uuid4().hex

        # Initialize configurations
        browser_config = get_browser_config()
        llm_strategy = get_llm_strategy()

        async with AsyncWebCrawler(config=browser_config) as crawler:
            while page_number <= self.max_pages:
                venues, no_results_found = await fetch_and_process_page(
                    crawler,
                    page_number,
                    BASE_URL,
                    CSS_SELECTOR,
                    llm_strategy,
                    session_id,
                    REQUIRED_KEYS,
                    seen_names,
                )

                if no_results_found:
                    print("No more venues found. Ending crawl.")
                    break

                if not venues:
                    print(f"No venues extracted from page {page_number}.")
                    break

                all_venues.extend(venues)
                page_number += 1

                # Be polite with a pause between requests
                await asyncio.sleep(self.sleep_time)

        if all_venues:
            save_venues_to_csv(all_venues, "agent_venues.csv")
            print(f"Saved {len(all_venues)} venues to 'agent_venues.csv'.")
        else:
            print("No venues collected during the crawl.")

        return all_venues


if __name__ == "__main__":
    agent = ResearchAgent()
    asyncio.run(agent.run())
