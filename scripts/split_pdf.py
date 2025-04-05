import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, chunk_size):
    """
    Splits the input PDF into multiple PDFs, each containing up to chunk_size pages.
    
    Parameters:
        input_pdf_path (str): Path to the input PDF file.
        chunk_size (int): Maximum number of pages per chunk.
    """
    # Open the input PDF file
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    # Determine the base name for the output files
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    
    # Process in chunks
    for start in range(0, total_pages, chunk_size):
        writer = PdfWriter()
        end = min(start + chunk_size, total_pages)
        
        # Add pages to the writer
        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])
        
        # Define the output filename
        chunk_number = start // chunk_size + 1
        output_filename = f"{base_name}_chunk_{chunk_number}.pdf"
        
        # Write out the chunk PDF
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Created: {output_filename} (pages {start + 1} to {end})")

def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF into chunks of specified number of pages (default 300)."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=300,
        help="Number of pages per chunk (default is 300)",
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_pdf):
        print(f"Error: The file '{args.input_pdf}' does not exist.")
        return
    
    split_pdf(args.input_pdf, args.chunk_size)

if __name__ == "__main__":
    main()
