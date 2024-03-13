# Email Commander

Ce script Python permet d'exécuter des commandes sur un système distant via des e-mails. Il utilise le protocole POP3 pour surveiller une boîte aux lettres Gmail spécifiée et exécute les commandes contenues dans les e-mails reçus.

## Fonctionnalités

- Exécute des commandes sur le système distant à partir d'e-mails avec le sujet "!command".
- Renvoie l'état du système sur demande avec le sujet "!status".
- Fournit une commande d'aide avec le sujet "!help".
- Fonctionne en continu, vérifiant périodiquement les nouveaux e-mails.
- Ne laisse pas de trace localement
- Les erreurs sont envoyées par mail

## Configuration requise

Avant d'utiliser ce script, assurez-vous d'avoir configuré les variables d'environnement suivantes dans un fichier `.env` :

- `GMAIL_USERNAME`: Nom d'utilisateur de votre compte Gmail.
- `GMAIL_PASSWORD`: Mot de passe de votre compte Gmail.
- `SENDTO_EMAIL`: Adresse e-mail à laquelle envoyer les réponses aux commandes.

## Utilisation

1. Configurez les variables d'environnement requises dans le fichier `.env`.
2. Exécutez le script en utilisant Python 3.
3. Envoyez des e-mails avec les sujets appropriés pour exécuter des commandes ou obtenir l'état du système.

## Sécurité

- Assurez-vous que le compte Gmail utilisé dispose d'une authentification à deux facteurs et que vous utilisez un mot de passe d'application pour des raisons de sécurité.
- Ne partagez pas le contenu de votre fichier `.env` avec d'autres personnes.

## Avertissement

- Ce script exécute des commandes sur le système distant en fonction des e-mails reçus. Assurez-vous de ne pas exposer votre système à des risques de sécurité en autorisant l'exécution de commandes à partir de sources non fiables.

## Avertissement à des fins éducatives

Ce script est fourni uniquement à des fins éducatives et de démonstration. L'exécution de commandes à distance à partir d'e-mails peut présenter des risques de sécurité. Ne l'utilisez pas sur un système en production sans comprendre pleinement les implications de sécurité associées. L'auteur ne peut être tenu responsable de tout dommage résultant de l'utilisation de ce script.
