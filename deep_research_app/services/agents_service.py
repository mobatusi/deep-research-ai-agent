from crewai import Crew, Agent, Task
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from firecrawl import FirecrawlApp
import os

extracted_links = []

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Initialize Firecrawl client (lazy initialization)
firecrawl_client = None

def get_firecrawl_client():
    """Get or initialize the Firecrawl client."""
    global firecrawl_client
    if firecrawl_client is None:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError(
                "FIRECRAWL_API_KEY not found in environment variables. "
                "Please ensure you have a .env file in the deep_research_app directory with:\n"
                "FIRECRAWL_API_KEY=your_api_key_here"
            )
        firecrawl_client = FirecrawlApp(api_key=api_key)
    return firecrawl_client



@tool("Firecrawl Search")
def firecrawl_search(query: str) -> str:
    """Search the web using Firecrawl API and extract links.

    Args:
        query: A search query string to search the web

    Returns:
        Search results as text with extracted URLs and content
    """
    global extracted_links

    try:
        # Get Firecrawl client
        client = get_firecrawl_client()

        # Use Firecrawl SDK's search method with content extraction
        search_results = client.search(
            query=query,
            params={
                "limit": 5,  # Limit number of results
                "scrapeOptions": {
                    "formats": ["markdown", "html"]
                }
            }
        )

        # Extract URLs and content from results
        results_text = []

        if search_results and "data" in search_results:
            for item in search_results["data"]:
                # Extract URL
                if "url" in item:
                    url = item["url"]
                    extracted_links.append(url)

                # Extract content (markdown or html)
                content = item.get("markdown", item.get("html", ""))
                title = item.get("title", "No title")

                results_text.append(f"Title: {title}\nURL: {url}\n\nContent:\n{content}\n\n---\n")

        if results_text:
            return "\n".join(results_text)
        else:
            return "No search results found."

    except Exception as e:
        return f"Error during Firecrawl search: {str(e)}"



def setup_agents_and_tasks(query: str, breadth: int, depth: int):
    """
    Set up a multi-stage AI workflow with three specialized agents using CrewAI framework.

    Args:
        query: Research topic to explore
        breadth: How wide-ranging the research should be across sources/subtopics
        depth: How thoroughly to explore each source or branch

    Returns:
        tuple: (crew, researcher, firecrawl_tool)
    """
    # Initialize ChatOpenAI model with temperature=0.3 for balanced reasoning
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY
    )

    # Define Research Agent
    researcher = Agent(
        role="Web searcher and data collector",
        goal=f"Perform recursive research on '{query}' with breadth={breadth} and depth={depth}. "
             f"Gather raw HTML content, extract links, and collect key information using the Firecrawl API.",
        backstory="You are an expert at web research and data collection. Your specialty is finding "
                  "relevant information across the web and extracting valuable insights from various sources.",
        tools=[firecrawl_search],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    # Define Summarizer Agent
    summarizer = Agent(
        role="Data summarization specialist",
        goal="Condense collected research data into clear, structured bullet points that highlight key findings.",
        backstory="You are skilled at analyzing large amounts of data and extracting the most important "
                  "information. You excel at creating well-organized summaries that are easy to understand.",
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    # Define Presenter Agent
    presenter = Agent(
        role="Report formatting specialist",
        goal="Format summarized research into a professional, human-readable report with proper structure and clarity.",
        backstory="You are an expert at creating polished, professional reports. You know how to present "
                  "complex information in a way that is engaging and accessible to human readers.",
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    # Create Research Task
    task_research = Task(
        description=f"Conduct deep research on the topic: '{query}'. "
                   f"Use breadth={breadth} to explore {breadth} different sources or subtopics. "
                   f"Use depth={depth} to thoroughly investigate each source. "
                   f"Gather raw HTML content, extract links, and collect key insights. "
                   f"Use the Firecrawl search tool to perform comprehensive web research.",
        agent=researcher,
        expected_output="Raw HTML content, extracted links, and comprehensive insights about the research topic."
    )

    # Create Summarization Task
    task_summarize = Task(
        description="Analyze all research findings from the previous task. "
                   "Convert the raw data into well-structured summaries with clear bullet points. "
                   "Organize information by themes or categories. "
                   "Highlight the most important findings and insights.",
        agent=summarizer,
        expected_output="Well-structured bullet points summarizing key findings, organized by themes."
    )

    # Create Presentation Task
    task_present = Task(
        description="Create a final, polished research report from the summarized findings. "
                   "Format the content professionally with clear sections and headings. "
                   "Ensure the report is human-readable, engaging, and comprehensive. "
                   "Include an introduction, main findings, and conclusion.",
        agent=presenter,
        expected_output="A professional, formatted research report ready for human consumption."
    )

    # Orchestrate workflow with Crew
    crew = Crew(
        agents=[researcher, summarizer, presenter],
        tasks=[task_research, task_summarize, task_present],
        max_steps=20,
        max_time=300,
        verbose=True
    )

    return crew, researcher, firecrawl_search
