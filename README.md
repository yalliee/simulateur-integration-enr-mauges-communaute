# Simulateur ENR des Mauges

Ce dossier contient une maquette interactive qui permet d'explorer des scénarios de développement du solaire et de l'éolien dans Mauges Communauté. Elle compare la production renouvelable à la consommation, estime les effets de solutions de flexibilité et présente des indicateurs, des graphiques et une carte des postes sources.

## Fichiers du dossier

| Fichier | Rôle |
| --- | --- |
| `maquette_Imran.html` | Maquette légère actuellement utilisée. Elle contient l'interface, le moteur JavaScript de simulation et charge les données depuis `data.js`. |
| `data.js` | Données nécessaires à la maquette : paramètres, profils et scénarios, géographie, et séries horaires encodées. |
| `maquette_v0.html` | Ancienne version autonome, plus volumineuse, dans laquelle les données sont intégrées directement au HTML. Elle ne reflète pas nécessairement les dernières modifications de l'interface. |
| `extraire.py` | Script permettant d'extraire les blocs de données `META`, `GEO` et `BIN` d'un HTML source pour créer `data.js` et une version HTML allégée. |

## Lancer la maquette

1. Garder `maquette_Imran.html` et `data.js` dans le même dossier.
2. Ouvrir `maquette_Imran.html` dans un navigateur récent.
3. Une connexion Internet est nécessaire pour charger les bibliothèques et ressources externes : Leaflet, ECharts, les fonds de carte et les polices. Sans fond de carte, les autres fonctions du simulateur restent disponibles.

Aucune installation de dépendances locales ni étape de compilation n'est nécessaire.

## Accéder au simulateur en ligne

Le workflow GitHub Actions publie `maquette_Imran.html` et `data.js` sur GitHub Pages à chaque modification de ces fichiers sur `main`. La page est accessible à l'adresse <https://yalliee.github.io/simulateur-integration-enr-mauges-communaute/> après activation de GitHub Pages dans les paramètres du dépôt et réussite du premier déploiement.

## Utilisation

### Vues

- **Élu** : résumé du scénario, indicateurs, verdict, journée type, carte et bilan mensuel.
- **Démo** : parcours guidé de scénarios, avec navigation par boutons ou touches fléchées.
- **Expert** : série horaire sur deux semaines, formulaire complet des hypothèses et comparaison des années météo.

Les vues **Élu**, **Démo** et **Expert**, ainsi que l'année météo, se choisissent dans l'en-tête ou dans la barre de commandes fixe en bas de l'écran. En **Démo**, le panneau de présentation est décalé pour laisser cette barre accessible. Les flèches sous l'en-tête replient ou ouvrent les barres latérales **Réglages** et **Affichage**.

### Réglages et résultats

La barre **Réglages** permet de choisir un scénario prédéfini ou de modifier le solaire, l'éolien, une batterie, le déplacement de la chauffe des ballons, le pilotage des véhicules électriques, le plafond d'injection solaire et l'horizon de consommation.

Le résumé du scénario affiche les puissances solaire et éolienne en MW ainsi que leur évolution en pourcentage par rapport au parc actuel. Les indicateurs clés sont réordonnés ainsi : énergie produite, taux de couverture, surplus/déficit, énergie perdue, heures de vigilance réseau, pointes d'injection et investissement batterie. Le bouton œil masque ou rétablit chaque indicateur ; le bouton d'information explique comment l'interpréter.

La barre **Affichage** contrôle la visibilité des textes, graphiques et éléments de la vue expert. La carte utilise par défaut le relief Esri topo ; OpenStreetMap reste disponible comme fond alternatif. Elle permet également d'afficher ou non les postes sources et d'activer la densité ENR. Les icônes d'information de la carte détaillent le calcul de densité par commune (puissance PV + éolien du scénario divisée par la surface) et l'estimation de la charge des postes (occupation actuelle plus ajout estimé selon les multiplicateurs, rapportés à la capacité réservée).

Les préférences d'affichage et d'état des barres latérales sont mémorisées dans le stockage local du navigateur.

## Fonctionnement et données

Le moteur JavaScript simule les séries horaires pour l'année sélectionnée. Les années disponibles sont 2021 à 2025 ; 2024 comprend 8 784 heures, les autres 8 760. Les calculs incluent notamment la production, la consommation, les flexibilités, le stockage, l'énergie échangée avec le réseau, l'écrêtement et les pointes.

`data.js` expose trois constantes JavaScript :

- `META` : années, nombre d'heures, noms et format des colonnes, constantes, profils, paramètres et scénarios ;
- `GEO` : données géographiques des communes et postes sources ;
- `BIN` : séries horaires encodées en Base64, une entrée par année.

Les séries sont au format Float32 little-endian. Le code de la maquette les décode et les utilise pour alimenter le moteur et les visualisations.

Les sources indiquées dans la maquette comprennent ODRÉ, Enedis, RTE Eco2Mix, Météo-France, INSEE et Caparéseau. Les références économiques citées sont NREL, RTE et CRE. Les contours communaux sont attribués à IGN/INSEE et les fonds de carte à leurs fournisseurs respectifs ; voir les crédits en bas de page.

## Compiler les rapports LaTeX

Les rapports `mon_rapport.tex` et `rapport_Thomas.tex` se compilent dans VS Code avec LaTeX Workshop : ouvrir le fichier `.tex`, puis lancer **Ctrl+Alt+B**. La recette pdfLaTeX est configurée par défaut. Les PDF sont générés directement dans ce dossier, à côté des fichiers `.tex` ; les fichiers auxiliaires sont rangés dans `out/`.

Les fichiers `.aux`, `.log`, `.out`, `.toc` et `.synctex.gz` sont des fichiers auxiliaires créés par LaTeX. Ils servent notamment aux références, aux signets, au diagnostic d'erreurs et à la synchronisation entre le code et le PDF. Il n'est pas nécessaire de les modifier ; le `.log` est à consulter en cas d'erreur de compilation.

## Extraction des données

`extraire.py` attend par défaut un fichier `maquette_Imran.backup.html` dans le dossier courant. Ce fichier n'est pas inclus dans le dossier actuel. Le HTML source doit contenir les déclarations JavaScript `const META = ...`, `const GEO = ...` et `const BIN = ...`.

Depuis PowerShell, après avoir placé ce fichier source dans le dossier :

```powershell
py extraire.py
```

Le script produit `maquette_Imran_clean.html` et `data.js`. Il écrit directement dans `data.js` : sauvegarder ce fichier au préalable si ses données doivent être conservées. Pour utiliser un autre nom de fichier source, appeler la fonction avec un chemin explicite :

```powershell
py -c "from extraire import extraire_donnees_maquette; extraire_donnees_maquette(r'mon_source.html')"
```

Les noms de fichiers de sortie peuvent également être passés à `extraire_donnees_maquette` (`fichier_html_sortie` et `fichier_data_js`).
