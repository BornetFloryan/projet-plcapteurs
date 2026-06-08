import random

from couverture import rendre_elementaire


def capteur_est_autorise(capteur, capteurs_choisis, capteurs_tabous):
    pas_deja_choisi = capteur not in capteurs_choisis
    pas_tabou = capteur not in capteurs_tabous

    return pas_deja_choisi and pas_tabou


def calculer_gain(capteur, zones_deja_couvertes, couvertures_ensembles):
    zones_du_capteur = couvertures_ensembles[capteur - 1]
    nouvelles_zones = zones_du_capteur - zones_deja_couvertes

    return len(nouvelles_zones)


def est_un_meilleur_choix(capteur, gain, meilleur_capteur, meilleur_gain, utilisations):
    gain_positif = gain > 0
    aucun_capteur_choisi = meilleur_capteur is None
    gain_plus_grand = gain > meilleur_gain

    meme_gain_mais_moins_utilise = (
        meilleur_capteur is not None
        and gain == meilleur_gain
        and utilisations[capteur] < utilisations[meilleur_capteur]
    )

    return gain_positif and (
        aucun_capteur_choisi
        or gain_plus_grand
        or meme_gain_mais_moins_utilise
    )


def choisir_meilleur_capteur(
    nb_capteurs,
    zones_deja_couvertes,
    couvertures_ensembles,
    capteurs_choisis,
    capteurs_tabous,
    utilisations
):
    meilleur_capteur = None
    meilleur_gain = 0

    for capteur in range(1, nb_capteurs + 1):
        autorise = capteur_est_autorise(
            capteur,
            capteurs_choisis,
            capteurs_tabous
        )

        if autorise:
            gain = calculer_gain(
                capteur,
                zones_deja_couvertes,
                couvertures_ensembles
            )

            meilleur_choix = est_un_meilleur_choix(
                capteur,
                gain,
                meilleur_capteur,
                meilleur_gain,
                utilisations
            )

            if meilleur_choix:
                meilleur_capteur = capteur
                meilleur_gain = gain

    return meilleur_capteur


def construire_glouton(
    capteur_depart,
    nb_capteurs,
    nb_zones,
    couvertures,
    couvertures_ensembles,
    capteurs_tabous,
    utilisations
):
    configuration = [capteur_depart]
    capteurs_choisis = {capteur_depart}
    capteurs_tabous = set(capteurs_tabous)

    zones_deja_couvertes = couvertures_ensembles[capteur_depart - 1].copy()

    while len(zones_deja_couvertes) < nb_zones:
        meilleur_capteur = choisir_meilleur_capteur(
            nb_capteurs,
            zones_deja_couvertes,
            couvertures_ensembles,
            capteurs_choisis,
            capteurs_tabous,
            utilisations
        )

        if meilleur_capteur is None:
            return None

        configuration.append(meilleur_capteur)
        capteurs_choisis.add(meilleur_capteur)
        zones_deja_couvertes.update(couvertures[meilleur_capteur - 1])

    return rendre_elementaire(configuration, couvertures, nb_zones)


def ajouter_configuration(configurations, configuration):
    if configuration is not None:
        configuration = sorted(configuration)

        if configuration not in configurations:
            configurations.append(configuration)


def mettre_a_jour_utilisations(configuration, utilisations):
    for capteur in configuration:
        utilisations[capteur] += 1


def trouver_capteur_le_plus_utilise(configuration, utilisations):
    capteur_le_plus_utilise = None

    for capteur in configuration:
        premier_capteur_teste = capteur_le_plus_utilise is None

        if premier_capteur_teste:
            capteur_le_plus_utilise = capteur
        else:
            capteur_plus_utilise = (
                utilisations[capteur] > utilisations[capteur_le_plus_utilise]
            )

            if capteur_plus_utilise:
                capteur_le_plus_utilise = capteur

    return capteur_le_plus_utilise


def ajouter_paires_et_triplets(
    configurations,
    nb_capteurs,
    nb_zones,
    couvertures_ensembles
):
    toutes_les_zones = set(range(1, nb_zones + 1))

    configurations_connues = {
        tuple(configuration)
        for configuration in configurations
    }

    for premier in range(nb_capteurs):
        for second in range(premier + 1, nb_capteurs):
            couverture_paire = (
                couvertures_ensembles[premier]
                | couvertures_ensembles[second]
            )

            paire_couvre_tout = couverture_paire == toutes_les_zones

            if paire_couvre_tout:
                configurations_connues.add((premier + 1, second + 1))

    if nb_capteurs >= 500:
        generateur = random.Random(42)
        print("Diversification : test de 500000 triplets...")

        for iteration in range(1, 500001):
            premier, second, troisieme = sorted(
                generateur.sample(range(nb_capteurs), 3)
            )

            couverture_premier_second = (
                couvertures_ensembles[premier]
                | couvertures_ensembles[second]
            )

            couverture_premier_troisieme = (
                couvertures_ensembles[premier]
                | couvertures_ensembles[troisieme]
            )

            couverture_second_troisieme = (
                couvertures_ensembles[second]
                | couvertures_ensembles[troisieme]
            )

            couverture_triplet = (
                couverture_premier_second
                | couvertures_ensembles[troisieme]
            )

            triplet_couvre_tout = couverture_triplet == toutes_les_zones

            aucune_paire_ne_couvre_tout = (
                couverture_premier_second != toutes_les_zones
                and couverture_premier_troisieme != toutes_les_zones
                and couverture_second_troisieme != toutes_les_zones
            )

            if triplet_couvre_tout and aucune_paire_ne_couvre_tout:
                configurations_connues.add(
                    (premier + 1, second + 1, troisieme + 1)
                )

            if iteration % 100000 == 0:
                print(iteration, "triplets testés")

    configurations_finales = [
        list(configuration)
        for configuration in sorted(configurations_connues)
    ]

    return configurations_finales


def generer_configurations(nb_capteurs, nb_zones, couvertures):
    configurations = []
    couvertures_ensembles = [set(zones) for zones in couvertures]
    utilisations = [0] * (nb_capteurs + 1)

    for capteur_depart in range(1, nb_capteurs + 1):
        configuration = construire_glouton(
            capteur_depart,
            nb_capteurs,
            nb_zones,
            couvertures,
            couvertures_ensembles,
            [],
            utilisations
        )

        ajouter_configuration(configurations, configuration)

        if configuration is not None:
            mettre_a_jour_utilisations(configuration, utilisations)

    liste_taboue = []
    taille_liste_taboue = min(5, max(1, nb_capteurs // 20))
    nb_iterations = min(500, nb_capteurs * 5)

    for iteration in range(nb_iterations):
        capteur_depart = iteration % nb_capteurs + 1
        depart_autorise = capteur_depart not in liste_taboue

        if depart_autorise:
            configuration = construire_glouton(
                capteur_depart,
                nb_capteurs,
                nb_zones,
                couvertures,
                couvertures_ensembles,
                liste_taboue,
                utilisations
            )

            if configuration is None:
                liste_taboue = []
            else:
                ajouter_configuration(configurations, configuration)
                mettre_a_jour_utilisations(configuration, utilisations)

                capteur_le_plus_utilise = trouver_capteur_le_plus_utilise(
                    configuration,
                    utilisations
                )

                if capteur_le_plus_utilise is not None:
                    liste_taboue.append(capteur_le_plus_utilise)

                liste_trop_longue = len(liste_taboue) > taille_liste_taboue

                if liste_trop_longue:
                    liste_taboue.pop(0)

    return ajouter_paires_et_triplets(
        configurations,
        nb_capteurs,
        nb_zones,
        couvertures_ensembles
    )


def afficher_configurations(configurations):
    limite_affichage = 50

    print("\nConfigurations élémentaires générées :", len(configurations))

    for i in range(min(len(configurations), limite_affichage)):
        print("u" + str(i + 1), "=", configurations[i])

    if len(configurations) > limite_affichage:
        nb_configurations_cachees = len(configurations) - limite_affichage

        print(
            "...",
            nb_configurations_cachees,
            "configurations non affichées"
        )