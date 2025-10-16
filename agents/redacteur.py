from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv

load_dotenv()

class Redacteur:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("templates"))

    def generer_email(self, offres):
        summaries = [
            {
                "titre": offre["titre"],
                "entreprise": offre.get("source", "Non spécifié"),
                "resume": f"{offre['description'][:150]}... (Score de pertinence : {offre.get('score_pertinence', 0):.2f})",
                "lien": offre["lien"]
            } for offre in offres
        ]
        
        template = self.env.get_template("email_template.html")
        email_content = template.render(offres=summaries, date="2025-10-15")
        return email_content