import pytesseract
from PIL import Image
import re

def extract_goods_description(image_path):
    """
    Extracts goods descriptions and appends structured keywords for clarity.
    """
    try:
        # Extract text
        text = pytesseract.image_to_string(Image.open(image_path))

        # Extract item descriptions with keywords
        pattern = r'(Tablebirds.*?Broiler|Starter|Finisher|Feed.*?Px)'
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Add contextual keywords
        if matches:
            goods_description = " ".join(matches)
            enriched_description = f"{goods_description} Animal Feed Poultry Feed"
        else:
            enriched_description = "Animal Feed Poultry Feed"

        print("Filtered Goods Description:")
        print(enriched_description)
        return enriched_description.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None
