import re
import os
import json
import csv
from collections import Counter
import matplotlib.pyplot as plt

fichier_log = r"E:\SCOLARITE\Master2_IRS\Projet_Python\TP2\TP2_auth.log"
regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# Données (ajoutées après analyse)
ips_echec = []
ips_succes = []
compteur_echecs = Counter()
compteur_succes = Counter()

def analyser_log():
    """Lit le fichier et remplit les compteurs d'IP échouées/réussies."""
    global ips_echec, ips_succes, compteur_echecs, compteur_succes
    ips_echec.clear()
    ips_succes.clear()

    try:
        with open(fichier_log, "r") as fichier:
            for ligne in fichier:
                match = re.search(regex_ip, ligne)
                if match:
                    ip = match.group()
                    if "Failed password" in ligne:
                        ips_echec.append(ip)
                    elif "Accepted password" in ligne:
                        ips_succes.append(ip)
        compteur_echecs = Counter(ips_echec)
        compteur_succes = Counter(ips_succes)
        print("Analyse terminée.")
    except FileNotFoundError:
        print(f"Fichier non trouvé : {fichier_log}")

def afficher_graphique():
    """Affiche un graphique des 5 IPs avec le plus d'échecs + réussites."""
    if not compteur_echecs:
        print("Veuillez d'abord analyser le fichier.")
        return

    top_echecs = compteur_echecs.most_common(5)
    ip_labels = [ip for ip, _ in top_echecs]
    nb_echecs = [nb for _, nb in top_echecs]
    nb_reussites = [compteur_succes[ip] for ip in ip_labels]

    x = range(len(ip_labels))
    plt.figure(figsize=(10, 6))
    plt.bar(x, nb_echecs, width=0.4, label="Échecs", color="red", align="center")
    plt.bar([i + 0.4 for i in x], nb_reussites, width=0.4, label="Réussites", color="green", align="center")
    plt.title("Top 5 IPs - Tentatives SSH échouées et réussies")
    plt.xlabel("Adresses IP")
    plt.ylabel("Nombre de tentatives")
    plt.xticks([i + 0.2 for i in x], ip_labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

def exporter_resultats():
    """Exporte les résultats des IPs dans un fichier CSV et JSON."""
    if not compteur_echecs:
        print("Veuillez d'abord analyser le fichier.")
        return

    top_echecs = compteur_echecs.most_common(5)
    ip_labels = [ip for ip, _ in top_echecs]

    # Export CSV
    with open("resultats_ips.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "Échecs", "Réussites"])
        for ip in ip_labels:
            writer.writerow([ip, compteur_echecs[ip], compteur_succes[ip]])

    # Export JSON
    donnees_json = {
        ip: {
            "echecs": compteur_echecs[ip],
            "reussites": compteur_succes[ip]
        } for ip in ip_labels
    }
    with open("resultats_ips.json", "w") as jsonfile:
        json.dump(donnees_json, jsonfile, indent=4)

    print("Export terminé.")
    print("CSV :", os.path.abspath("resultats_ips.csv"))
    print("JSON :", os.path.abspath("resultats_ips.json"))

def rechercher_ip():
    """Permet de rechercher une IP spécifique."""
    if not compteur_echecs:
        print("Veuillez d'abord analyser le fichier.")
        return

    while True:
        ip = input("🔎 Entrez une adresse IP à rechercher (ou 'exit' pour quitter) : ")
        if ip.lower() == "exit":
            break
        elif ip in compteur_echecs or ip in compteur_succes:
            print(f"Statistiques pour {ip} :")
            print(f"  - Échecs   : {compteur_echecs.get(ip, 0)}")
            print(f"  - Réussites : {compteur_succes.get(ip, 0)}")
        else:
            print("IP non trouvée dans les logs.")

def menu():
    """Menu principal interactif."""
    while True:
        print("\n=== MENU D'ANALYSE LOG SSH ===")
        print("1. Analyser le fichier auth.log")
        print("2. Afficher graphique (top 5 IP)")
        print("3. Exporter les résultats (CSV & JSON)")
        print("4. Rechercher une IP")
        print("5. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            analyser_log()
        elif choix == "2":
            afficher_graphique()
        elif choix == "3":
            exporter_resultats()
        elif choix == "4":
            rechercher_ip()
        elif choix == "5":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide, essayez encore.")

# Lancer le menu
menu()
