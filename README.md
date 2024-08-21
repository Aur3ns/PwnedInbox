<h1 align="center">Project PwnInbox</h1>

Ce projet contient deux scripts Python permettant d'exécuter des commandes sur un système distant via des e-mails. Ils utilisent le protocole POP3 pour surveiller une boîte aux lettres Gmail spécifiée et exécuter les commandes contenues dans les e-mails reçus.

## 🚀 Fonctionnalités

- **Exécution de commandes à distance :** Exécute des commandes sur le système distant à partir d'e-mails avec le sujet `!command`.
- **Etat du système :** Renvoie l'état du système sur demande avec le sujet `!status`.
- **Aide :** Fournit une commande d'aide avec le sujet `!help`.
- **Effacement des logs :** Efface les logs système à partir d'un e-mail avec le sujet `!clearlogs`.
- **Surveillance continue :** Le script fonctionne en continu, vérifiant périodiquement les nouveaux e-mails.
- **Journalisation :** Les événements sont enregistrés dans un fichier de log (`attacker.log`).
- **Notifications d'erreur :** Les erreurs sont envoyées par e-mail à l'adresse spécifiée.

## 🛠️ Scripts

### Script 1: Command Execution with Linux Log Clearing

Le premier script est conçu pour fonctionner principalement sur un système Linux et inclut des commandes spécifiques pour effacer les logs système Linux.

### Script 2: Command Execution with Windows Log Clearing

Le second script est conçu pour fonctionner sur un système Windows et inclut des commandes spécifiques pour effacer les logs système Windows.

## ⚙️ Configuration requise

Avant d'utiliser ces scripts, assurez-vous d'avoir configuré les variables d'environnement suivantes dans un fichier `.env` :

- `GMAIL_USERNAME`: Nom d'utilisateur de votre compte Gmail.
- `GMAIL_PASSWORD`: Mot de passe de votre compte Gmail.
- `SENDTO_EMAIL`: Adresse e-mail à laquelle envoyer les réponses aux commandes.

## 📜 Utilisation

1. Configurez les variables d'environnement requises dans le fichier `.env`.
2. Exécutez le script en utilisant Python 3.
3. Envoyez des e-mails avec les sujets appropriés pour exécuter des commandes ou obtenir l'état du système.

### Exemples de sujets d'e-mail

- **Exécution de commande :**  
  Sujet : `!command <votre commande>`  
  Corps de l'e-mail : La commande à exécuter sur le système.

- **Obtenir l'état du système :**  
  Sujet : `!status`  
  Corps de l'e-mail : (Vide)

- **Effacer les logs système :**  
  Sujet : `!clearlogs`  
  Corps de l'e-mail : (Vide)

- **Obtenir de l'aide :**  
  Sujet : `!help`  
  Corps de l'e-mail : (Vide)

## ⚠️ Sécurité

- **Authentification sécurisée :** Assurez-vous que le compte Gmail utilisé dispose d'une authentification à deux facteurs et que vous utilisez un mot de passe d'application pour des raisons de sécurité.
- **Ne partagez pas le fichier `.env` :** Ne partagez pas le contenu de votre fichier `.env` avec d'autres personnes.
- **Attention aux sources d'e-mails non fiables :** Ce script exécute des commandes en fonction des e-mails reçus. Assurez-vous de ne pas exposer votre système à des risques de sécurité.

## 👤 Auteur

- **[BlackBird63030]**
