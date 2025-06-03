# VOIR ENONCE TP1 AVEC BONUS
import random

# Chargement des mots de passe faibles depuis le fichier texte
with open("TP1_passe.txt", "r") as fichier:
    mots_de_passe_faibles = [ligne.strip() for ligne in fichier if ligne.strip()]

# Sélection d'un mot de passe aléatoire
mot_aleatoire = random.choice(mots_de_passe_faibles)
# Limite d'essais
limite_essais = int(input("Combien de tentatives maximum souhaitez-vous ? "))
# Initialisation des variables
trouve = False
essais = 0
historique = []  # Liste pour stocker les propositions
# Boucle 
while not trouve and essais < limite_essais:
    proposition = input("Devinez le mot de passe ('triche' pour le révéler) : ")
    essais += 1 # Incrémente essais de 1
    historique.append(proposition) #création de l'historique
    # Option triche
    if proposition.lower() == "triche":
        print("Mot de passe révélé (triche) :", mot_aleatoire)
        continue  # Ne compte pas comme une vraie tentative
    # Réponse correcte
    if proposition == mot_aleatoire:
        print("Bravo ! Vous avez trouvé le mot de passe.")
        trouve = True
    else:
        # Mauvaise réponse, on donne des indices
        if len(proposition) < len(mot_aleatoire):
            print("Le mot de passe est plus long.")
        elif len(proposition) > len(mot_aleatoire):
            print("Le mot de passe est plus court.")
        else:
            print("Longueur correcte, mais ce n'est pas le bon mot.")

        # Vérification de la première lettre
        if proposition and mot_aleatoire.startswith(proposition[0]):
            print("Il commence par la même lettre.")

        # Compte les lettres identiques à la même position
        lettres_communes = 0
        for a, b in zip(proposition, mot_aleatoire):
            if a == b:
                lettres_communes += 1
        print("Lettres communes à la même position :", lettres_communes)

# Trop de tentatives ratées
if not trouve:
    print("Vous avez atteint la limite d’essais.")
    print("Le mot de passe était :", mot_aleatoire)

# Résumé
print("\n--- Résumé ---")
print("Votre nombre de tentatives est :", essais)
print("Voici l'historique de vos tentatives :")
for i, tentative in enumerate(historique, 1):
    print(f"{i}. {tentative}")
