# Test IPv4 de façon automatique avec IP contenues dans un fichier texte

import re

regex_ip = r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
fichier = "Liste_IPv4.txt"

try:
    with open(fichier, "r") as fichier:
        lignes = fichier.readlines()

    print("Voici le résultat de la vérification des adresses IP :\n")

    for ligne in lignes:
        ip = ligne.strip()

        # Vérification avec regex
        if re.match(regex_ip, ip):
            print(f"{ip} : Cette adresse IP est valide")
        else:
            print(f"{ip} : Cette adresse IP est invalide")

except FileNotFoundError:
    print(f"Erreur : le fichier '{fichier}' est introuvable.")

