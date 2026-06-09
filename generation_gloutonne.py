from couverture import rendre_elementaire, couvre_toutes_les_zones


def compter_nouvelles_zones(capteur, zones_deja_couvertes, couvertures):
    """Compte combien de nouvelles zones sont couvertes par ce capteur."""
    zones_du_capteur = couvertures[capteur - 1]
    return len(zones_du_capteur - zones_deja_couvertes)


def choisir_capteur_qui_couvre_le_plus(
    nb_capteurs,
    capteurs_choisis,
    zones_deja_couvertes,
    couvertures,
    choisir_dernier_en_cas_egalite
):
    """
    Choisit le capteur qui couvre le plus de nouvelles zones.

    En cas d'egalite, on choisit soit le premier, soit le dernier.
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

    if len(meilleurs_capteurs) == 0:
        return None

    if choisir_dernier_en_cas_egalite:
        return meilleurs_capteurs[-1]

    return meilleurs_capteurs[0]


def ajouter_zones_du_capteur(capteur, zones_deja_couvertes, couvertures):
    """Ajoute les zones couvertes par un capteur."""
    zones_deja_couvertes.update(couvertures[capteur - 1])


def construire_configuration_gloutonne(
    capteur_depart,
    nb_capteurs,
    nb_zones,
    couvertures,
    choisir_dernier_en_cas_egalite
):
    """Construit une configuration avec la methode gloutonne."""
    configuration = [capteur_depart]
    capteurs_choisis = {capteur_depart}
    zones_deja_couvertes = set()

    ajouter_zones_du_capteur(
        capteur_depart,
        zones_deja_couvertes,
        couvertures
    )

    while len(zones_deja_couvertes) < nb_zones:
        capteur_a_ajouter = choisir_capteur_qui_couvre_le_plus(
            nb_capteurs,
            capteurs_choisis,
            zones_deja_couvertes,
            couvertures,
            choisir_dernier_en_cas_egalite
        )

        if capteur_a_ajouter is None:
            return None

        configuration.append(capteur_a_ajouter)
        capteurs_choisis.add(capteur_a_ajouter)
        ajouter_zones_du_capteur(
            capteur_a_ajouter,
            zones_deja_couvertes,
            couvertures
        )

    configuration = rendre_elementaire(configuration, couvertures, nb_zones)
    configuration.sort()
    return configuration


def generer_configurations_gloutonnes(nb_capteurs, nb_zones, couvertures):
    """
    Genere deux configurations par capteur de depart.

    En cas d'egalite, la premiere choisit le premier capteur possible
    et la seconde choisit le dernier.
    """
    configurations = []
    configurations_connues = set()
    couvertures = [set(zones) for zones in couvertures]

    for capteur_depart in range(1, nb_capteurs + 1):
        if capteur_depart % 100 == 0:
            print(
                "Progression :",
                capteur_depart,
                "/",
                nb_capteurs,
                "capteurs de depart testes"
            )

        for choisir_dernier in [False, True]:
            configuration = construire_configuration_gloutonne(
                capteur_depart,
                nb_capteurs,
                nb_zones,
                couvertures,
                choisir_dernier
            )

            if configuration is not None:
                if couvre_toutes_les_zones(configuration, couvertures, nb_zones):
                    cle_configuration = tuple(configuration)

                    if cle_configuration not in configurations_connues:
                        configurations_connues.add(cle_configuration)
                        configurations.append(configuration)

    return configurations
