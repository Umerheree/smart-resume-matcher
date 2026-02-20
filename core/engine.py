# core/engine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import yaml

class MatchingEngine:
    def __init__(self, config_path="data/config.yaml"):
        # Load dynamic weights from config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.weights = self.config.get('scoring_weights', {})
        self.scaling = self.weights.get('scaling_factor', 400)

    def _get_jaccard_similarity(self, text1, text2):
        """Calculates set-based overlap."""
        set1, set2 = set(text1.split()), set(text2.split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return (intersection / union) if union != 0 else 0

    def run_tfidf_match(self, jd_text, resume_texts):
        """
        Production-grade TF-IDF matching with explainability.
        """
        documents = [jd_text] + resume_texts
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        jd_vector = tfidf_matrix[0]
        feature_names = vectorizer.get_feature_names_out()
        
        results = []
        for i in range(1, len(documents)):
            # 1. Cosine Similarity
            cos_score = cosine_similarity(jd_vector, tfidf_matrix[i])[0][0]
            
            # 2. Jaccard Similarity
            jac_score = self._get_jaccard_similarity(jd_text, documents[i])
            
            # 3. Weighted Blend from Config
            raw_avg = (cos_score * self.weights.get('cosine', 0.6)) + \
                      (jac_score * self.weights.get('jaccard', 0.4))
            
            # 4. Final Normalized Score
            final_score = min(round(raw_avg * self.scaling, 2), 100)

            # 5. Explainability: Top Contributing Keywords
            # Find words in this resume with highest TF-IDF weight matching the JD
            row = tfidf_matrix[i].toarray().flatten()
            top_indices = row.argsort()[-5:][::-1]
            keywords = [feature_names[idx] for idx in top_indices if row[idx] > 0]

            results.append({
                "score": final_score,
                "keywords": keywords,
                "raw_cosine": cos_score
            })
            
        return results