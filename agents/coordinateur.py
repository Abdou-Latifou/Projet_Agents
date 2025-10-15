from agents.chercheur import Chercheur
from agents.analyste import Analyste
from agents.redacteur import Redacteur
from agents.assistant import Assistant
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Coordinateur:
    def __init__(self):
        self.chercheur = Chercheur()
        self.analyste = Analyste()
        self.redacteur = Redacteur()
        self.assistant = Assistant()

    def executer(self):
        try:
            logging.info("Démarrage de la recherche d'offres...")
            offres_brutes = self.chercheur.rechercher_offres()
            logging.info(f"{len(offres_brutes)} offres brutes collectées")

            offres_filtrees = self.analyste.analyser_offres(offres_brutes)
            logging.info(f"{len(offres_filtrees)} offres filtrées")

            # Vérifier offres non envoyées
            offres_a_envoyer = [o for o in offres_filtrees if self.assistant.verifier_offre_envoyee(o)]
            if not offres_a_envoyer:
                logging.info("Aucune nouvelle offre à envoyer")
                return

            email_content = self.redacteur.generer_email(offres_a_envoyer)
            self.assistant.envoyer_email(email_content)
            self.assistant.archiver_offres(offres_a_envoyer)
            logging.info("Processus terminé avec succès")
        except Exception as e:
            logging.error(f"Erreur fatale: {e}")

if __name__ == "__main__":
    coord = Coordinateur()
    coord.executer()  # Pour tester immédiatement