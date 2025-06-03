import re
from collections import Counter
import matplotlib.pyplot as plt
import csv
import json

fichier = r"E:\SCOLARITE\Master2_IRS\Projet_Python\TP2\TP2_auth.log"
regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# Listes pour stocker les IP
ips_echec = []
ips_succes = []

try:
    with open(fichier, "r") as f:
        for ligne in f:
            match = re.search(regex_ip, ligne)
            if match:
                ip = match.group()
                if "Failed password" in ligne:
                    ips_echec.append(ip)
                elif "Accepted password" in ligne:
                    ips_succes.append(ip)

    # Compter échecs/succès
    compteur_failed = Counter(ips_echec)
    compteur_success = Counter(ips_succes)

    # Top 5 des IPs avec le plus d’échecs
    top_failed = compteur_failed.most_common(5)

    # Données pour le graphique
    ip_labels = [ip for ip, _ in top_failed]
    nb_echecs = [nb for _, nb in top_failed]
    nb_reussites = [compteur_success[ip] for ip in ip_labels]

    # Affichage graphique
    x = range(len(ip_labels))

    plt.figure(figsize=(10, 6))
    plt.bar(x, nb_echecs, width=0.4, label="Échecs", color="red", align="center")
    plt.bar([i + 0.4 for i in x], nb_reussites, width=0.4, label="Réussites", color="green", align="center")
    plt.title("Top 5 IPs – Tentatives SSH échouées et réussies")
    plt.xlabel("Adresses IP")
    plt.ylabel("Nombre de tentatives")
    plt.xticks([i + 0.2 for i in x], ip_labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # Export CSV
    with open("resultats_ips.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "Échecs", "Réussites"])
        for ip in ip_labels:
            writer.writerow([ip, compteur_failed[ip], compteur_success[ip]])

    # Export JSON
    donnees_json = {
        ip: {"echecs": compteur_failed[ip], "reussites": compteur_success[ip]}
        for ip in ip_labels
    }
    with open("resultats_ips.json", "w") as jsonfile:
        json.dump(donnees_json, jsonfile, indent=4)

    # Interface utilisateur simple
    while True:
        choix = input("\nTapez une adresse IP pour voir ses stats (ou 'exit' pour quitter) : ")
        if choix.lower() == "exit":
            print("Fin de l'analyse.")
            break
        elif choix in compteur_failed or choix in compteur_success:
            print(f"Statistiques pour {choix} :")
            print(f"  - Échecs : {compteur_failed.get(choix, 0)}")
            print(f"  - Réussites : {compteur_success.get(choix, 0)}")
        else:
            print("IP non trouvée dans les logs.")

except FileNotFoundError:
    print(f"Fichier '{fichier}' introuvable.")
