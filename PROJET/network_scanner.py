# network_scanner.py
import socket # Module socket importé
import threading
from concurrent.futures import ThreadPoolExecutor

def scanner_port(adresse_ip, port, delai_attente=1, verbeux=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
    sock.settimeout(delai_attente)
    resultat = sock.connect_ex((adresse_ip, port)) #
    sock.close() #
    
    if resultat == 0:
        if verbeux:
            print(f"Port {port} ouvert sur {adresse_ip}")
        return True
    else:
        if verbeux:
            print(f"Port {port} fermé/filtré sur {adresse_ip} (Erreur: {resultat})")
        return False

def scan_mono_thread(adresse_ip, ports, delai_attente=1, verbeux=False):
    print(f"\nLancement du scan mono-thread sur {adresse_ip}...")
    ports_ouverts = {}
    for port in ports:
        if scanner_port(adresse_ip, port, delai_attente, verbeux):
            ports_ouverts[port] = "Ouvert"
    return ports_ouverts

def scan_multi_thread(adresse_ip, ports, delai_attente=1, max_threads=20, verbeux=False):

    print(f"\nLancement du scan multi-thread sur {adresse_ip} avec {max_threads} threads...")
    ports_ouverts = {}
    
    with ThreadPoolExecutor(max_workers=max_threads) as executeur:
        futurs = {executeur.submit(scanner_port, adresse_ip, port, delai_attente, verbeux): port for port in ports}
        for futur in futurs:
            port = futurs[futur]
            try:
                if futur.result():
                    ports_ouverts[port] = "Ouvert"
            except Exception as exc:
                if verbeux:
                    print(f"Port {port} a généré une exception: {exc}")
    return ports_ouverts

if __name__ == "__main__":

    ip_cible = "127.0.0.1"  # IP locale pour les tests
    ports_communs = [21, 22, 23, 25, 80, 110, 135, 139, 443, 445, 3389, 8080]

    # Test du scanner mono-thread
    ports_ouverts_mono = scan_mono_thread(ip_cible, ports_communs, verbeux=True)
    print(f"\nPorts ouverts (Mono-thread) sur {ip_cible}: {ports_ouverts_mono}")

    # Test du scanner multi-thread
    ports_ouverts_multi = scan_multi_thread(ip_cible, ports_communs, verbeux=True)
    print(f"\nPorts ouverts (Multi-thread) sur {ip_cible}: {ports_ouverts_multi}")