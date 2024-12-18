from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_goods_to_hs_code(goods_description, tariff_lines):
    """
    Matches goods description to HS codes with strict filtering for Chapter 23.
    """
    try:
        # Step 1: Pre-filter tariff lines for Chapter 23 and keywords
        keywords = ['feed', 'meal', 'animal', 'preparations', 'residues', 'poultry']
        filtered_tariffs = [
            line for line in tariff_lines
            if any(word.lower() in line.lower() for word in keywords) and "23" in line[:3]  # Focus on Chapter 23
        ]

        if not filtered_tariffs:
            print("No Chapter 23-related tariff lines found. Defaulting to broader list.")
            filtered_tariffs = tariff_lines  # Fallback to all tariff lines

        # Step 2: Match using NLP
        description_embedding = model.encode([goods_description])
        tariff_embeddings = model.encode(filtered_tariffs)
        similarities = cosine_similarity(description_embedding, tariff_embeddings)[0]

        best_match_index = similarities.argmax()
        return filtered_tariffs[best_match_index], similarities[best_match_index]
    except Exception as e:
        print(f"Error matching HS code: {e}")
        return None, 0
