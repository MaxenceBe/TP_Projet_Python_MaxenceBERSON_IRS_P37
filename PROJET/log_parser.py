# log_parser.py
import re
from collections import defaultdict

def analyser_log_authentification(chemin_fichier_log):
    
    occurrences_ip = defaultdict(int)
    regex = r"Failed password.*from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    try:
        with open(chemin_fichier_log, 'r') as f:
            for ligne in f:
                # Vérifier si la ligne contient une indication d'échec d'authentification
                if "Failed password" in ligne: 
                    correspondance = re.search(regex, ligne)
                    if correspondance:
                        adresse_ip = correspondance.group(1)
                        occurrences_ip[adresse_ip] += 1
    except FileNotFoundError:
        print(f"Erreur : Le fichier de log '{chemin_fichier_log}' est introuvable.")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier de log : {e}")
        return None
    
    return dict(occurrences_ip)
