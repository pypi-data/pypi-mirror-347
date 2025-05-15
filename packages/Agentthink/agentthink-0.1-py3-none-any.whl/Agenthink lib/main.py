import os
import io
import requests  # for fetching the blob if needed
from pathlib import Path


def fetch_data_from_blob(blob_url: str):
    """Fetch data from Azure Blob Storage or other sources."""
    response = requests.get(blob_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch data from {blob_url}, Status Code: {response.status_code}")


def convert_to_binary(data: bytes):
    """Convert the input data to binary and save it in a temporary location."""
    temp_path = Path("tempdata") / "input_file.bin"
    temp_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the tempdata folder exists

    with open(temp_path, "wb") as temp_file:
        temp_file.write(data)

    return temp_path


def process_input(blob_url: str):
    """Process input from the blob URL and prepare it for model."""
    data = fetch_data_from_blob(blob_url)
    binary_file_path = convert_to_binary(data)

    return binary_file_path
