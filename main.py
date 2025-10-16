from agents.coordinateur import Coordinateur
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

def main():
    coord = Coordinateur()
    scheduler = BlockingScheduler()
    scheduler.add_job(coord.executer, 'cron', hour=8, minute=0)  # Exécute chaque matin à 8h
    print("Système multi-agents démarré. En attente de l'exécution quotidienne...")
    #coord.executer()  # Ajoute ceci pour tester maintenant

    scheduler.start()

if __name__ == "__main__":
    coord = Coordinateur()
    coord.executer()  # Ajouté pour tester
    scheduler.start()