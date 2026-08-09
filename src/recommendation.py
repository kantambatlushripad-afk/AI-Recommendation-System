from typing import List, Dict
from .similarity import cosine_similarity, jaccard_similarity, euclidean_similarity, pearson_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
import numpy as np

class RecommendationSystem:
    def __init__(self, items: List[Dict]):
        self.items = items
        self._init_tfidf()

    def _init_tfidf(self):
        contents = []
        for item in self.items:
            title = item.get("title", "")
            category = item.get("category", "")
            description = item.get("description", "")
            tags = " ".join(item.get("tags", []))
            content = f"{title} {category} {description} {tags}"
            contents.append(content)

        if contents:
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(contents)
        else:
            self.vectorizer = None
            self.tfidf_matrix = None

    def recommend(self, user_profile: Dict, algorithm: str = "cosine", top_n: int = 5) -> List[Dict]:
        recommendations = []
        
        if algorithm == "tfidf" and self.vectorizer is not None:
            query_parts = []
            query_parts.extend(user_profile.get("categories", []))
            query_parts.extend(user_profile.get("topics", []))
            query = " ".join(query_parts)
            
            if not query.strip():
                for item in self.items:
                    recommendations.append({
                        "item": item, 
                        "score": 0.0,
                        "explanation": "No preference interests selected."
                    })
            else:
                user_vector = self.vectorizer.transform([query])
                sims = sklearn_cosine_similarity(user_vector, self.tfidf_matrix).flatten()
                for i, item in enumerate(self.items):
                    recommendations.append({
                        "item": item,
                        "score": round(float(sims[i]), 4),
                        "explanation": self._generate_explanation(user_profile, item)
                    })
        else:
            user_vector = self._build_user_vector(user_profile)
            for item in self.items:
                item_vector = self._build_item_vector(item)
                
                if algorithm == "jaccard":
                    score = jaccard_similarity(user_vector, item_vector)
                elif algorithm == "euclidean":
                    score = euclidean_similarity(user_vector, item_vector)
                elif algorithm == "pearson":
                    score = pearson_similarity(user_vector, item_vector)
                else:
                    score = cosine_similarity(user_vector, item_vector)
                    
                recommendations.append({
                    "item": item,
                    "score": round(float(score), 4),
                    "explanation": self._generate_explanation(user_profile, item)
                })

        recommendations.sort(key=lambda x: (x["score"], x["item"].get("rating", 0.0)), reverse=True)
        return recommendations[:top_n]

    def _generate_explanation(self, user_profile: Dict, item: Dict) -> str:
        pref_categories = user_profile.get("categories", [])
        pref_topics = user_profile.get("topics", [])
        
        matched_cat = item["category"] in pref_categories
        matched_tags = set(item.get("tags", [])) & set(pref_topics)
        
        if matched_cat and matched_tags:
            return f"Matches category '{item['category']}' and topic(s): {', '.join(sorted(matched_tags))}."
        elif matched_cat:
            return f"Matches category '{item['category']}'."
        elif matched_tags:
            return f"Matches topic(s): {', '.join(sorted(matched_tags))}."
        else:
            return f"Suggested based on general item attributes (Rating: {item.get('rating', 0.0)})."

    def _build_user_vector(self, user_profile: Dict) -> Dict[str, float]:
        vector = {}
        for category in user_profile.get("categories", []):
            vector[f"category::{category}"] = vector.get(f"category::{category}", 0.0) + 1.0
        for topic in user_profile.get("topics", []):
            vector[f"tag::{topic}"] = vector.get(f"tag::{topic}", 0.0) + 1.0
        return vector

    def _build_item_vector(self, item: Dict) -> Dict[str, float]:
        vector = {}
        vector[f"category::{item['category']}"] = 1.0
        for tag in item.get("tags", []):
            vector[f"tag::{tag}"] = 1.0
        return vector
