# Partie 2 – Visualisation (script avancé) 
# 1. Utiliser la bibliothèque matplotlib (utilisez pip install matplotlib)
# 2. Créer un graphique de barres représentant les IPs avec le plus grand nombre d’échecs 
# 3. Comparer les IPs ayant échoué et celles ayant réussi (bonus) 
# 4. Ajouter une légende, un titre, et des axes lisibles 

import re
from collections import Counter
import matplotlib.pyplot as plt 

fichier = r"E:\SCOLARITE\Master2_IRS\Projet_Python\TP2\TP2_auth.log"
regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# Listes
ips_echec = []
ips_succes = []

try:
    with open(fichier, "r") as fichier:
        for ligne in fichier:
            match = re.search(regex_ip, ligne)
            if match:
                ip = match.group()
                if "Failed password" in ligne:
                    ips_echec.append(ip) 
                elif "Accepted password" in ligne:
                    ips_succes.append(ip) 

    # Compteur IP echec
    compteur_failed = Counter(ips_echec)
    top_failed = compteur_failed.most_common(5)

    # Données pour le graphique
    ip_labels = [ip for ip, _ in top_failed]
    nb_echecs = [nb for _, nb in top_failed]

    # Compteur IP succes
    compteur_success = Counter(ips_succes)
    nb_reussites = [compteur_success[ip] for ip in ip_labels]

    # Création du graphique de barres
    x = range(len(ip_labels))  # positions sur l'axe X

    plt.figure(figsize=(10, 6))  # Taille du graphique

    # Echecs = Rouge
    plt.bar(x, nb_echecs, width=0.4, label="Échecs", color="red", align="center")

    # Réussites = Vert
    plt.bar([i + 0.4 for i in x], nb_reussites, width=0.4, label="Réussites", color="green", align="center")

    # Titres
    plt.title("Top 5 IPs – Tentatives SSH échouées et réussies")
    plt.xlabel("Adresses IP")
    plt.ylabel("Nombre de tentatives")
    plt.xticks([i + 0.2 for i in x], ip_labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

except FileNotFoundError:
    print(f"Fichier '{fichier}' introuvable.")

