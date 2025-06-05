import psutil # Importe la bibliothèque psutil
import time   # Importe la bibliothèque time pour les pauses

print("--- Découverte des fonctions psutil ---")

# psutil.cpu_percent()
# Fonctionnalité: Retourne le pourcentage d'utilisation du CPU.
# Si vous l'appelez sans délai (interval=None), elle donne la charge depuis le dernier appel.
# Avec un délai (ex: interval=1), elle calcule la charge sur la dernière seconde.
print("\n1. Utilisation CPU (psutil.cpu_percent()):")
# Premier appel pour initialiser la mesure. psutil.cpu_percent() a besoin d'être appelé
# une première fois pour que le deuxième appel (avec interval=1) soit précis.
# percpu=True donne l'utilisation pour chaque cœur logique du CPU.
psutil.cpu_percent(interval=None, percpu=True) 
print("  (Premier appel pour initialisation, attendez 1 seconde pour le prochain appel)")
time.sleep(1) # Attend une seconde pour permettre la collecte de données pour la mesure suivante.

# Charge totale du CPU sur la dernière seconde.
cpu_usage_total = psutil.cpu_percent(interval=1) 
# Charge par cœur CPU sur la dernière seconde.
cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True) 
print(f"  Utilisation CPU totale (dernière seconde): {cpu_usage_total}%")
print(f"  Utilisation CPU par cœur (dernière seconde): {cpu_usage_per_core}%")


# psutil.virtual_memory()
# Fonctionnalité: Retourne des statistiques sur l'utilisation de la mémoire vive (RAM).
# L'objet retourné contient des informations comme la mémoire totale, disponible, utilisée, libre, etc.
print("\n2. Mémoire Virtuelle (psutil.virtual_memory()):")
ram = psutil.virtual_memory() # Récupère les informations sur la mémoire virtuelle.
# Convertit les octets en Gigaoctets pour une meilleure lisibilité (1 GB = 1024^3 octets).
print(f"  Mémoire RAM totale: {ram.total / (1024**3):.2f} GB") 
print(f"  Mémoire RAM utilisée: {ram.used / (1024**3):.2f} GB ({ram.percent:.1f}%)")
print(f"  Mémoire RAM libre: {ram.free / (1024**3):.2f} GB")


# psutil.disk_usage('/')
# Fonctionnalité: Retourne des statistiques sur l'utilisation de l'espace disque pour un chemin donné.
# Pour Windows, utilisez la lettre du lecteur, par exemple 'C:/'. Pour Linux/macOS, utilisez '/'.
print("\n3. Utilisation Disque (psutil.disk_usage()):")
try:
    # Tente d'abord pour les systèmes Unix-like (Linux, macOS) en utilisant le répertoire racine '/'.
    disk = psutil.disk_usage('/')
    print(f"  Espace disque total sur '/': {disk.total / (1024**3):.2f} GB")
    print(f"  Espace disque utilisé sur '/': {disk.used / (1024**3):.2f} GB ({disk.percent:.1f}%)")
    print(f"  Espace disque libre sur '/': {disk.free / (1024**3):.2f} GB")
except Exception as e_unix:
    # Si l'accès à '/' échoue (probablement sur Windows), essaie 'C:/'.
    try:
        disk = psutil.disk_usage('C:/')
        print(f"  Espace disque total sur 'C:/': {disk.total / (1024**3):.2f} GB")
        print(f"  Espace disque utilisé sur 'C:/': {disk.used / (1024**3):.2f} GB ({disk.percent:.1f}%)")
        print(f"  Espace disque libre sur 'C:/': {disk.free / (1024**3):.2f} GB")
    except Exception as e_win:
        # Si les deux tentatives échouent, affiche un message d'erreur.
        # On affiche les erreurs spécifiques pour aider au débogage.
        print(f"  Impossible de récupérer l'utilisation du disque.")
        print(f"  Erreur Unix-like: {e_unix}")
        print(f"  Erreur Windows: {e_win}")


# psutil.net_io_counters()
# Fonctionnalité: Retourne des statistiques globales d'entrée/sortie réseau (octets et paquets envoyés/reçus)
# depuis le démarrage du système. Ces valeurs sont cumulatives.
print("\n4. Compteurs d'E/S Réseau (psutil.net_io_counters()):")
net_io = psutil.net_io_counters() # Récupère les compteurs d'entrée/sortie réseau.
# Convertit les octets en Mégaoctets.
print(f"  Octets envoyés: {net_io.bytes_sent / (1024**2):.2f} MB") 
print(f"  Octets reçus: {net_io.bytes_recv / (1024**2):.2f} MB")
print(f"  Paquets envoyés: {net_io.packets_sent}")
print(f"  Paquets reçus: {net_io.packets_recv}")

print("\n--- Fin de la découverte ---")