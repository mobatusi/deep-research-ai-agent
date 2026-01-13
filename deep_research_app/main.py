import os
# Disable CrewAI telemetry to avoid signal handler errors in Streamlit
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY"] = "false"

import streamlit as st
from controllers.research_controller import run_deep_research
import base64


# Set page configuration
st.set_page_config(page_title="Deep Research AI Agent", layout="wide")

# Page title and instructions
st.title("🔍 Deep Research AI Agent")

st.markdown("""
### Welcome to the Deep Research Tool!

This AI-powered research assistant uses CrewAI agents to conduct comprehensive web research on any topic.

**How it works:**
1. Enter your research query below
2. Adjust the breadth (number of sources) and depth (recursion level) parameters
3. Click "Run Deep Research" to start the AI agents
4. View and download your professional research report

**Note:** This app uses the Firecrawl API for web research. If results seem unclear or incomplete,
try rerunning the research or rephrasing your query. For more accurate output, consider using
paid tools like SerpAPI or Tavily.
""")

st.divider()

# Input section
st.subheader("📝 Research Configuration")

# Text input for research query
query = st.text_input(
    "Enter your research query:",
    placeholder="e.g., Latest developments in quantum computing",
    help="Enter the topic or question you want to research"
)

# Create two columns for sliders
col1, col2 = st.columns(2)

with col1:
    # Breadth slider (1-10)
    breadth = st.slider(
        "Breadth (Number of Sources)",
        min_value=1,
        max_value=10,
        value=3,
        help="Controls how many different sources or subtopics to explore"
    )

with col2:
    # Depth slider (1-5)
    depth = st.slider(
        "Depth (Recursion Level)",
        min_value=1,
        max_value=5,
        value=2,
        help="Controls how thoroughly to investigate each source"
    )

st.divider()

# Run Deep Research button
if st.button("🚀 Run Deep Research", type="primary", use_container_width=True):
    # Validate query
    if not query or query.strip() == "":
        st.error("⚠️ Please enter a research query before running the research.")
    else:
        # Show spinner while processing
        with st.spinner("🤖 AI agents are researching your query... This may take a few minutes."):
            try:
                # Call the research function
                cleaned_output, pdf_data, base64_pdf = run_deep_research(query, breadth, depth)

                # Show success message
                st.success("✅ Research completed successfully!")

                st.divider()

                # Display results section
                st.subheader("📊 Research Results")

                # Preview of cleaned report
                st.text_area(
                    "Research Report Preview:",
                    value=cleaned_output,
                    height=400,
                    help="This is the cleaned, formatted version of your research report"
                )

                # Create two columns for download and preview
                col1, col2 = st.columns([1, 1])

                with col1:
                    # Download button for PDF
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=f"research_report_{query[:30].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col2:
                    # Display PDF inline (optional preview)
                    st.markdown("**PDF Preview:**")

                # Inline PDF viewer
                st.markdown("### 📄 PDF Report Viewer")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred during research: {str(e)}")
                st.exception(e)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Powered by CrewAI, OpenAI, and Firecrawl | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

