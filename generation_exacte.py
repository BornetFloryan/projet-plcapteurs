from itertools import combinations

from couverture import couvre_toutes_les_zones


def est_configuration_elementaire(configuration, couvertures, nb_zones):
    """
    Vérifie si une configuration est élémentaire.

    Une configuration est élémentaire si :
    - elle couvre toutes les zones ;
    - aucun capteur ne peut être retiré sans perdre cette couverture.
    """

    if not couvre_toutes_les_zones(configuration, couvertures, nb_zones):
        return False

    for capteur in configuration:
        configuration_test = configuration.copy()
        configuration_test.remove(capteur)

        if couvre_toutes_les_zones(configuration_test, couvertures, nb_zones):
            return False

    return True


def generer_configurations_exactes(nb_capteurs, nb_zones, couvertures):
    """
    Génère toutes les configurations élémentaires possibles.

    Cette méthode teste toutes les combinaisons de capteurs.
    Elle est donc adaptée seulement aux petites instances.
    """

    configurations = []

    for taille in range(1, nb_capteurs + 1):
        for combinaison in combinations(range(1, nb_capteurs + 1), taille):
            configuration = list(combinaison)

            if est_configuration_elementaire(configuration, couvertures, nb_zones):
                configurations.append(configuration)

    return configurations