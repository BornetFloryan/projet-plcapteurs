import subprocess


def resoudre_avec_glpk(fichier_lp, fichier_solution):
    commande = ["glpsol", "--cpxlp", fichier_lp, "-o", fichier_solution]

    try:
        resultat = subprocess.run(commande, capture_output=True, text=True)
    except OSError:
        print("Erreur : GLPK n'est pas installé ou glpsol est introuvable.")
        return False

    if resultat.returncode != 0:
        print("Erreur pendant la résolution.")
        print(resultat.stderr)
        return False

    print("Résolution terminée.")
    return True


def lire_solution(fichier_solution):
    fichier = open(fichier_solution, "r", encoding="utf-8", errors="ignore")
    lignes = fichier.readlines()
    fichier.close()

    valeur_objectif = None
    valeurs_t = {}

    for ligne in lignes:
        ligne = ligne.strip()

        if ligne.startswith("Objective:"):
            morceaux = ligne.split("=")
            if len(morceaux) >= 2:
                valeur = morceaux[1].split()[0]
                valeur_objectif = float(valeur)

        morceaux = ligne.split()

        if len(morceaux) >= 4:
            nom_variable = morceaux[1]

            if nom_variable.startswith("t"):
                try:
                    valeur = float(morceaux[3])
                    valeurs_t[nom_variable] = valeur
                except ValueError:
                    pass

    return valeur_objectif, valeurs_t


def afficher_solution(valeur_objectif, valeurs_t, configurations):
    print("\nSolution :")
    print("Durée de vie maximale :", valeur_objectif)

    print("\nTemps d'activation :")

    for i in range(len(configurations)):
        nom_variable = "t" + str(i + 1)

        if nom_variable in valeurs_t:
            valeur = valeurs_t[nom_variable]
        else:
            valeur = 0

        if valeur > 0:
            print(nom_variable, "=", valeur, "pour la configuration", configurations[i])