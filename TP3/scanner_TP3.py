import socket      # Pour les opérations réseau
import argparse    # Pour les arguments en ligne de commande
import os          # Pour la gestion des fichiers/dossiers
from concurrent.futures import ThreadPoolExecutor # Pour le scan multi-threadé

def tester_port(ip, port, delai, verbeux):
    """Tente une connexion à un port. Retourne True si ouvert, False sinon."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(delai) # Définit le délai d'attente

    try:
        res = sock.connect_ex((ip, port)) # Essaie de se connecter
        if res == 0: # 0 signifie succès (port ouvert)
            if verbeux: print(f"Port {port} sur {ip}: OUVERT")
            return True
        else:
            # Si pas ouvert, on peut afficher la raison en mode verbeux
            if verbeux: print(f"Port {port} sur {ip}: FERMÉ/FILTRÉ (Code erreur: {res})")
            return False
    except socket.gaierror: # Gère les adresses IP invalides
        print(f"Erreur: Adresse IP ou nom d'hôte invalide '{ip}'.")
        return False
    except socket.timeout: # Gère les délais dépassés
        if verbeux: print(f"Port {port} sur {ip}: DÉLAI D'ATTENTE DÉPASSÉ")
        return False
    except Exception as e: # Gère toute autre erreur inattendue
        print(f"Erreur inattendue au port {port}: {e}")
        return False
    finally:
        sock.close() # Ferme toujours le socket

def main():
    """Fonction principale pour configurer, exécuter et sauvegarder le scan."""
    # Configuration des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Scanner de ports TCP.")
    parser.add_argument('--ip', type=str, required=True, help="Adresse IP cible.")
    parser.add_argument('--start-port', type=int, required=True, help="Port de début de la plage.")
    parser.add_argument('--end-port', type=int, required=True, help="Port de fin de la plage.")
    parser.add_argument('--timeout', type=float, default=1.0, help="Délai d'attente par port (s).")
    parser.add_argument('--verbose', action='store_true', help="Affiche aussi les ports fermés/filtrés.")
    parser.add_argument('--multithread', action='store_true', help="Active le scan multi-threadé.")
    parser.add_argument('--output', type=str, help="Nom du fichier pour sauvegarder les résultats.")
    
    args = parser.parse_args()

    # Vérification simple de la plage de ports
    if args.start_port > args.end_port:
        print("Erreur: Le port de début doit être <= au port de fin.")
        return

    # Préparation du scan
    ports_a_scanner = range(args.start_port, args.end_port + 1)
    ports_ouverts = []

    print(f"\n--- Scan de {args.ip} (Ports: {args.start_port}-{args.end_port}) ---")
    
    # Exécution du scan (mono-thread ou multi-thread)
    if args.multithread:
        # Utilisation de ThreadPoolExecutor pour multi-threading (plus rapide)
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(tester_port, args.ip, port, args.timeout, args.verbose): port
            for port in ports_a_scanner}
            for future in futures:
                port = futures[future]
                try:
                    if future.result(): # Si le port est ouvert
                        ports_ouverts.append(port)
                except Exception: # Gère les exceptions des threads
                    pass # L'erreur a déjà été affichée par tester_port si verbeux
    else:
        # Scan mono-thread
        for port in ports_a_scanner:
            if tester_port(args.ip, port, args.timeout, args.verbose):
                ports_ouverts.append(port)

    # Affichage des ports ouverts
    print("\n--- Ports OUVERTS trouvés ---")
    if ports_ouverts:
        for port in sorted(ports_ouverts): # Affiche les ports triés
            print(f"Port {port} est ouvert.")
    else:
        print("Aucun port ouvert trouvé.")

    # Sauvegarde des résultats si un fichier de sortie est spécifié
    if args.output:
        output_dir = "rapports_scan"
        os.makedirs(output_dir, exist_ok=True) # Crée le dossier s'il n'existe pas
        file_path = os.path.join(output_dir, args.output)
        
        try:
            with open(file_path, 'w') as f:
                f.write(f"Scan de {args.ip} ({args.start_port}-{args.end_port})\n")
                f.write("-------------------------------------\n")
                if ports_ouverts:
                    f.write("Ports OUVERTS:\n")
                    for p_ouvert in sorted(ports_ouverts):
                        f.write(f"- {p_ouvert}\n")
                else:
                    f.write("Aucun port ouvert trouvé.\n")
            print(f"Résultats sauvegardés dans : {file_path}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    print("\nScan terminé.")

if __name__ == "__main__":
    main()