import psutil # Pour obtenir les métriques système
import time # Pour les pauses (attendre 5 secondes)
import os # Pour effacer l'écran
import sys # Pour quitter le programme proprement (bien que Ctrl+C soit préférable ici)

# --- Fonction pour effacer l'écran ---
def clear_screen():
    """
    Efface l'écran du terminal.
    Utilise 'clear' pour Linux/macOS et 'cls' pour Windows.
    """
    if os.name == 'posix': # Pour Linux et macOS
        _ = os.system('clear')
    else: # Pour Windows
        _ = os.system('cls')

# --- Fonction pour afficher une barre graphique ASCII ---
def get_ascii_bar(percent, width=50):
    """
    Génère une barre de progression ASCII pour un pourcentage donné.
    Ex: [████████████████████████████████████████████████] 100.0%
    """
    # S'assure que le pourcentage est entre 0 et 100
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100
    
    # Calcule la largeur de la barre remplie
    filled_width = int(width * percent / 100)
    # Crée la barre avec des caractères "█" pour la partie remplie et "-" pour le reste
    bar = '█' * filled_width + '-' * (width - filled_width)
    return f"[{bar}] {percent:.1f}%" # Retourne la barre et le pourcentage formaté

# --- Fonction principale pour afficher le tableau de bord ---
def display_dashboard():
    """
    Affiche dynamiquement les informations système dans un tableau de bord textuel.
    Se rafraîchit toutes les 5 secondes et permet de quitter avec 'q'.
    """
    
    # Initialise les compteurs réseau pour calculer le débit (octets/seconde)
    # On stocke les compteurs actuels pour pouvoir calculer la différence à la prochaine itération.
    last_net_io = psutil.net_io_counters() 
    
    while True: # Boucle infinie pour rafraîchir l'affichage du tableau de bord
        clear_screen() # Efface l'écran à chaque nouveau cycle pour un affichage propre
        
        print("--- Tableau de Bord des Métriques Système ---")
        print("Pour quitter, tapez 'q' et appuyez sur Entrée (ou Ctrl+C).\n")
        
        # Section 1: Utilisation CPU
        print("### Utilisation CPU ###")
        # psutil.cpu_percent(interval=None, percpu=True) : Obtient l'utilisation CPU depuis le dernier appel.
        # percpu=True donne une liste de pourcentages, un par cœur CPU.
        cpu_percents = psutil.cpu_percent(interval=None, percpu=True)
        # psutil.cpu_percent(interval=None) : Donne l'utilisation totale moyenne du CPU.
        cpu_total_percent = psutil.cpu_percent(interval=None) 
        
        # Affiche l'utilisation pour chaque cœur CPU
        for i, percent in enumerate(cpu_percents):
            print(f"  Cœur {i}: {get_ascii_bar(percent)}") 
        # Affiche l'utilisation totale du CPU
        print(f"  Total: {get_ascii_bar(cpu_total_percent)}") 
        print("-" * 30) # Ligne de séparation

        # Section 2: Mémoire RAM
        print("\n### Mémoire RAM ###")
        ram = psutil.virtual_memory() # Obtient toutes les informations sur la RAM
        print(f"  Total: {ram.total / (1024**3):.2f} GB") # Convertit les octets en Gigaoctets
        print(f"  Utilisée: {ram.used / (1024**3):.2f} GB ({get_ascii_bar(ram.percent, width=30)})")
        print(f"  Libre: {ram.free / (1024**3):.2f} GB")
        print("-" * 30)

        # Section 3: Utilisation Disque par partition 
        print("\n### Utilisation Disque ###")
        # psutil.disk_partitions() : Liste toutes les partitions de disque trouvées sur le système.
        for partition in psutil.disk_partitions():
            try:
                # psutil.disk_usage(partition.mountpoint) : Obtient l'utilisation pour le point de montage de la partition.
                disk = psutil.disk_usage(partition.mountpoint)
                print(f"  {partition.device} ({partition.mountpoint}):") # Nom du périphérique et point de montage
                print(f"    Total: {disk.total / (1024**3):.2f} GB")
                print(f"    Utilisé: {disk.used / (1024**3):.2f} GB ({get_ascii_bar(disk.percent, width=30)})")
                print(f"    Libre: {disk.free / (1024**3):.2f} GB")
            except PermissionError:
                # Gère les cas où l'accès à une partition est refusé (ex: lecteur de CD vide, partition non montée)
                print(f"  Accès refusé pour {partition.device} ({partition.mountpoint})")
            except Exception as e:
                # Gère toute autre erreur inattendue lors de la récupération des infos disque
                print(f"  Erreur lors de la récupération des infos disque pour {partition.mountpoint}: {e}")
        print("-" * 30)

        # Section 4: Activité Réseau (Octets et Paquets Envoyés/Reçus) 
        print("\n### Activité Réseau ###")
        current_net_io = psutil.net_io_counters() # Obtient les compteurs réseau actuels
        
        # Calcul du débit en octets/seconde sur les 5 dernières secondes
        bytes_sent_diff = current_net_io.bytes_sent - last_net_io.bytes_sent
        bytes_recv_diff = current_net_io.bytes_recv - last_net_io.bytes_recv
        
        # On divise par l'intervalle de temps (5 secondes) pour obtenir un débit par seconde
        send_speed_mbps = (bytes_sent_diff / (1024**2)) / 5 # Débit en Mégaoctets par seconde
        recv_speed_mbps = (bytes_recv_diff / (1024**2)) / 5 # Débit en Mégaoctets par seconde

        print(f"  Octets envoyés (total): {current_net_io.bytes_sent / (1024**2):.2f} MB")
        print(f"  Octets reçus (total): {current_net_io.bytes_recv / (1024**2):.2f} MB")
        print(f"  Vitesse d'envoi: {send_speed_mbps:.2f} MB/s")
        print(f"  Vitesse de réception: {recv_speed_mbps:.2f} MB/s")
        print(f"  Paquets envoyés (total): {current_net_io.packets_sent}")
        print(f"  Paquets reçus (total): {current_net_io.packets_recv}")
        
        # Met à jour les compteurs précédents pour le prochain calcul de débit
        last_net_io = current_net_io 
        print("-" * 30)

        # Section 5: Statistiques réseau par interface 
        print("\n### Statistiques Réseau par Interface ###")
        # psutil.net_if_stats() : Statistiques de chaque interface réseau (up/down, vitesse, etc.)
        # psutil.net_io_counters(pernic=True) : Compteurs d'E/S pour chaque interface réseau
        if_stats = psutil.net_if_stats()
        if_io_counters = psutil.net_io_counters(pernic=True)

        for interface_name, stats in if_stats.items(): # Parcourt chaque interface réseau
            print(f"  Interface: {interface_name}")
            print(f"    Statut: {'UP' if stats.isup else 'DOWN'}") # Indique si l'interface est active
            print(f"    Duplex: {stats.duplex.name}") # Mode duplex (full, half)
            print(f"    Vitesse: {stats.speed} Mbps") # Vitesse de l'interface
            
            # Affiche les compteurs d'E/S spécifiques à cette interface si disponibles
            if interface_name in if_io_counters:
                io_counts = if_io_counters[interface_name]
                print(f"    Octets envoyés: {io_counts.bytes_sent / (1024**2):.2f} MB")
                print(f"    Octets reçus: {io_counts.bytes_recv / (1024**2):.2f} MB")
            print("-" * 30)

        # Bonus 1: Température CPU (si disponible sur le système) 
        print("\n### Température CPU (Bonus) ###")
        # hasattr(psutil, "sensors_temperatures") : Vérifie si la fonction existe sur le système actuel.
        # Cette fonction n'est pas disponible sur tous les systèmes (ex: souvent pas sur Windows).
        if hasattr(psutil, "sensors_temperatures"): 
            temps = psutil.sensors_temperatures() # Obtient les températures des capteurs
            if temps: # Si des températures sont retournées
                for name, entries in temps.items(): # Parcourt chaque catégorie de capteurs (ex: cpu_fan, coretemp)
                    print(f"  {name}:")
                    for entry in entries: # Parcourt chaque entrée de température dans la catégorie
                        # entry.label peut donner un nom plus spécifique (ex: "Package id 0")
                        # entry.current est la température actuelle
                        print(f"    {entry.label or name}: {entry.current}°C")
            else:
                print("  Température CPU non disponible (ou capteurs non trouvés).")
        else:
            print("  La fonction psutil.sensors_temperatures() n'est pas disponible sur ce système.")
        print("-" * 30)

        # Bonus 3: Export des données dans un fichier log (CSV)
        # Les données sont écrites à chaque itération dans un fichier CSV simple.
        # Le fichier 'system_metrics.csv' sera créé ou mis à jour dans le même dossier que le script.
        try:
            # 'a' pour "append" (ajouter à la fin) : si le fichier n'existe pas, il est créé.
            with open('system_metrics.csv', 'a') as f: 
                # Vérifie si le fichier est vide pour écrire l'en-tête une seule fois
                if os.path.getsize('system_metrics.csv') == 0:
                    f.write("Timestamp,CPU_Total_Percent,RAM_Used_Percent,Bytes_Sent_Total,Bytes_Recv_Total\n")
                
                # Écrit les données actuelles dans le fichier
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # Format de la date et heure
                f.write(f"{timestamp},{cpu_total_percent},{ram.percent},{current_net_io.bytes_sent},{current_net_io.bytes_recv}\n")
            print("  Données exportées dans system_metrics.csv")
        except Exception as e:
            print(f"  Erreur lors de l'export des données: {e}")
        print("-" * 30)

        # Attendre 5 secondes avant la prochaine mise à jour de l'affichage
        print("\nRafraîchissement dans 5 secondes...")
        time.sleep(5) # Pause de 5 secondes

        # Option pour quitter le programme (après la pause de 5 secondes)
        # Cela permet au tableau de bord de rester affiché pendant 5 secondes avant d'attendre une entrée.
        print("\n") # Laisse un espace pour la saisie utilisateur
        try:
            # Attend une entrée de l'utilisateur. C'est une action bloquante.
            user_input = input("Appuyez sur Entrée pour rafraîchir, ou tapez 'q' pour quitter : ").strip().lower()
            if user_input == 'q': # Si l'utilisateur tape 'q'
                print("Quitting program...")
                break # Sort de la boucle infinie 'while True'
        except KeyboardInterrupt:
            # Gère l'appui sur Ctrl+C si cela se produit pendant l'attente de l'input()
            print("\nInterruption clavier détectée (Ctrl+C). Quitting program.")
            break
        except Exception as e:
            # Gère toute autre erreur lors de la saisie utilisateur
            print(f"Une erreur inattendue est survenue lors de la saisie utilisateur: {e}")
            break # Quitte en cas d'erreur

# --- Point d'entrée du programme ---
if __name__ == "__main__":
    # Ce bloc s'exécute uniquement si le script est lancé directement (pas importé comme un module).
    print("Démarrage du tableau de bord. Appuyez sur Ctrl+C pour quitter à tout moment.")
    try:
        display_dashboard() # Appelle la fonction principale pour démarrer le tableau de bord
    except KeyboardInterrupt:
        # Attrape l'exception KeyboardInterrupt (Ctrl+C) si elle est pressée en dehors de l'input()
        print("\nTableau de bord terminé suite à une interruption utilisateur.")
    finally:
        # Ce bloc s'exécute toujours, que des erreurs se produisent ou non.
        # Utile pour le nettoyage (fermer des fichiers, etc.) si nécessaire.
        pass