from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_jaccard_similarity(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return (intersection / union) if union != 0 else 0

def normalize_score(raw_score):
    """
    Scales a raw similarity score (usually 0.0 to 0.4) to a percentage (0 to 100).
    We assume a raw score of 0.25 (25% overlap) is a 'Perfect' 100% match for resumes.
    """
    # Scaling factor: if raw score is 0.2, result is 0.2 * 400 = 80%
    # We cap it at 100% so it doesn't go over.
    scaled_score = raw_score * 400 
    return min(round(scaled_score, 2), 100)

def calculate_match(job_description, resumes_text):
    # 1. Cosine Similarity
    documents = [job_description] + resumes_text
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    jd_vector = tfidf_matrix[0]
    
    results = []
    
    # Loop through resumes
    for i in range(1, len(documents)):
        resume_text = documents[i]
        
        # Raw Cosine (0.0 - 1.0)
        cosine_raw = cosine_similarity(jd_vector, tfidf_matrix[i])[0][0]
        
        # Raw Jaccard (0.0 - 1.0)
        jaccard_raw = get_jaccard_similarity(job_description, resume_text)
        
        # Weighted Average (60% Cosine, 40% Jaccard)
        avg_raw = (cosine_raw * 0.6) + (jaccard_raw * 0.4)
        
        # SCALE IT UP for human readability
        final_score = normalize_score(avg_raw)
        
        results.append({
            "cosine": round(cosine_raw, 4),
            "jaccard": round(jaccard_raw, 4),
            "total": final_score  # (0-100)
        })
        
    return results