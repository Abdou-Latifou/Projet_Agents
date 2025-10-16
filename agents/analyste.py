#from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

class Analyste:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Gardé pour futur usage

    def analyser_offres(self, offres):
        # Keywords élargis pour matcher les offres togolaises
        tech_keywords = [
            "informatique", "developpeur", "développeur", "data", "software", "technologie", "devops", "reseau", "réseau",
            "tech", "it", "programmeur", "ntic", "telecommunications", "télécommunications", "flutter", "javascript",
            "node", "digital", "web", "mobile", "fullstack", "analyst", "scientist", "engineer", "sig", "infrastructure"
        ]
        
        print(f"Analyse locale de {len(offres)} offres brutes avec keywords tech...")
        filtered = []
        seen = set()
        for offre in offres:
            titre_lower = offre["titre"].lower()
            desc_lower = offre["description"].lower()
            if any(kw.lower() in titre_lower or kw.lower() in desc_lower for kw in tech_keywords):
                key = (titre_lower[:50], desc_lower[:100])  # Clé pour dédoublonnage
                if key not in seen:
                    seen.add(key)
                    offre["score_pertinence"] = min(1.0, 0.5 + 0.1 * len([kw for kw in tech_keywords if kw.lower() in titre_lower or kw.lower() in desc_lower]))  # Score dynamique
                    filtered.append(offre)
        
        filtered_sorted = sorted(filtered, key=lambda x: x.get("score_pertinence", 0), reverse=True)[:5]
        print(f"{len(filtered_sorted)} offres tech filtrées par analyse locale.")
        return filtered_sorted