import streamlit as st
import os, time
import tempfile
from cad import generate_cad

# Set page configuration
st.set_page_config(
    page_title="Project CADIA - CAD Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the entire application
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Custom headers */
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h1 {
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
    }
    
    /* Form styling */
    .stTextArea textarea, .stSelectbox, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-size: 16px;
    }
    
    .stTextArea textarea:focus, .stSelectbox:focus, .stTextInput input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
    }
    
    /* Button styling */
    .stButton button, .stDownloadButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stButton button:hover, .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .stButton button[data-baseweb="button"] {
        background-color: #3B82F6;
        color: white;
        border: none;
    }
    
    /* Card-like containers */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Status messages */
    .info-box, .success-box, .error-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    }
    
    .info-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
    }
    
    .success-box {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
    }
    
    .error-box {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
    }
    
    /* Example prompts */
    .example-prompt {
        background-color: #F9FAFB;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid #CBD5E1;
        color: #1F2937 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .example-prompt:hover {
        background-color: #F3F4F6;
        border-left-color: #3B82F6;
    }
    
    /* Make the example prompt buttons more attractive */
    [data-testid="baseButton-secondary"] {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: #BAE6FD !important;
        color: #0284C7 !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
        color: #6B7280;
        font-size: 0.875rem;
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A;
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        border-radius: 50%;
        border: 4px solid #3B82F6;
        padding: 4px;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 1.5rem 0;
    }
    
    /* Emphasize important elements */
    .highlight {
        font-weight: 600;
        color: #1E3A8A;
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.image("logo.png", width=150)
    
    st.title("Project CADIA")
    st.markdown("##### CAD Generator")
    
    st.link_button("Visit Project CADIA", "https://projectcadia.com", use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### How it works")
    st.markdown("""
    1. **Describe** your CAD design in natural language
    2. **Generate** a 3D model from your description
    3. **Download** your CAD file in your preferred format
    4. **View or Edit** using Autodesk Viewer or your preferred CAD software
    """)
    
    st.markdown("---")
    
    st.markdown("### Documentation")
    
    with st.expander("Quick Guide", expanded=False):
        st.markdown("""
        - Use descriptive language for better results
        - Choose between STL or STEP formats
        - Name your files meaningfully
        - Generation typically takes 1-2 minutes
        """)
    
    with st.expander("API Information", expanded=False):
        st.markdown("""
        This application uses the Zoo text-to-CAD API to generate 3D models from natural language descriptions.
        
        [View CADIA API Documentation](https://github.com/SourceBox-LLC/cad-generator)
        """)
        
    st.markdown("---")
    
    # Footer in sidebar
    st.markdown("""
    <div style="opacity: 0.7; font-size: 0.8rem; text-align: center; padding-top: 20px;">
        © 2023 Project CADIA<br>
        Powered by Zoo's text-to-CAD API
    </div>
    """, unsafe_allow_html=True)

# Main page header
st.markdown("""
<div style="text-align: center; padding: 1rem 0 2rem 0;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Text to CAD Generator</h1>
    <p style="font-size: 1.2rem; color: #4B5563; max-width: 800px; margin: 0 auto;">
        Transform your ideas into 3D models with AI-powered text-to-CAD technology
    </p>
</div>
""", unsafe_allow_html=True)

# Create containers for main sections
input_container = st.container()
result_container = st.container()

# Input Section
with input_container:
    left_col, right_col = st.columns([3, 1])
    
    with left_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown("### Create Your 3D Model")
        st.markdown("Describe in detail what you want to generate")
        
        # Create a form for the CAD generation
        with st.form("cad_form"):
            # Text input for the CAD description
            prompt = st.text_area(
                "Describe the CAD design you want to generate", 
                value=st.session_state.get("form_prompt", ""),  # Use the stored prompt if available
                placeholder="Example: A gear with 20 teeth, 5mm thick, with a 10mm center hole",
                height=120
            )
            
            # Add a hint about examples if no prompt has been entered yet
            if not prompt:
                st.info("💡 **Tip:** Not sure what to write? Check out the example prompts below the form!")
            
            # Create two columns for the form inputs
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                output_format = st.selectbox(
                    "Output format", 
                    ["step", "stl"], 
                    index=0,
                    help="STEP is better for precision engineering, STL for 3D printing"
                )
            
            with form_col2:
                file_name = st.text_input(
                    "Output file name (without extension)", 
                    "my_design",
                    help="Name your file without the extension"
                )
            
            # Submit button - full width and prominent
            submit_button = st.form_submit_button("🔄 Generate 3D Model")
        
        # Example prompts section with improved UI
        st.markdown("### Example Prompts")
        st.markdown("Select any example below to use it as your prompt:")
        
        # Add visual separator before examples
        st.markdown("<hr style='margin: 1rem 0; border-color: #E5E7EB;'>", unsafe_allow_html=True)
        
        # Function to set example prompt
        def set_example_prompt(prompt):
            st.session_state["example_prompt"] = prompt
            st.session_state["selected_example"] = prompt  # Store which example was selected
            st.rerun()
        
        examples = [
            "A gear with 20 teeth, 5mm thick, with a 10mm diameter center hole",
            "A simple cube with dimensions 20x20x20mm and a cylindrical hole of 10mm diameter through the center",
            "A coffee mug with a handle, 100mm tall and 80mm diameter, wall thickness of 3mm",
            "A screwdriver with phillips head, 150mm shaft length, and an ergonomic handle",
            "A wrench suitable for 15mm bolts with a comfortable grip"
        ]
        
        # Create a container for examples
        examples_container = st.container()
        
        # Display examples in a more reliable way
        for i, example in enumerate(examples):
            col1, col2 = examples_container.columns([5, 1])
            
            # Check if this example is currently selected
            is_selected = "selected_example" in st.session_state and st.session_state["selected_example"] == example
            
            # Apply different styling based on selection state
            border_style = "border-left: 3px solid #2563EB; background-color: #EFF6FF;" if is_selected else "border-left: 3px solid #CBD5E1;"
            
            with col1:
                st.markdown(f"""
                <div class="example-prompt" style="{border_style}">
                    <span class="highlight">Example {i+1}:</span> {example}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Use", key=f"example_{i}", use_container_width=True):
                    set_example_prompt(example)
            
            # Add a small vertical space between examples (except the last one)
            if i < len(examples) - 1:
                examples_container.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        # Add visual separator after examples
        st.markdown("<hr style='margin: 1.5rem 0 1rem 0; border-color: #E5E7EB;'>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column with viewer and information
    with right_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### View & Edit")
        st.markdown("Open your CAD files in Autodesk Viewer:")
        
        st.link_button(
            "🔍 Open Autodesk Viewer", 
            "https://viewer.autodesk.com", 
            type="primary",
            use_container_width=True
        )
        
        st.markdown("""
        **With Autodesk Viewer you can:**
        - View your 3D models in a browser
        - Rotate, zoom, and pan
        - Take measurements
        - Share with collaborators
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional information card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### File Formats")
        
        st.markdown("""
        **STEP (.step)**
        - Industry standard for CAD exchange
        - Preserves parametric features
        - Ideal for engineering workflows
        
        **STL (.stl)**
        - Standard for 3D printing
        - Simple mesh representation
        - Widely compatible
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Process the form submission
if submit_button and prompt:
    with result_container:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        try:
            # Custom info message
            st.markdown("""
            <div class="info-box">
                <div>
                    <h3 style="margin: 0; color: #1E40AF;">Generating your 3D model...</h3>
                    <p style="margin: 0.5rem 0 0 0;">This typically takes 1-2 minutes. Please wait while we process your request.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a temporary file to store the CAD output
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmp_file:
                output_path = tmp_file.name
            
            # Generate the CAD file
            generate_cad(prompt, output_path)
            
            # Read the generated file for download
            with open(output_path, "rb") as file:
                file_content = file.read()
            
            # Success message with custom styling
            st.markdown("""
            <div class="success-box">
                <div>
                    <h3 style="margin: 0; color: #065F46;">Success! Your 3D model is ready</h3>
                    <p style="margin: 0.5rem 0 0 0;">Your CAD file has been generated and is ready for download.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a download button
            final_filename = f"{file_name}.{output_format}"
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📥 Download CAD File",
                    data=file_content,
                    file_name=final_filename,
                    mime="application/octet-stream",
                    use_container_width=True,
                )
            
            with col2:
                st.link_button(
                    "🔍 View in Autodesk",
                    "https://viewer.autodesk.com",
                    use_container_width=True,
                )
            
            # Clean up temporary file
            os.unlink(output_path)
            
            # Display information about the generated design
            st.markdown("### Generated Design Details")
            st.markdown(f"**Description:** {prompt}")
            st.markdown(f"**Format:** {output_format.upper()}")
            st.markdown(f"**Filename:** {final_filename}")
            
            # Add tips for viewing/editing
            st.info("""
            **Next Steps:**
            1. Download your CAD file using the button above
            2. Open it in Autodesk Viewer or your preferred CAD software
            3. Make any necessary adjustments or refinements
            """)
            
        except Exception as e:
            # Error message with custom styling
            st.markdown(f"""
            <div class="error-box">
                <div>
                    <h3 style="margin: 0; color: #991B1B;">Error Generating CAD Model</h3>
                    <p style="margin: 0.5rem 0 0 0;">An error occurred during the generation process: {e}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **Troubleshooting Steps:**
            1. Check that your API key is correctly set in `.streamlit/secrets.toml`
            2. Verify your prompt is clear and descriptive
            3. Try again with a simpler description
            4. Contact support if the issue persists
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Project CADIA • Powered by Zoo's Text-to-CAD API • © 2023 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

# Use the example prompt if selected
if "example_prompt" in st.session_state:
    # Store the prompt value
    example_value = st.session_state["example_prompt"]
    
    # Clear the session state to prevent infinite loops
    del st.session_state["example_prompt"]
    
    # Set the prompt in a way that persists between reruns
    st.session_state["form_prompt"] = example_value
    
    # Rerun to apply the changes
    st.rerun()

# Pre-fill the form if we have a saved prompt
if "form_prompt" in st.session_state and not prompt:
    prompt = st.session_state["form_prompt"]
