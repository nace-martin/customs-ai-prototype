import requests
import pdfplumber
import os

def download_tariff_pdf(url, save_path):
    """
    Downloads the PNG Customs Tariff Act PDF from the provided URL.
    :param url: The URL to the PDF file.
    :param save_path: Local path to save the downloaded PDF.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print("PDF downloaded successfully.")
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

def parse_tariff_pdf(pdf_path):
    """
    Parses the PNG Customs Tariff Act PDF and extracts text line by line.
    :param pdf_path: Path to the PDF file.
    :return: List of extracted text lines.
    """
    tariff_entries = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    tariff_entries.extend(text.splitlines())
        print("PDF parsed successfully.")
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return tariff_entries

if __name__ == "__main__":
    # Step 1: Download PDF
    pdf_url = "https://customs.gov.pg/pdf/pages/HS%202022%20Import%20&%20Export%20Tariff%20Act.pdf"
    local_pdf_path = "data/customs_tariff.pdf"

    # Create data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    download_tariff_pdf(pdf_url, local_pdf_path)

    # Step 2: Parse PDF
    tariff_lines = parse_tariff_pdf(local_pdf_path)

    # Step 3: Print sample lines
    print("Sample Tariff Lines:")
    for line in tariff_lines[:10]:  # Display first 10 lines
        print(line)
