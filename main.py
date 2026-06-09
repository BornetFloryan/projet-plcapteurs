import argparse
from pathlib import Path

from lecture_instance import lire_instance, afficher_instance
from generation_configuration import generer_configurations, afficher_configurations
from programme_lineaire import ecrire_programme_lp
from glpk import resoudre_avec_glpk, lire_solution, afficher_solution


def lire_arguments():
    parser = argparse.ArgumentParser(
        description="Maximise la durée de vie d'un réseau de capteurs."
    )

    parser.add_argument(
        "instance",
        help="fichier d'instance à résoudre"
    )

    parser.add_argument(
        "--methode",
        choices=["exacte", "gloutonne"],
        required=True,
        help="méthode de génération des configurations"
    )

    return parser.parse_args()


def main():
    arguments = lire_arguments()
    fichier_instance = arguments.instance
    fichier_lp = "sorties/programme.lp"
    fichier_solution = "sorties/solution.txt"

    if not Path(fichier_instance).is_file():
        raise SystemExit(f"Erreur : fichier d'instance introuvable : {fichier_instance}")

    Path("sorties").mkdir(exist_ok=True)

    nb_capteurs, nb_zones, durees_vie, couvertures = lire_instance(fichier_instance)

    print("=== Instance lue ===")
    afficher_instance(nb_capteurs, nb_zones, durees_vie, couvertures)

    print("\nGénération des configurations en cours...")
    configurations = generer_configurations(
        nb_capteurs,
        nb_zones,
        couvertures,
        arguments.methode
    )
    print("Génération terminée.")
    afficher_configurations(configurations)

    print("\nÉcriture du programme linéaire en cours...")
    ecrire_programme_lp(nb_capteurs, durees_vie, configurations, fichier_lp)
    print("\nFichier LP écrit :", fichier_lp)

    print("Résolution avec GLPK en cours...")
    ok = resoudre_avec_glpk(fichier_lp, fichier_solution)

    if ok:
        valeur_objectif, valeurs_t = lire_solution(fichier_solution)
        afficher_solution(valeur_objectif, valeurs_t, configurations)


if __name__ == "__main__":
    main()