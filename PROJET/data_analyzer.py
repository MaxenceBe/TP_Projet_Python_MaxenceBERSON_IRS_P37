# data_analyzer.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def analyser_et_visualiser_ips(donnees_ip, repertoire_sortie="results"):
    #Conversion des données en DataFrame + trie des IPs les plus actives + graphique/export.

    if not donnees_ip:
        print("Aucune donnée IP à analyser ou visualiser.")
        return None, None

    df_ips = pd.DataFrame(list(donnees_ip.items()), columns=['Adresse_IP', 'Occurrences']) 
    
    #(Top 5)
    df_trie = df_ips.sort_values(by='Occurrences', ascending=False) 
    top_ips = df_trie.head(5)

    print("\nTop 5 IPs suspectes:")
    print(top_ips)

    # Creation répertoire
    if not os.path.exists(repertoire_sortie):
        os.makedirs(repertoire_sortie)

    # Générer un graphique à barres
    plt.figure(figsize=(10, 6))
    plt.bar(top_ips['Adresse_IP'], top_ips['Occurrences'], color='skyblue') 
    plt.xlabel('Adresse IP')
    plt.ylabel('Nombre d\'occurrences')
    plt.title('Top 5 des adresses IP suspectes (Tentatives de connexion échouées)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Enregistrer le graphique
    chemin_graphique = os.path.join(repertoire_sortie, 'top_ips_chart.png')
    plt.savefig(chemin_graphique)
    print(f"\nGraphique enregistré sous : {chemin_graphique}")
    # plt.show() # Décommenter pour afficher le graphique immédiatement

    # Exporter des résultats au format CSV
    chemin_csv = os.path.join(repertoire_sortie, 'suspect_ips.csv')
    df_trie.to_csv(chemin_csv, index=False) 
    print(f"Données exportées au format CSV sous : {chemin_csv}")
    
    return top_ips['Adresse_IP'].tolist(), chemin_graphique 

