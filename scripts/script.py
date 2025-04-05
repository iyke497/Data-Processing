import os
from mistralai import Mistral

# Set your Mistral API key
api_key = os.environ["MISTRAL_API_KEY"]

# Initialize the Mistral client
client = Mistral(api_key=api_key)

chunk_1 = "https://www.dropbox.com/scl/fi/9qr5s1g72xosximbbs3jh/2025_chunk_1_ocr_ready.pdf?rlkey=q2fb1i5cnukftpgbx3xkavcrb&st=ihd28tec&dl=1"
chunk_2 = "https://www.dropbox.com/scl/fi/oqdo19nyhme32bwsgki3w/2025_chunk_2_ocr_ready.pdf?rlkey=6m6znvkqje8og3466bfvhf2ob&st=pvu3v32j&dl=1"
chunk_3 = "https://www.dropbox.com/scl/fi/sgazpyg8ffcddp7j18281/2025_chunk_3_ocr_ready.pdf?rlkey=e1bhlh0r6tei0tw2slxbdy8jo&st=bcrgsv0e&dl=1"
chunk_4 = "https://www.dropbox.com/scl/fi/otn4bgz5agpm7p05l7d99/2025_chunk_4_ocr_ready.pdf?rlkey=03lodblptlixklwfx18m6vfrk&st=3jmzxxwe&dl=1"
chunk_5 = "https://www.dropbox.com/scl/fi/7l46asyejli26le94pjaz/2025_chunk_5_ocr_ready.pdf?rlkey=kvyuzo2jhfsf61ksbar2tf3oz&st=gdwsloh7&dl=1"


# Process the pdf file using the shareable link
ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": "YOUR_DOCUMENT_URL_HERE"
    },
    include_image_base64=True
)

# Access the pages attribute using dot notation
for page in ocr_response.pages:
    print(page.markdown)
