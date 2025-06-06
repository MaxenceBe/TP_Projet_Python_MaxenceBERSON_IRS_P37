# main.py
import os
import sys

from log_parser import analyser_log_authentification
from data_analyzer import analyser_et_visualiser_ips
from network_scanner import scan_mono_thread, scan_multi_thread

def afficher_menu_principal():
    #Affichage menu principal
    print("\n***************************")
    print("    Menu interactif")
    print("***************************")
    print("1 - Analyser des logs ")
    print("2 - Scan de ports")
    print("3 - Analyser & scanner les IPs suspectes")
    print("4 - Quitter")
    print("***************************")

def input_utilisateur(invite, type_func=str, valeur_defaut=None, fonction_validation=None):
    #Input utilisateur avec option par défaut et validation.
    while True:
        input_complet = f"{invite} ({'par défaut: ' + str(valeur_defaut) if valeur_defaut is not None else 'obligatoire'}): "
        entree_utilisateur = input(input_complet).strip()
        
        if entree_utilisateur == "" and valeur_defaut is not None:
            return valeur_defaut
        
        if entree_utilisateur:
            try:
                entree_convertie = type_func(entree_utilisateur)
                if fonction_validation and not fonction_validation(entree_convertie):
                    print("Entrée invalide.")
                    continue
                return entree_convertie
            except ValueError:
                print("Entrée invalide.")
        elif valeur_defaut is None:
            print("Entrée obligatoire.")

def menu_analyse_log():
    #Gère menu pour l'analyse des logs.
    fichier_log = input_utilisateur("Chemin du fichier de logs", valeur_defaut='auth.log')
    print(f"\n Analyse du fichier de logs : {fichier_log}")
    ips_suspectes = analyser_log_authentification(fichier_log)
    
    # Correction ici : le bloc else doit être lié au premier if
    if ips_suspectes:
        print(" Analyse des logs terminée. Résultats: ")
        top_ips, _ = analyser_et_visualiser_ips(ips_suspectes)
        return top_ips 
    else: 
        print("Aucune IP suspecte trouvée ou erreur lors de l'analyse des logs.")
        return None

def menu_scan_ports(ips_predefinies=None):
    #Gère menu scan de ports.
    ips_a_scanner = []
    if ips_predefinies:
        ips_a_scanner.extend(ips_predefinies)
        print(f"\nScan de ports lancé avec les IPs prédéfinies : {', '.join(ips_a_scanner)}")
    else:
        chaine_ips = input_utilisateur("Entrez les adresses IP à scanner (séparées par des espaces)", type_func=str)
        if not chaine_ips:
            print("Aucune IP spécifiée pour le scan.")
            return
        ips_a_scanner = chaine_ips.split()
    
    chaine_ports = input_utilisateur("Entrez les ports à scanner (séparés par des espaces, ex: 22 80 443)", 
                               valeur_defaut='22 80 443 21 23 25 110 3389')
    ports = []
    try:
        ports = [int(p) for p in chaine_ports.split()]
        if not ports:
            print("Aucun port spécifié. Utilisation des ports par défaut.")
            ports = [22, 80, 443, 21, 23, 25, 110, 3389] # Ports par défaut si l'utilisateur entre vide
    except ValueError:
        print("Format de port invalide. Utilisation des ports par défaut.")
        ports = [22, 80, 443, 21, 23, 25, 110, 3389]

    choix_multithread = input_utilisateur("Activer le multi-thread pour le scan (oui/non)", valeur_defaut='non').lower()
    multithread = (choix_multithread == 'oui')

    choix_verbeux = input_utilisateur("Afficher les ports fermés (oui/non)", valeur_defaut='non').lower()
    verbeux = (choix_verbeux == 'oui')
    
    delai_attente = input_utilisateur("Délai d'attente pour chaque port (secondes)", type_func=float, valeur_defaut=1.0)

    if ips_a_scanner:
        effectuer_scan(ips_a_scanner, ports, multithread, verbeux, delai_attente)
    else:
        print("Aucune IP à scanner.")

def effectuer_scan(ips_a_scanner, ports, multithread, verbeux, delai_attente):
    #exécuter le scan.
    print(f"\n Lancement du scan de ports pour les IPs : {', '.join(ips_a_scanner)}")
    print(f"Ports à scanner : {', '.join(map(str, ports))}")
    print(f"Mode multi-thread : {'Oui' if multithread else 'Non'}")
    print(f"Mode verbeux : {'Oui' if verbeux else 'Non'}")
    print(f"Délai d'attente par port : {delai_attente} secondes")

    tous_ports_ouverts = {}
    for ip in ips_a_scanner:
        if multithread:
            ports_ouverts = scan_multi_thread(ip, ports, delai_attente, verbeux=verbeux)
        else:
            ports_ouverts = scan_mono_thread(ip, ports, delai_attente, verbeux=verbeux)
        
        if ports_ouverts:
            tous_ports_ouverts[ip] = ports_ouverts
        else:
            print(f"Aucun port ouvert trouvé sur {ip}.")
    
    if tous_ports_ouverts:
        print("\n***************************")
        print("    RÉSUMÉ DES PORTS OUVERTS      ")
        print("***************************")
        for ip, donnees_ports in tous_ports_ouverts.items():
            print(f"IP: {ip}")
            for port, statut in donnees_ports.items():
                print(f"  - Port {port}: {statut}")
        print("***************************\n")

        # Export des résultats de scan en HTML
        repertoire_sortie = "resultats"
        if not os.path.exists(repertoire_sortie):
            os.makedirs(repertoire_sortie)
        chemin_sortie_html = os.path.join(repertoire_sortie, 'scan_resultats.html')
        with open(chemin_sortie_html, 'w') as f:
            f.write("<!DOCTYPE html>\n<html>\n<head><title>Résultats du Scan de Ports</title>")
            f.write("<style>table, th, td {border: 1px solid black; border-collapse: collapse;} th, td {padding: 8px; text-align: left;} th {background-color: #f2f2f2;}</style>")
            f.write("</head>\n<body>\n")
            f.write("<h1>Résultats du Scan de Ports</h1>\n")
            f.write("<table>\n<tr><th>Adresse IP</th><th>Ports Ouverts</th></tr>\n")
            for ip, donnees_ports in tous_ports_ouverts.items():
                f.write(f"<tr><td>{ip}</td><td>{', '.join(map(str, donnees_ports.keys()))}</td></tr>\n")
            f.write("</table>\n</body>\n</html>")
        print(f"Résultats du scan de ports exportés en HTML : {chemin_sortie_html}")

def main():
    # Menu principal.
    while True: # Ajout de la boucle while True pour maintenir le menu
        afficher_menu_principal()
        choix = input_utilisateur("Votre choix", type_func=int)

        if choix == 1:
            # Analyser les logs
            menu_analyse_log()
        
        elif choix == 2:
            # Effectuer un scan de ports sur des IPs spécifiées manuellement
            menu_scan_ports()

        elif choix == 3:
            # Analyser les logs ET scanner les IPs suspectes
            print("\n--- Étape 1 : Analyse des logs ---")
            top_ips = menu_analyse_log()
            
            if top_ips:
                print("\n--- Étape 2 : Scan des IPs suspectes ---")
                print(f" Les IPs suspectes suivantes seront scannées : {', '.join(top_ips)}")
                menu_scan_ports(ips_predefinies=top_ips)
            else:
                print(" Pas d'IPs suspectes trouvées dans les logs pour lancer le scan.")

        elif choix == 4:
            print("Bye !")
            sys.exit(0)
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
        
        input("\nAppuyez sur Entrée pour revenir au menu principal...") # Pause pour que l'utilisateur lise la sortie

if __name__ == "__main__":
    main()