import os
from mistralai import Mistral

# Set your Mistral API key
api_key = "AuZsE8zHXlghWoZYLWJmMso8RFHTTQJq"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# List of document URLs
documents = [
    "https://www.dropbox.com/scl/fi/3wltw6pljpko1izk2btz7/2025_chunk_1.pdf?rlkey=fi67f4lq4nku3v2yq82513pg3&st=8ngn7gwm&dl=1",
    "https://www.dropbox.com/scl/fi/ejiyqunid6zdo28iutesa/2025_chunk_2.pdf?rlkey=zmvm6taxjbwwjtsmzkc9hdt56&st=8fyznnx1&dl=1",
    "https://www.dropbox.com/scl/fi/i22z3wwhm2qfnfhibwb43/2025_chunk_3.pdf?rlkey=10acdiwxeol7hzks0o98ir2mv&st=hcpgp2v6&dl=1",
    "https://www.dropbox.com/scl/fi/aczyyl7e6cteyjfe3s9am/2025_chunk_4.pdf?rlkey=zcgvjcarizszzf6rl89saywf5&st=j8iho7k4&dl=1",
    "https://www.dropbox.com/scl/fi/w03vubttwbsf7zlch2k3x/2025_chunk_5.pdf?rlkey=6nrdxv8b3hmqofl5xwmqtsbmc&st=t88row4a&dl=1"
]

# Process each document in a loop
for index, document_url in enumerate(documents, start=1):
    try:
        print(f"Processing chunk {index}...")
        
        # Process the PDF using the current URL
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": document_url
            },
            include_image_base64=True
        )

        # Create output filename
        output_file = f"output_chunk_{index}.md"
        
        # Write results to markdown file
        with open(output_file, "w", encoding="utf-8") as md_file:
            for page in ocr_response.pages:
                md_file.write(page.markdown + "\n\n")
        
        print(f"Successfully processed chunk {index} -> {output_file}")

    except Exception as e:
        print(f"Error processing chunk {index}: {str(e)}")