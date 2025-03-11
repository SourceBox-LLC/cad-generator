import streamlit as st
import os, time
import tempfile
from cad import generate_cad
import webbrowser

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
    
    # Autodesk Viewer button (placeholder)
    autodesk_web = st.button("Autodesk Viewer", type="primary")
    
    # Add some space and maybe a description
    st.write("Visualize your CAD models directly in the browser.")

    if autodesk_web:
        webbrowser.open("https://viewer.autodesk.com")
# Use the example prompt if selected (outside of columns to affect the form)
if "example_prompt" in st.session_state:
    prompt = st.session_state["example_prompt"]
    del st.session_state["example_prompt"]
