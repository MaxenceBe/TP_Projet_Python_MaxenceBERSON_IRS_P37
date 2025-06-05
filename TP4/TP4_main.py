import pandas as pd 
import re 
import matplotlib.pyplot as plt 

# Chargement/parsing du fichier 

def parse_log_line(line):
    # Regex pour extraire les différentes parties d'une ligne de log Apache 
    log_regex = re.compile(
        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - ' # Capture IP
        r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] ' # Capture date et heure
        r'"([A-Z]+) (\S+) HTTP/\d\.\d" ' # Capture HTTP (GET, POST, etc.) et URL
        r'(\d{3}) (\d+|-)\s*' # Capture le code de statut HTTP et taille de réponse
        r'(?:"([^"]*)"|(\S+))?\s*' # Capture le "referrer"
        r'"([^"]*)"' # Capture le user_agent
    )
    match = log_regex.match(line) 

    if match:
        ip, datetime_str, methode, url, status_str, _, user_agent = match.groups()[:7] 
        status = int(status_str) if status_str.isdigit() else None
        return {
            'ip': ip,
            'datetime': datetime_str,
            'methode': methode,
            'url': url,
            'status': status,
            'user_agent': user_agent
        }
    return None

def load_and_parse_log(file_path):
    # Charge le fichier access.log et parse chaque ligne + Dataframe
    parsed_data = [] # Liste pour stocker chaque ligne analysée
    with open(file_path, 'r') as f:
        for line in f: 
            data = parse_log_line(line)
            if data: 
                parsed_data.append(data) 
    # Crée un DataFrame à partir de la liste 
    df = pd.DataFrame(parsed_data) 
    # Convertit la colonne 'datetime' 
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    return df

log_file = r'E:\SCOLARITE\Master2_IRS\Projet_Python\TP4\access.log'

# Charge et parse le fichier log dans un DataFrame
print("Étape 1 - Chargement/parsing du fichier access.log")
df_logs = load_and_parse_log(log_file)
print("5 premières lignes du DataFrame:")
print(df_logs.head()) # Affiche les 5 premières lignes 
print("\n")

# Filtrage des erreurs 404 

print("Étape 2 - Filtrage des erreurs 404")
df_errors_404 = df_logs[df_logs['status'] == 404] # Sélectionne seulement les lignes 404
print("5 premières erreurs 404:")
print(df_errors_404.head()) # Affiche 5 premières erreurs
print(f"Nombre total d'erreurs 404: {len(df_errors_404)}\n")

# Top 5 des IPs en erreur

print("Étape 3 - Top 5 des IPs en erreurs 404")
# Groupe les erreurs 404 par IP + compte le nombre d'occurrences pour chaque IP
ip_404_nb = df_errors_404['ip'].value_counts()
# Sélectionne les 5 IPs les plus fréquentes
top_5_ips = ip_404_nb.head(5)
print("Top 5 des IPs générant le plus d'erreurs 404:")
print(top_5_ips)
print("\n")

# Visualisation

print("Étape 4 - Création de graphique des Top 5 IPs en erreur")
plt.figure(figsize=(10, 6)) 
top_5_ips.plot(kind='bar', color='skyblue') 
plt.title('Top 5 des IPs générant des erreurs 404') 
plt.xlabel('Adresse IP') 
plt.ylabel("Nombre d'erreurs 404") 
plt.xticks(rotation=45, ha='right') 
plt.grid(axis='y', linestyle='--') 
plt.tight_layout() 
plt.show() 
print("Graphique généré : 'Top 5 des IPs générant des erreurs 404'.\n")

# Détection de bots

print("Détection de bots")
# Filtre les lignes où user_agent contient 'bot', 'crawler' ou 'spider'
bot_patterns = 'bot|crawler|spider'
df_bots = df_logs[df_logs['user_agent'].str.contains(bot_patterns, case=False, na=False)]
print("Activités détectées comme bots:") 
print(df_bots.head()) 
print(f"Nombre total de requêtes provenant de bots: {len(df_bots)}\n")

# Identifier IPs suspectes bots
ip_suspect = df_bots['ip'].unique()
print(f"IPs suspectes d'être des bots): {ip_suspect}\n")

# Calculer le % d'erreurs 404 de bots 
df_404_bots = df_errors_404[df_errors_404['user_agent'].str.contains(bot_patterns, case=False, na=False)]
num_404_bots = len(df_404_bots)
total_404_erreurs = len(df_errors_404)

if total_404_erreurs > 0:
    pourcentage_404_bots = (num_404_bots / total_404_erreurs) * 100
    print(f"Pourcentage d'erreurs 404 de bots: {pourcentage_404_bots:.2f}%\n")
else:
    print("Aucune erreur 404 trouvée.\n")
