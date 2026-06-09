from generation_exacte import generer_configurations_exactes
from generation_gloutonne import generer_configurations_gloutonnes


def generer_configurations(nb_capteurs, nb_zones, couvertures, methode):
    """
    Génère les configurations selon la méthode choisie.

    methode = "exacte"    -> teste toutes les combinaisons
    methode = "gloutonne" -> utilise l'heuristique gloutonne
    """

    if methode == "exacte":
        print("Méthode utilisée : génération exacte")
        return generer_configurations_exactes(
            nb_capteurs,
            nb_zones,
            couvertures
        )

    if methode == "gloutonne":
        print("Méthode utilisée : heuristique gloutonne")
        return generer_configurations_gloutonnes(
            nb_capteurs,
            nb_zones,
            couvertures
        )

    print("Erreur : méthode inconnue.")
    return []


def afficher_configurations(configurations):
    """
    Affiche les configurations générées.
    """

    limite_affichage = 50

    print("\nConfigurations élémentaires générées :", len(configurations))

    for i in range(min(len(configurations), limite_affichage)):
        print("u" + str(i + 1), "=", configurations[i])

    if len(configurations) > limite_affichage:
        print(
            "...",
            len(configurations) - limite_affichage,
            "configurations non affichées"
        )
