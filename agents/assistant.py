import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self):
        self.conn = sqlite3.connect("offres.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS offres_envoyees (
                titre TEXT,
                lien TEXT,
                date_envoi TEXT,
                PRIMARY KEY (titre, lien)
            )
        """)
        self.conn.commit()

    def envoyer_email(self, email_content):
        msg = MIMEMultipart()
        msg["From"] = os.getenv("GMAIL_USER")
        msg["To"] = os.getenv("RECIPIENT_EMAIL")
        msg["Subject"] = "Offres d'emploi Tech au Togo - Quotidien"
        msg.attach(MIMEText(email_content, "html"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASSWORD"))
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            server.quit()
            print("Email envoyé avec succès")
        except Exception as e:
            print(f"Erreur envoi email: {e}")

    def archiver_offres(self, offres):
        for offre in offres:
            try:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO offres_envoyees (titre, lien, date_envoi) VALUES (?, ?, ?)",
                    (offre["titre"], offre["lien"], "2025-10-15")
                )
            except Exception as e:
                print(f"Erreur archivage: {e}")
        self.conn.commit()

    def verifier_offre_envoyee(self, offre):
        self.cursor.execute(
            "SELECT 1 FROM offres_envoyees WHERE titre = ? AND lien = ?",
            (offre["titre"], offre["lien"])
        )
        return self.cursor.fetchone() is None