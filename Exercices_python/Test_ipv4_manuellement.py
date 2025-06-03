# - Règles que doit respecter une adresse IPv4 :
# - Une adresse IPv4 est composée de 4 nombres séparés par des points (.)
# - Chaque nombre est compris entre 0 et 255
# - Tester avec : 
# [192.168.1.1]-[10.0.0.255]-[172.16.254.1]-[abc.def.ghi.jkl]-[256.256.256.256]-[192.168.1.]-[192.168.1.01]-[0.0.0.0]

import re  

# Expression régulière d'une adresse IPv4
regex_ip = r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
adresse = input("Saisissez une adresse IPv4 : ")
# Vérification
if re.match(regex_ip, adresse):
    print("L'adresse IPv4 est valide.")
else:
    print("L'adresse IPv4 n'est pas valide.")
