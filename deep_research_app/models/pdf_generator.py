from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import tempfile

def create_pdf(summary: str, content: str, links: list) -> str:
    """
    Generate a PDF report using reportlab with consistent layout.

    Args:
        summary: Brief summary or heading for the report
        content: Cleaned research findings as text
        links: List of URLs used during research

    Returns:
        str: Path to the generated temporary PDF file
    """
    # Create a temporary PDF file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_file.name
    temp_file.close()

    # Initialize PDF document with letter page size and margins
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    # Get default styles
    styles = getSampleStyleSheet()
    story = []

    # Add report title
    title = Paragraph("Research Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3 * inch))

    # Add summary section
    summary_heading = Paragraph("Summary", styles['Heading1'])
    story.append(summary_heading)
    story.append(Spacer(1, 0.2 * inch))

    summary_text = Paragraph(summary, styles['BodyText'])
    story.append(summary_text)
    story.append(Spacer(1, 0.3 * inch))

    # Add content section
    content_heading = Paragraph("Research Findings", styles['Heading1'])
    story.append(content_heading)
    story.append(Spacer(1, 0.2 * inch))

    # Process content lines
    content_lines = content.split('\n')
    for line in content_lines:
        # Skip empty lines
        if line.strip():
            # Add each valid line as a paragraph
            paragraph = Paragraph(line, styles['BodyText'])
            story.append(paragraph)
            story.append(Spacer(1, 0.1 * inch))

    # Add sources/links section
    if links:
        story.append(Spacer(1, 0.2 * inch))
        links_heading = Paragraph("Sources", styles['Heading1'])
        story.append(links_heading)
        story.append(Spacer(1, 0.2 * inch))

        for link in links:
            if link.strip():
                link_paragraph = Paragraph(f"• {link}", styles['BodyText'])
                story.append(link_paragraph)
                story.append(Spacer(1, 0.1 * inch))

    # Build the PDF document
    doc.build(story)

    return pdf_path

