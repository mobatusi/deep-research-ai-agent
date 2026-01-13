from services.agents_service import setup_agents_and_tasks
from models.pdf_generator import create_pdf
from utils.markdown_cleaner import clean_markdown
import base64

extracted_links = []


def run_deep_research(query: str, breadth: int, depth: int):
    """
    Run the complete research workflow using CrewAI.

    This function executes a multi-stage research process:
    1. Initialize research crew with agents
    2. Execute the research workflow
    3. Clean and format the output
    4. Generate a PDF report
    5. Encode PDF for API transmission

    Args:
        query: The research topic/question
        breadth: How many sources/subtopics to explore
        depth: How thoroughly to investigate each source

    Returns:
        tuple: (cleaned_output, pdf_data, base64_pdf)
            - cleaned_output: Cleaned markdown text
            - pdf_data: Binary PDF data
            - base64_pdf: Base64-encoded PDF string
    """
    # Initialize the CrewAI workflow
    crew, researcher_tool, firecrawl_tool = setup_agents_and_tasks(query, breadth, depth)

    # Trigger the research process
    result = crew.kickoff()

    # Extract raw output from result
    raw_output = str(result)

    # Clean the markdown formatting from the output
    cleaned_output = clean_markdown(raw_output)

    # Create summary heading based on the query
    summary_text = f"Research Summary: {query}"

    # Generate PDF from the cleaned output
    pdf_path = create_pdf(summary_text, cleaned_output, extracted_links)

    # Read the PDF file in binary mode and encode in base64
    with open(pdf_path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')

    # Return cleaned text, binary PDF data, and base64-encoded PDF
    return cleaned_output, pdf_data, base64_pdf

