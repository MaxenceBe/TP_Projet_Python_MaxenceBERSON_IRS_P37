import string
ambiguous_chars = {'I', 'l', '1'}

while True:
    mot_de_passe = input("Saisir votre mot de passe : ")

    # Vérifie la longueur
    if len(mot_de_passe) < 12:
        print("Votre mot de passe doit contenir au minimum 12 caractères.")
        continue

    # Remise à zéro des compteurs
    Maj = 0
    Min = 0
    Chiffres = 0
    Cara_spe = 0
    Ambigu = 0

    # Parcours du mot de passe caractère par caractère
    for char in mot_de_passe:
        if char in ambiguous_chars:
            Ambigu += 1
        elif char.isupper():
            Maj += 1
        elif char.islower():
            Min += 1
        elif char.isdigit():
            Chiffres += 1
        elif char in string.punctuation:
            Cara_spe += 1

    # Vérification des conditions
    if Maj == 0:
        print("Le mot de passe doit contenir au moins une majuscule.")
        continue
    if Min == 0:
        print("Le mot de passe doit contenir au moins une minuscule.")
        continue
    if Chiffres == 0:
        print("Le mot de passe doit contenir au moins un chiffre.")
        continue
    if Cara_spe == 0:
        print("Le mot de passe doit contenir au moins un caractère spécial.")
        continue
    if Ambigu > 0:
        print("Le mot de passe contient un caractère ambigu (comme I, l, 1).")
        continue

    # Si toutes les vérifications sont passées
    print("Mot de passe accepté.")
    print("Le mot de passe est :", mot_de_passe)
    break