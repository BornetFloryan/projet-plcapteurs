from couverture import rendre_elementaire, couvre_toutes_les_zones


def compter_nouvelles_zones(capteur, zones_deja_couvertes, couvertures):
    """
    Compte combien de nouvelles zones sont couvertes par ce capteur.
    """

    nombre_nouvelles_zones = 0
    zones_du_capteur = couvertures[capteur - 1]

    for zone in zones_du_capteur:
        if zone not in zones_deja_couvertes:
            nombre_nouvelles_zones = nombre_nouvelles_zones + 1

    return nombre_nouvelles_zones


def trouver_capteurs_qui_couvrent_le_plus(
    nb_capteurs,
    capteurs_choisis,
    zones_deja_couvertes,
    couvertures
):
    """
    Retourne tous les capteurs qui couvrent le plus de nouvelles zones.

    S'il y a plusieurs capteurs ex aequo, on les garde tous.
    """

    meilleurs_capteurs = []
    meilleur_nombre_zones = 0

    for capteur in range(1, nb_capteurs + 1):
        if capteur not in capteurs_choisis:
            nombre_zones = compter_nouvelles_zones(
                capteur,
                zones_deja_couvertes,
                couvertures
            )

            if nombre_zones > meilleur_nombre_zones:
                meilleur_nombre_zones = nombre_zones
                meilleurs_capteurs = [capteur]

            elif nombre_zones == meilleur_nombre_zones and nombre_zones > 0:
                meilleurs_capteurs.append(capteur)

    return meilleurs_capteurs


def ajouter_zones_du_capteur(capteur, zones_deja_couvertes, couvertures):
    """
    Ajoute les zones couvertes par un capteur dans la liste
    des zones deja couvertes.
    """

    zones_du_capteur = couvertures[capteur - 1]

    for zone in zones_du_capteur:
        if zone not in zones_deja_couvertes:
            zones_deja_couvertes.append(zone)


def construire_configurations_gloutonnes(
    configuration,
    capteurs_choisis,
    zones_deja_couvertes,
    nb_capteurs,
    nb_zones,
    couvertures
):
    """
    Construit une ou plusieurs configurations avec la methode gloutonne.

    A chaque etape, on garde tous les capteurs ex aequo
    qui couvrent le plus de nouvelles zones.
    """

    if len(zones_deja_couvertes) == nb_zones:
        configuration_elementaire = rendre_elementaire(
            configuration,
            couvertures,
            nb_zones
        )

        configuration_elementaire.sort()
        return [configuration_elementaire]

    meilleurs_capteurs = trouver_capteurs_qui_couvrent_le_plus(
        nb_capteurs,
        capteurs_choisis,
        zones_deja_couvertes,
        couvertures
    )

    if len(meilleurs_capteurs) == 0:
        return []

    configurations_trouvees = []

    for capteur in meilleurs_capteurs:
        nouvelle_configuration = configuration.copy()
        nouveaux_capteurs_choisis = capteurs_choisis.copy()
        nouvelles_zones_couvertes = zones_deja_couvertes.copy()

        nouvelle_configuration.append(capteur)
        nouveaux_capteurs_choisis.append(capteur)

        ajouter_zones_du_capteur(
            capteur,
            nouvelles_zones_couvertes,
            couvertures
        )

        configurations_suivantes = construire_configurations_gloutonnes(
            nouvelle_configuration,
            nouveaux_capteurs_choisis,
            nouvelles_zones_couvertes,
            nb_capteurs,
            nb_zones,
            couvertures
        )

        for config in configurations_suivantes:
            configurations_trouvees.append(config)

    return configurations_trouvees


def generer_configurations_gloutonnes(nb_capteurs, nb_zones, couvertures):
    """
    Genere des configurations elementaires avec une methode gloutonne.

    Pour chaque capteur de depart, on construit les configurations possibles.
    A chaque etape, si plusieurs capteurs couvrent le meme meilleur nombre
    de nouvelles zones, on les teste tous.
    """

    configurations = []

    for capteur_depart in range(1, nb_capteurs + 1):
        if capteur_depart % 100 == 0:
            print(
                "Progression :",
                capteur_depart,
                "/",
                nb_capteurs,
                "capteurs de depart testes"
            )

        configuration_depart = [capteur_depart]
        capteurs_choisis = [capteur_depart]
        zones_deja_couvertes = []

        ajouter_zones_du_capteur(
            capteur_depart,
            zones_deja_couvertes,
            couvertures
        )

        configurations_trouvees = construire_configurations_gloutonnes(
            configuration_depart,
            capteurs_choisis,
            zones_deja_couvertes,
            nb_capteurs,
            nb_zones,
            couvertures
        )

        for configuration in configurations_trouvees:
            if couvre_toutes_les_zones(configuration, couvertures, nb_zones):
                configuration.sort()

                if configuration not in configurations:
                    configurations.append(configuration)

    return configurations
