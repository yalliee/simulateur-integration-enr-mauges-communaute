# Simulateur ENR des Mauges

Ce dossier contient une maquette interactive qui permet d'explorer des scénarios de développement du solaire et de l'éolien dans Mauges Communauté. Elle compare la production renouvelable à la consommation, estime les effets de solutions de flexibilité et présente des indicateurs, des graphiques et une carte des postes sources.

## Fichiers du dossier

| Fichier | Rôle |
| --- | --- |
| `maquette_quetinn.html` | Version de référence et version publiée sur GitHub Pages. Elle correspond au code de production de Quetinn, à un saut de ligne final près. |
| `maquette_Imran.html` | Ancienne version de la maquette, conservée pour servir de base aux prochaines modifications à partir de la version de référence. Elle charge ses données depuis `data.js`. |
| `data.js` | Données du simulateur : paramètres, profils et scénarios, géographie et séries horaires encodées. |
| `index.html` | Point d'entrée GitHub Pages : redirige vers `maquette_quetinn.html`. |
| `precalcul.js` | Précalculs nécessaires aux trajectoires et à l'analyse de sensibilité de `maquette_quetinn.html`. |
| `vendor/` | Bibliothèques JavaScript, feuilles de style et polices utilisées localement par `maquette_quetinn.html`. Les licences d'ECharts et de Leaflet sont conservées dans leurs sous-dossiers. |
| `maquette_v0.html` | Ancienne version autonome, plus volumineuse, dans laquelle les données sont intégrées directement au HTML. Elle ne reflète pas nécessairement les dernières modifications de l'interface. |
| `extraire.py` | Script permettant d'extraire les blocs de données `META`, `GEO` et `BIN` d'un HTML source pour créer `data.js` et une version HTML allégée. |

## Lancer le simulateur

Garder `maquette_quetinn.html`, `data.js`, `precalcul.js` et le dossier `vendor/` côte à côte, puis ouvrir `maquette_quetinn.html` dans un navigateur récent. Les scripts, feuilles de style et polices sont chargés localement ; seule la carte de fond nécessite Internet. Aucun serveur ni compilation n'est nécessaire.

Les ressources de `vendor/` et `precalcul.js` proviennent du dossier [`app/` du dépôt public simulateur-mauges de Quetinn](https://github.com/quetinn/simulateur-mauges/tree/main/app). Elles ont été vérifiées par rapport aux fichiers de ce dépôt ; les licences fournies avec ECharts et Leaflet sont conservées.

## Accéder au simulateur en ligne

Le site public est disponible à l'adresse <https://yalliee.github.io/simulateur-integration-enr-mauges-communaute/>. Son `index.html` redirige vers `maquette_quetinn.html`. Le workflow GitHub Actions publie la maquette, ses données, ses précalculs et le dossier `vendor/` à chaque modification de ces fichiers sur `main`.

## Utilisation

### Vues

- **Élu** : résumé du scénario, indicateurs, verdict, journée type, carte et bilan mensuel.
- **Démo** : parcours guidé en cinq étapes, utilisable au clavier ou avec les boutons.
- **Expert** : analyse horaire, trajectoires, sensibilité, hypothèses détaillées, indicateurs par année et export CSV/JSON.

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

Le rapport `rapport_Thomas.tex` se compile dans VS Code avec LaTeX Workshop : ouvrir le fichier `.tex`, puis lancer **Ctrl+Alt+B**. La recette pdfLaTeX est configurée par défaut. Le PDF est généré dans ce dossier ; les fichiers auxiliaires sont rangés dans `out/`.

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
