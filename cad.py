import os
import time
import streamlit as st

from kittycad.api.ml import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import Client
from kittycad.models import (
    ApiCallStatus,
    Error,
    FileExportFormat,
    TextToCad,
    TextToCadCreateBody,
)

def generate_cad(prompt: str, output_file: str = "output.step") -> str:
    """
    Generates a CAD file from a text prompt using the Zoo text-to-CAD API.
    """
    # Get API key exclusively from Streamlit secrets
    try:
        os.environ["ZOO_API_TOKEN"] = st.secrets["ZOO_API_KEY"]
    except (KeyError, AttributeError):
        raise ValueError("ZOO_API_KEY not found in Streamlit secrets. Please add it to .streamlit/secrets.toml")

    # Create client directly with API key instead of using environment variables
    client = Client(token=os.environ["ZOO_API_TOKEN"])
    
    # Determine file format from output file extension
    file_ext = os.path.splitext(output_file)[1].lstrip('.')
    if not file_ext:
        file_ext = "step"  # Default format
    
    # Convert file extension to FileExportFormat enum
    format_map = {
        "step": FileExportFormat.STEP,
        "stl": FileExportFormat.STL,
    }
    
    # Default to STEP if extension is not supported
    output_format = format_map.get(file_ext.lower(), FileExportFormat.STEP)

    # Show progress if in Streamlit
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Submitting your design prompt to the API...")
    except:
        progress_bar = None
        status_text = None
    
    # Prompt the API to generate a 3D model from text
    response = create_text_to_cad.sync(
        client=client,
        output_format=output_format,
        body=TextToCadCreateBody(
            prompt=prompt,
        ),
    )

    if isinstance(response, Error) or response is None:
        raise Exception(f"Error: {response}")

    result: TextToCad = response

    # Polling to check if the task is complete
    poll_count = 0
    max_polls = 60  # Maximum number of polls (5 min at 5 sec intervals)
    
    while result.completed_at is None:
        if status_text:
            status_text.text(f"Generating your CAD model... (this may take a minute)")
        
        if progress_bar:
            progress = min(0.9, poll_count / max_polls)
            progress_bar.progress(progress)
            
        # Wait for 5 seconds before checking again
        time.sleep(5)
        poll_count += 1
        
        if poll_count >= max_polls:
            raise Exception("CAD generation timed out after 5 minutes")

        # Check the status of the task
        response = get_text_to_cad_model_for_user.sync(
            client=client,
            id=result.id,
        )

        if isinstance(response, Error) or response is None:
            raise Exception(f"Error: {response}")

        result = response

    if progress_bar:
        progress_bar.progress(1.0)
        
    if status_text:
        status_text.text("CAD model completed! Preparing download...")

    if result.status == ApiCallStatus.FAILED:
        # Print out the error message
        raise Exception(f"Text-to-CAD failed: {result.error}")

    elif result.status == ApiCallStatus.COMPLETED:
        if result.outputs is None:
            raise Exception("Text-to-CAD completed but returned no files.")

        # Get the source file with the correct extension
        output_key = f"source.{file_ext.lower()}"
        if output_key not in result.outputs:
            # Fallback to any available output
            if not result.outputs:
                raise Exception("No output files available")
            output_key = next(iter(result.outputs))

        final_result = result.outputs[output_key]
        
        # Save the data
        with open(output_file, "w", encoding="utf-8") as output_file_handle:
            output_file_handle.write(final_result.decode("utf-8"))
    
    return output_file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a CAD file from a text prompt using the Zoo text-to-CAD API."
    )
    parser.add_argument("prompt", type=str, help="Text prompt describing the design for the CAD file.")
    parser.add_argument("-o", "--output", type=str, default="output.step", help="Output file path for the generated CAD file.")
    args = parser.parse_args()

    try:
        result_path = generate_cad(args.prompt, args.output)
        print(f"CAD file successfully generated and saved to: {result_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
