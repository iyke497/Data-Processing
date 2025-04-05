import os
from mistralai import Mistral

# Set your Mistral API key
api_key = "AuZsE8zHXlghWoZYLWJmMso8RFHTTQJq"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# List of document URLs
documents = [
    "https://www.dropbox.com/scl/fi/ndafw269y159gtc1dp96p/2025_act_chunk_1.pdf?rlkey=7thmz47mjqii290xrhi3bjvjz&st=v79h3dyn&dl=1",
    "https://www.dropbox.com/scl/fi/bo1bdwc72lwrbce1kn1m9/2025_act_chunk_2.pdf?rlkey=j4ui7kprqm3eel2u53xwu5z97&st=nernek73&dl=1",
    "https://www.dropbox.com/scl/fi/f1he0y9tkk5hk3yu2i7t2/2025_act_chunk_3.pdf?rlkey=c5463h72n77jf134t2iozrd6g&st=j936cjqk&dl=1",
    "https://www.dropbox.com/scl/fi/5unot6pqeyk0le0hxv814/2025_act_chunk_4.pdf?rlkey=d2em7ls2exhl19sp5yx5f5tz0&st=x7djosqy&dl=1",
    "https://www.dropbox.com/scl/fi/jsoao019ajlwckdwuutwj/2025_act_chunk_5.pdf?rlkey=6d1hmk25atk75f1j7h4ozsbri&st=h2deazkq&dl=1"
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
        output_file = f"2025_act_chunk_{index}.md"
        
        # Write results to markdown file
        with open(output_file, "w", encoding="utf-8") as md_file:
            for page in ocr_response.pages:
                md_file.write(page.markdown + "\n\n")
        
        print(f"Successfully processed chunk {index} -> {output_file}")

    except Exception as e:
        print(f"Error processing chunk {index}: {str(e)}")