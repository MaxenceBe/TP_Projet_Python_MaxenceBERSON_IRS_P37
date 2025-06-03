# TP2_Partie1_Script_Simple
# 1. Ouvrir le fichier TP2_auth.log 
# 2. Extraire toutes les lignes contenant "Failed password" 
# 3. Extraire les adresses IP de ces lignes à l’aide d’une expression régulière 
# 4. Compter le nombre d’occurrences de chaque IP 
# 5. Afficher les 5 IPs ayant généré le plus d’échecs 

import re
from collections import Counter  # Permet de compter les IP

fichier = "E:\SCOLARITE\Master2_IRS\Projet_Python\TP2\TP2_auth.log"

# Liste des IP "Failed password"
ips_failed = []
regex_ip = r"(\d{1,3}\.){3}\d{1,3}"

try:
    with open(fichier, "r") as fichier:
        for ligne in fichier:
            # Lignes contenant "Failed password"
            if "Failed password" in ligne:
                # IP dans la ligne
                match = re.search(regex_ip, ligne)
                if match:
                    # Si IP trouvée - ajout à la liste
                    ips_failed.append(match.group())

    # Comptage des IP
    compteur_ips = Counter(ips_failed)

    # Affichage des 5 IP
    print("Les 5 IPs avec le plus de tentatives échouées sont :\n")
    for ip, nb in compteur_ips.most_common(5):
        print(f"{ip} → {nb} échecs")

except FileNotFoundError:
    print(f"Erreur : le fichier '{fichier}' est introuvable.")
