import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

class Chercheur:
    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.sites = [
            "https://emploitogo.info",
            "https://www.emploi.tg",
            "https://www.emploi.tg",
            "https://anpetogo.org",
            "https://www.rmo-jobcenter.com/fr/togo/offres-emploi.html",
            "https://www.goafricaonline.com/tg/emploi",
            "https://www.linkedin.com/jobs/search/?keywords=tech&location=Togo"
        ]

    def rechercher_offres(self):
        offres = []
        query = "offres d'emploi tech Togo 2025"

        # Recherche via Tavily
        try:
            results = self.tavily.search(query=query, max_results=10)
            for result in results.get("results", []):
                offres.append({
                    "titre": result.get("title", ""),
                    "description": result.get("content", "")[:500],
                    "lien": result.get("url", ""),
                    "source": result.get("url", "").split("/")[2]
                })
        except Exception as e:
            print(f"Erreur Tavily: {e}")

        # Scraping des sites togolais
        for site in self.sites:
            try:
                response = requests.get(site, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                job_elements = soup.find_all(['h2', 'h3', 'a', 'div'], class_=['job', 'offre', 'listing'])
                for job in job_elements[:5]:  # Limiter à 5 par site
                    titre = job.get_text(strip=True) or "Sans titre"
                    lien = job.get('href', '') if job.name == 'a' else ''
                    if lien and not lien.startswith('http'):
                        lien = site + lien
                    offres.append({
                        "titre": titre,
                        "description": "Description non disponible",
                        "lien": lien,
                        "source": site.split("/")[2]
                    })
            except Exception as e:
                print(f"Erreur scraping {site}: {e}")

        return offres