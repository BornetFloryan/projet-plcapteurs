def zones_couvertes(configuration, couvertures):
    """
    Retourne les zones couvertes par une configuration.
    """

    zones = []

    for capteur in configuration:
        zones_du_capteur = couvertures[capteur - 1]

        for zone in zones_du_capteur:
            if zone not in zones:
                zones.append(zone)

    return zones


def couvre_toutes_les_zones(configuration, couvertures, nb_zones):
    """
    Vérifie si une configuration couvre toutes les zones.
    """

    zones = zones_couvertes(configuration, couvertures)
    return len(zones) == nb_zones


def rendre_elementaire(configuration, couvertures, nb_zones):
    """
    Rend une configuration élémentaire en supprimant les capteurs redondants.
    """

    configuration_elementaire = configuration.copy()

    for capteur in configuration.copy():
        configuration_test = configuration_elementaire.copy()

        configuration_test.remove(capteur)

        if couvre_toutes_les_zones(configuration_test, couvertures, nb_zones):
            configuration_elementaire.remove(capteur)

    return configuration_elementaire
