# Voir énoncé TP 1 sans BONUS

import random

# Création de la liste des mots de passe faibles
mots_de_passe_faibles = [
    "123456", "password", "admin", "123456789", "qwerty",
    "abc123", "letmein", "welcome", "monkey", "football"
]

# Sélection d'un mot de passe aléatoire
mot_aleatoire = random.choice(mots_de_passe_faibles)
# Variable Booléenne pour savoir si le mot de passe a été trouvé
trouve = False
# Compteur d'essais à 0 par défaut
essais = 0

# Boucle tant que le mot n'est pas trouvé
while not trouve:
    # Demande à l'utilisateur de deviner et taper un mot
    proposition = input("Devinez le mot de passe : ")
    essais += 1  # On augmente le nombre d'essais à chaque fois que l'utilisateur tape une proposition

    # Si la proposition est correcte
    if proposition == mot_aleatoire:
        print("Bravo ! Vous avez trouvé le mot de passe.")
        trouve = True  # Fin de la boucle
    else:
        # Comparaison des longueurs
        if len(proposition) < len(mot_aleatoire):
            print("Le mot de passe est plus long.")
        elif len(proposition) > len(mot_aleatoire):
            print("Le mot de passe est plus court.")
        else:
            print("Longueur correcte, mais ce n'est pas le bon mot.")

        # Vérifie si la première lettre est la même
        if proposition and mot_aleatoire.startswith(proposition[0]):
            print("Il commence par la même lettre.")

        # Compter les lettres identiques à la même position
        lettres_communes = 0
        for a, b in zip(proposition, mot_aleatoire):
            if a == b:
                lettres_communes += 1
        print("Lettres communes à la même position :", lettres_communes)

# Affichage final
print("Nombre total d'essais :", essais)
