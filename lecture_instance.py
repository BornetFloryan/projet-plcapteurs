def lire_instance(nom_fichier):
    """
    Lit le fichier d'instance.

    Format du fichier :
    ligne 1 : nombre de capteurs
    ligne 2 : nombre de zones
    ligne 3 : durees de vie des capteurs
    lignes suivantes : zones couvertes par chaque capteur
    """

    fichier = open(nom_fichier, "r", encoding="utf-8")
    lignes = fichier.readlines()
    fichier.close()

    lignes_propres = []
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne != "":
            lignes_propres.append(ligne)

    nb_capteurs = int(lignes_propres[0])
    nb_zones = int(lignes_propres[1])

    durees = lignes_propres[2].split()
    durees_vie = []

    for duree in durees:
        durees_vie.append(float(duree))

    couvertures = []

    for i in range(nb_capteurs):
        ligne_zones = lignes_propres[3 + i]
        zones_texte = ligne_zones.split()

        zones = []
        for zone in zones_texte:
            zones.append(int(zone))

        couvertures.append(zones)

    return nb_capteurs, nb_zones, durees_vie, couvertures


def afficher_instance(nb_capteurs, nb_zones, durees_vie, couvertures):
    limite_affichage = 20

    print("Nombre de capteurs :", nb_capteurs)
    print("Nombre de zones :", nb_zones)
    print("Durées de vie :", durees_vie[:limite_affichage])

    if nb_capteurs > limite_affichage:
        print("...", nb_capteurs - limite_affichage, "durées non affichées")

    print("\nZones couvertes par chaque capteur :")
    for i in range(min(nb_capteurs, limite_affichage)):
        zones = couvertures[i]
        print("Capteur", i + 1, "->", zones[:limite_affichage], end="")

        if len(zones) > limite_affichage:
            print(" ...", len(zones) - limite_affichage, "zones non affichées")
        else:
            print()

    if nb_capteurs > limite_affichage:
        print("...", nb_capteurs - limite_affichage, "capteurs non affichés")
