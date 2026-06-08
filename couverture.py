def zones_couvertes(configuration, couvertures):
    zones = set()

    for capteur in configuration:
        indice_capteur = capteur - 1
        zones.update(couvertures[indice_capteur])

    return zones


def couvre_toutes_les_zones(configuration, couvertures, nb_zones):
    zones = zones_couvertes(configuration, couvertures)
    return len(zones) == nb_zones


def rendre_elementaire(configuration, couvertures, nb_zones):
    configuration_elementaire = configuration.copy()

    for capteur in configuration.copy():
        configuration_test = configuration_elementaire.copy()
        configuration_test.remove(capteur)

        capteur_est_inutile = couvre_toutes_les_zones(
            configuration_test,
            couvertures,
            nb_zones
        )

        if capteur_est_inutile:
            configuration_elementaire.remove(capteur)

    return configuration_elementaire