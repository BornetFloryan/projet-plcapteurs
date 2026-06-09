# Projet PL Capteurs

Projet de techniques d'optimisation portant sur le problème d'activation de capteurs pour la surveillance de zones.

Le programme permet de :

- lire une instance depuis un fichier texte ;
- générer des configurations élémentaires ;
- écrire le programme linéaire associé au format `.lp` ;
- résoudre ce programme avec GLPK ;
- afficher la durée de vie maximale obtenue.

## Installation de l'environnement Python

Créer un environnement virtuel :

```powershell
python -m venv .venv
```

Activer l'environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

## Installation de GLPK

Le programme utilise la commande `glpsol`.

Vérifier si GLPK est installé :

```powershell
glpsol --version
```

Si la commande n'est pas reconnue, il faut installer GLPK puis ajouter le dossier contenant `glpsol.exe` dans le `PATH` de Windows.

## Méthodes de génération

Le programme propose deux méthodes.

### Méthode exacte

La méthode exacte teste toutes les combinaisons de capteurs et conserve uniquement les configurations élémentaires.

Elle permet d'obtenir toutes les configurations élémentaires, mais elle devient trop coûteuse lorsque le nombre de capteurs est élevé.

### Méthode gloutonne

La méthode gloutonne construit rapidement des configurations élémentaires.

Elle part d'un capteur de départ, puis ajoute à chaque étape le capteur qui couvre le plus de nouvelles zones non encore couvertes.

Cette méthode est plus rapide, mais elle ne garantit pas de trouver toutes les configurations élémentaires possibles.

Sur les grandes instances, une progression est affichée tous les 100 capteurs de
départ testés.

## Lancer les instances

### Instance 1 : fichier-exemple

```powershell
python main.py instances/fichier-exemple.txt --methode gloutonne
```

### Instance 2 : moyen_test_2

```powershell
python main.py instances/moyen_test_2.txt --methode gloutonne
```

### Instance 3 : moyen_test_3

```powershell
python main.py instances/moyen_test_3.txt --methode gloutonne
```

### Instance 4 : gros_test_1

```powershell
python main.py instances/gros_test_1.txt --methode gloutonne
```

### Instance 5 : maxi_test_1

```powershell
python main.py instances/maxi_test_1.txt --methode gloutonne
```

## Méthode utilisée

La méthode gloutonne peut être utilisée sur toutes les instances. Elle permet
d'obtenir rapidement des configurations utiles sans tester toutes les
combinaisons possibles.

La méthode exacte reste disponible pour comparer les résultats sur les petites
instances, mais elle devient trop coûteuse lorsque le nombre de capteurs
augmente.

Pour résoudre une instance, on utilise donc l'option :

```powershell
--methode gloutonne
```

## Fichiers générés

Après l'exécution, le programme crée le dossier `sorties` contenant :

```text
sorties/programme.lp
sorties/solution.txt
```

Le fichier `programme.lp` contient le programme linéaire écrit automatiquement.

Le fichier `solution.txt` contient la solution produite par GLPK.

## Structure du projet

```text
projet-plcapteurs/
│
├── instances/
│   ├── fichier-exemple.txt
│   ├── moyen_test_2.txt
│   ├── moyen_test_3.txt
│   ├── gros_test_1.txt
│   └── maxi_test_1.txt
│
├── sorties/
│
├── main.py
├── lecture_instance.py
├── couverture.py
├── generation_exacte.py
├── generation_gloutonne.py
├── generation_configuration.py
├── programme_lineaire.py
├── glpk.py
└── README.md
```

```

```
