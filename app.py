import streamlit as st
import os, time
import tempfile
from cad import generate_cad






with st.sidebar:
    st.image("logo.png")
    
    # Add CSS for circular border around the image
    st.markdown("""
        <style>
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            border-radius: 50%;           /* Makes the image circular */
            border: 3px solid #4CAF50;    /* Adds a 3px solid green border */
            padding: 5px;                 /* Optional: adds space between image and border */
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); /* Optional: adds shadow for depth */
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.link_button("Project CADIA", "https://projectcadia.com")

    
    st.title("Welcome to the Project CADIA CAD Generator")
    st.write("This is a simple tool to generate CAD models from natural language descriptions.")
    st.markdown("---")
    st.markdown("""
    **Quick Docs:**
    - Use the text input to describe the CAD design you want to generate.
    - Use the output format dropdown to select the format of the CAD file you want to generate.
    - Use the output file name input to name the CAD file you want to generate.
    - Use the generate CAD button to generate the CAD file.
    - You can view your downloaded CAD file online via the Autodesk Viewer by clicking the "Autodesk Viewer" button. or any viewer and editor of your choice.
    
    for more information on the CADIA API, please visit the [CADIA API Documentation](https://github.com/SourceBox-LLC/cad-generator)
    """)




# Create two main columns for the app layout
left_col, right_col = st.columns([2, 1])  # 2:1 ratio gives more space to the CAD generator

# LEFT COLUMN - Text to CAD Generator
with left_col:
    st.title("Text to CAD Generator")
    st.write("Enter a description and generate a CAD file using Zoo's text-to-CAD API")

    # Create a form for the CAD generation
    with st.form("cad_form"):
        # Text input for the CAD description
        prompt = st.text_area("Describe the CAD design you want to generate", 
                            placeholder="Example: a gear with 20 teeth",
                            height=100)
        
        # File name input with default - only offer supported formats
        # Remove 'dxf' which isn't supported by the FileExportFormat enum
        output_format = st.selectbox("Output format", ["step", "stl"], index=0)
        file_name = st.text_input("Output file name (without extension)", "my_design")
        
        # Submit button
        submit_button = st.form_submit_button("Generate CAD")

    # Process the form submission
    if submit_button and prompt:
        try:
            st.info("Generating CAD file from your description...")
            
            # Create a temporary file to store the CAD output
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmp_file:
                output_path = tmp_file.name
            
            # Generate the CAD file
            generate_cad(prompt, output_path)
            
            # Read the generated file for download
            with open(output_path, "rb") as file:
                file_content = file.read()
            
            # Success message
            st.success(f"CAD file successfully generated!")
            
            # Create a download button
            final_filename = f"{file_name}.{output_format}"
            st.download_button(
                label="Download CAD File",
                data=file_content,
                file_name=final_filename,
                mime="application/octet-stream"
            )
            
            # Clean up temporary file
            os.unlink(output_path)
            
            # Display some example rendering or info
            st.write("### Your CAD design is ready!")
            st.write(f"Description: {prompt}")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Please check your API key in .streamlit/secrets.toml and try again.")

    # Add some example prompts to try
    with st.expander("Example prompts to try"):
        examples = [
            "A gear with 20 teeth",
            "A simple cube with a hole in the center",
            "A coffee mug with handle",
            "A screwdriver with phillips head",
            "A simple wrench"
        ]
        
        for example in examples:
            st.markdown(f"**{example}**")

# RIGHT COLUMN - View Files Section
with right_col:
    st.title("View Files (Autodesk)")
    
    # Replace webbrowser with Streamlit's link_button
    st.link_button("Autodesk Viewer", "https://viewer.autodesk.com", type="primary")
    
    # Add some space and maybe a description
    st.write("Visualize your CAD models directly in the browser.")

# Use the example prompt if selected (outside of columns to affect the form)
if "example_prompt" in st.session_state:
    prompt = st.session_state["example_prompt"]
    del st.session_state["example_prompt"]
