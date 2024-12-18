import sys
import os

# Add the 'src' directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr import extract_goods_description
from src.parse_pdf import parse_tariff_pdf, download_tariff_pdf
from src.hs_code_matcher import match_goods_to_hs_code

def main():
    # Step 1: Extract Goods Description using OCR
    print("Step 1: Extracting Goods Description...")
    invoice_path = "data/sample_invoice.png"  # Replace with your invoice image path
    goods_description = extract_goods_description(invoice_path)
    if not goods_description:
        print("No goods description found. Exiting...")
        return

    # Step 2: Download and Parse Customs Tariff PDF
    print("Step 2: Downloading and Parsing PNG Customs Tariff PDF...")
    pdf_url = "https://customs.gov.pg/pdf/pages/HS%202022%20Import%20&%20Export%20Tariff%20Act.pdf"
    local_pdf_path = "data/customs_tariff.pdf"

    if not os.path.exists("data"):
        os.makedirs("data")

    download_tariff_pdf(pdf_url, local_pdf_path)
    tariff_lines = parse_tariff_pdf(local_pdf_path)

    if not tariff_lines:
        print("No tariff data found. Exiting...")
        return

    # Step 3: Match Goods Description to HS Codes
    print("Step 3: Matching Goods Description to HS Codes...")
    best_match, confidence = match_goods_to_hs_code(goods_description, tariff_lines)

    # Step 4: Display Results
    print("\n--- Matching Result ---")
    print(f"Goods Description: {goods_description}")
    print(f"Best HS Code Match: {best_match}")
    print(f"Confidence Score: {confidence:.2f}")

if __name__ == "__main__":
    main()
