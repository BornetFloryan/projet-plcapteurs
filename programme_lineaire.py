def ecrire_programme_lp(nb_capteurs, durees_vie, configurations, nom_fichier):
    fichier = open(nom_fichier, "w", encoding="utf-8")

    fichier.write("Maximize\n")
    fichier.write(" obj: ")

    for i in range(len(configurations)):
        if i > 0:
            fichier.write(" + ")
        fichier.write("t" + str(i + 1))

    fichier.write("\n")

    fichier.write("Subject To\n")

    for capteur in range(1, nb_capteurs + 1):
        variables = []

        for i in range(len(configurations)):
            configuration = configurations[i]

            if capteur in configuration:
                variables.append("t" + str(i + 1))

        if len(variables) > 0:
            fichier.write(" c" + str(capteur) + ": ")

            for j in range(len(variables)):
                if j > 0:
                    fichier.write(" + ")
                fichier.write(variables[j])

            fichier.write(" <= " + str(durees_vie[capteur - 1]) + "\n")

    fichier.write("Bounds\n")

    for i in range(len(configurations)):
        fichier.write(" t" + str(i + 1) + " >= 0\n")

    fichier.write("End\n")

    fichier.close()