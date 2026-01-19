# Extracteur de Résultats de Courses de Ski

Ce projet contient un script Python pour extraire automatiquement les résultats de courses de ski depuis des fichiers PDF et les exporter en format CSV.

---

## 👋 Nouveau dans le monde de la programmation?

**Si vous n'êtes pas familier avec GitHub, Python ou les outils informatiques**, consultez d'abord notre [**Guide pour débutants**](GUIDE_DEBUTANT.md)! Ce guide vous explique pas à pas comment:
- Installer Python sur votre ordinateur
- Télécharger et utiliser ce projet
- Résoudre les problèmes courants

📖 **[Cliquez ici pour accéder au Guide pour débutants](GUIDE_DEBUTANT.md)**

---

## Fonctionnalités

- 📄 Extraction automatique des données depuis des PDFs de résultats de courses générés par LiveTiming
- 📊 Génération d'un fichier CSV avec toutes les informations pertinentes pour analyse dans Excel
- 🇫🇷 Format décimal français (virgule au lieu de point)
- 📁 **Traitement par dossier**: Traitez tous les PDFs d'un dossier en une seule commande (récursif)
- 📈 Calcul automatique des temps en secondes et des notes de performance
- 📋 Résumé détaillé du traitement avec liste des succès et échecs

## À propos des fichiers source (LiveTiming)

Ce script traite les fichiers PDF générés par les systèmes de chronométrage **LiveTiming** utilisés lors des compétitions de ski. Ces systèmes sont couramment utilisés par:

- **SKIBEC** (Fédération de ski acrobatique du Québec)
- **SQA** (Ski Québec Alpin)
- Clubs de ski régionaux (Mont-Sainte-Anne, Stoneham, Relais, etc.)

### Systèmes compatibles

Le script est compatible avec les PDFs générés par:
- **Split Second Ver. 8.08 Rev. 4** - Système de chronométrage professionnel
- **TAG HEUER CP 540** - Chronométrage haute précision
- **LiveTiming Race Results** - Format standard utilisé au Québec

### Format typique des PDFs LiveTiming

Les PDFs de résultats LiveTiming contiennent généralement:
- **En-tête**: Date, lieu, type de compétition (ex: GRANDS CIRCUITS SLALOM 1)
- **Catégorie**: Genre (Masculin/Féminin) et classe d'âge (U12, U14, etc.)
- **Tableau de résultats**: Avec colonnes standardisées (Rang, Dossard, Nom, AN, Classe, Club, NAT, Temps, Écart)
- **Métadonnées**: Heure de début, système de chronométrage, conditions météo

### Où obtenir ces fichiers?

Les fichiers PDF LiveTiming sont généralement disponibles:
- Sur les sites web des clubs de ski après chaque course
- Par courriel aux entraîneurs et officiels
- Sur les plateformes de résultats en ligne (ex: live.skibec.ca)
- Téléchargement direct depuis le système LiveTiming lors des événements

## Informations extraites

Le script extrait les informations suivantes pour chaque course:

### Informations générales
- **Date**: Date de la compétition
- **Lieu**: Lieu de la course (ex: STONEHAM)
- **Type de compétition**: Description de l'événement (ex: GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ)

### Résultats individuels
- **Rang**: Position du compétiteur
- **Dossard**: Numéro de dossard
- **Nom**: Nom du compétiteur
- **Année**: Année de naissance
- **Club**: Club d'appartenance
- **Temps**: Temps réalisé (format original: 36,16 ou 1:02,92)
- **Temps (secondes)**: Temps converti en secondes (36,16 ou 62,92)
- **Écart**: Écart avec le premier (format avec virgule)
- **Note**: Valeur numérique de performance calculée avec la formule: (1 - écart/temps) × 100 (ex: 93,79 pour 93,79%)

## Installation

### Prérequis
- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou directement:

```bash
pip install pdfplumber
```

## Utilisation

### Structure des dossiers

Placez vos fichiers PDF de résultats dans le répertoire `courses/` avec la structure suivante:

```
résultats/
├── courses/
│   ├── Sl-Stoneham/
│   │   ├── 298137 Race Results.pdf
│   │   ├── 298139 Race Results.pdf
│   │   ├── Stoneham_2026-01-18_Slalom1_F.csv  (généré)
│   │   ├── Stoneham_2026-01-18_Slalom2_F.csv  (généré)
│   │   └── ...
│   └── Autre-Lieu/
│       └── ...
├── extracteur_resultats.py
├── requirements.txt
└── README.md
```

### Exécution du script

Le script s'utilise en ligne de commande et accepte deux modes d'utilisation:

#### Mode 1: Traiter un fichier PDF unique

```bash
python3 extracteur_resultats.py <chemin_vers_fichier_pdf>
```

**Exemples:**

```bash
# Avec guillemets (recommandé pour les noms avec espaces)
python3 extracteur_resultats.py "courses/Sl-Stoneham/298137 Race Results.pdf"

# Avec échappement des espaces
python3 extracteur_resultats.py courses/Sl-Stoneham/298137\ Race\ Results.pdf
```

**Sortie:**
```
Mode: Fichier unique
Fichier: courses/Sl-Stoneham/298137 Race Results.pdf

Traitement de courses/Sl-Stoneham/298137 Race Results.pdf...
  ✓ 47 résultats extraits

Génération du fichier CSV: courses/Sl-Stoneham/Stoneham_2026-01-18_Slalom1_F.csv
✓ Fichier CSV généré avec succès

✅ Traitement terminé!
```

#### Mode 2: Traiter tous les PDFs d'un dossier (NOUVEAU!)

```bash
python3 extracteur_resultats.py <chemin_vers_dossier>
```

**Exemples:**

```bash
# Traiter tous les PDFs du dossier Sl-Stoneham
python3 extracteur_resultats.py courses/Sl-Stoneham

# Traiter tous les PDFs de tous les sous-dossiers dans courses
python3 extracteur_resultats.py courses
```

**Sortie:**
```
Mode: Dossier
Dossier: courses/Sl-Stoneham

📄 4 fichier(s) PDF trouvé(s):
  - 298137 Race Results.pdf
  - 298138 Race Results.pdf
  - 298139 Race Results.pdf
  - 298140 Race Results.pdf

======================================================================
DÉBUT DU TRAITEMENT
======================================================================

[1/4] 298137 Race Results.pdf
  ✓ 47 résultats extraits
  ✓ CSV généré

[2/4] 298138 Race Results.pdf
  ✓ 37 résultats extraits
  ✓ CSV généré

... (suite)

======================================================================
RÉSUMÉ DU TRAITEMENT
======================================================================

✅ Fichiers traités avec succès: 4/4

Fichiers CSV générés:
  ✓ 298137 Race Results.pdf → Stoneham_2026-01-18_Slalom1_F.csv
  ✓ 298138 Race Results.pdf → Stoneham_2026-01-18_Slalom2_M.csv
  ✓ 298139 Race Results.pdf → Stoneham_2026-01-18_Slalom2_F.csv
  ✓ 298140 Race Results.pdf → Stoneham_2026-01-18_Slalom1_M.csv

📁 Dossier de sortie: courses/Sl-Stoneham
```

**Avantages du mode dossier:**
- ⚡ Traite tous les PDFs en une seule commande
- 📊 Affiche un résumé complet du traitement
- 🔍 Recherche récursive dans tous les sous-dossiers
- ✅ Continue même si un fichier échoue
- 📝 Liste les succès et échecs à la fin

### Comment ça fonctionne

Le script va:
1. Lire et analyser le(s) fichier(s) PDF spécifié(s)
2. Extraire les informations (date, lieu, type, résultats)
3. Générer un fichier CSV avec un nom descriptif dans le **même répertoire** que le PDF source

**Format du nom de fichier CSV généré:**
```
Lieu_Date_Slalom[N]_[Type].csv
```

Exemples:
- `Stoneham_2026-01-18_Slalom1_F.csv` (Slalom 1 Féminin)
- `Stoneham_2026-01-18_Slalom2_M.csv` (Slalom 2 Masculin)

### Exemple de sortie

```
======================================================================
EXTRACTEUR DE RÉSULTATS DE COURSES DE SKI
======================================================================

Fichier à traiter: courses/Sl-Stoneham/298137 Race Results.pdf

Traitement de courses/Sl-Stoneham/298137 Race Results.pdf...
  ✓ 47 résultats extraits

Génération du fichier CSV: courses/Sl-Stoneham/Stoneham_2026-01-18_Slalom1_F.csv
✓ Fichier CSV généré avec succès: courses/Sl-Stoneham/Stoneham_2026-01-18_Slalom1_F.csv

✅ Traitement terminé!
📁 Répertoire: courses/Sl-Stoneham
📄 Fichier CSV: Stoneham_2026-01-18_Slalom1_F.csv
```

### Ancienne méthode de traitement par lots (optionnelle)

Si vous préférez utiliser des boucles shell plutôt que le mode dossier intégré:

```bash
# Traiter tous les PDFs dans un répertoire (non récursif)
for pdf in courses/Sl-Stoneham/*.pdf; do
    python3 extracteur_resultats.py "$pdf"
done

# Traiter tous les PDFs récursivement avec find
find courses -name "*.pdf" -exec python3 extracteur_resultats.py {} \;
```

**Note:** Le mode dossier intégré (voir ci-dessus) est maintenant recommandé car il offre un meilleur résumé et une meilleure gestion des erreurs.

## Format du fichier CSV pour Excel

Le fichier CSV généré est optimisé pour une ouverture directe dans Excel avec les bons paramètres:

### Spécifications techniques

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| **Séparateur de colonnes** | Point-virgule (`;`) | Standard français/européen pour CSV |
| **Séparateur décimal** | Virgule (`,`) | Format décimal français (37,58 au lieu de 37.58) |
| **Encodage** | UTF-8 avec BOM | Assure l'affichage correct des accents (é, è, à, ô) dans Excel |
| **Fin de ligne** | CRLF (`\r\n`) | Compatible Windows et Mac |
| **Guillemets** | Aucun (sauf si nécessaire) | Fichier propre et lisible |

### Pourquoi ces choix?

**Point-virgule au lieu de virgule:**
- En français, la virgule est le séparateur décimal (37,58)
- Si on utilisait la virgule comme séparateur de colonnes, Excel ne pourrait pas distinguer entre "37,58" (un nombre) et "37,58" (deux colonnes)
- Le point-virgule est le standard pour les CSV francophones

**UTF-8 avec BOM:**
- Le BOM (Byte Order Mark) est un marqueur invisible au début du fichier
- Il indique à Excel que le fichier est en UTF-8
- Sans le BOM, Excel pourrait interpréter les accents incorrectement
- Avec le BOM, "Léa" s'affiche correctement au lieu de "LÃ©a"

**Format décimal avec virgule:**
- Respect des normes françaises et québécoises
- Compatible avec les formules Excel en français
- `=MOYENNE(J2:J50)` fonctionnera correctement avec 37,58
- Cohérent avec le système d'exploitation configuré en français

### Exemple de contenu

```csv
Date;Lieu;Type de compétition;Rang;Dossard;Nom;Année;Club;Temps;Temps (secondes);Écart;Note
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;1;38;Léa, Doyon;2014;REL;37,58;37,58;0,00;100,00
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;2;15;Mélya, Ménard;2015;REL;40,07;40,07;2,49;93,79
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;48;12;Alice, Pronovost;2015;MASS;1:02,92;62,92;25,34;59,73
```

### Description détaillée des colonnes

Le fichier CSV généré contient **12 colonnes** pour faciliter l'analyse dans Excel, Google Sheets ou tout autre tableur:

| # | Colonne | Type | Description | Exemple |
|---|---------|------|-------------|---------|
| 1 | **Date** | Texte | Date complète de la compétition avec jour de la semaine | `Dimanche 1/18/2026` |
| 2 | **Lieu** | Texte | Nom de la station de ski où s'est déroulée la course | `STONEHAM` |
| 3 | **Type de compétition** | Texte | Description complète de l'épreuve et catégorie | `GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ` |
| 4 | **Rang** | Nombre | Position finale du compétiteur (1 = premier) | `1`, `2`, `48` |
| 5 | **Dossard** | Nombre | Numéro de dossard porté pendant la course | `38`, `15`, `12` |
| 6 | **Nom** | Texte | Prénom et nom du compétiteur (format: Prénom, Nom) | `Léa, Doyon` |
| 7 | **Année** | Nombre | Année de naissance du compétiteur | `2014`, `2015` |
| 8 | **Club** | Texte | Code du club d'appartenance (3-4 lettres) | `REL`, `MSA`, `STON`, `MASS` |
| 9 | **Temps** | Texte | Temps original tel qu'affiché dans le PDF LiveTiming | `37,58` ou `1:02,92` |
| 10 | **Temps (secondes)** | Nombre | Temps converti en secondes décimales pour calculs Excel | `37,58` ou `62,92` |
| 11 | **Écart** | Nombre | Écart de temps avec le premier (en secondes) | `0,00`, `2,49`, `25,34` |
| 12 | **Note** | Nombre | Performance relative en pourcentage: (1 - écart/temps) × 100 | `100,00`, `93,79`, `59,73` |

### Utilisation des colonnes dans Excel

**Pour l'analyse statistique:**
- Utilisez **Temps (secondes)** pour calculer moyennes, médianes, écarts-types
- Utilisez **Note** pour comparer les performances entre différentes courses
- Triez par **Rang** pour voir le classement officiel
- Triez par **Note** pour voir les meilleures performances relatives

**Pour les filtres:**
- Filtrez par **Lieu** pour analyser les résultats par station
- Filtrez par **Club** pour voir les résultats d'un club spécifique
- Filtrez par **Année** pour comparer les catégories d'âge (2014 vs 2015)

**Pour les graphiques:**
- Graphique en barres: **Nom** (axe X) vs **Note** (axe Y) pour visualiser les performances
- Graphique temporel: **Date** (axe X) vs **Note** (axe Y) pour suivre la progression d'un athlète
- Graphique de dispersion: **Temps (secondes)** vs **Écart** pour identifier les tendances

### Codes de clubs courants

Voici les codes des clubs de ski les plus fréquents dans les résultats:

| Code | Club | Région |
|------|------|--------|
| **REL** | Le Relais | Lac-Beauport |
| **MSA** | Mont-Sainte-Anne | Beaupré |
| **STON** | Stoneham | Stoneham-et-Tewkesbury |
| **MASS** | Massif de Charlevoix | Petite-Rivière-Saint-François |
| **ADS** | Adstock | Adstock |
| **MGF** | Mont-Grand-Fonds | La Malbaie |

### Conversion automatique des temps

La colonne "Temps (secondes)" convertit automatiquement tous les temps en secondes:
- `36,12` secondes → `36,12` (déjà en secondes)
- `1:02,30` (1 minute 2,30 sec) → `62,30` secondes
- `1:23,45` (1 minute 23,45 sec) → `83,45` secondes

### Calcul automatique de la note

La colonne "Note" calcule le pourcentage de performance par rapport au meilleur temps:

**Formule:** `Note = (1 - écart/temps) × 100`

**Exemples:**
- Temps: 37,58 sec, Écart: 0,00 sec → Note: **100,00** (premier, 100%)
- Temps: 40,07 sec, Écart: 2,49 sec → Note: **93,79** (93,79%)
- Temps: 62,92 sec, Écart: 25,34 sec → Note: **59,73** (59,73%)

**Note:** La valeur est stockée comme nombre décimal (ex: `93,79`) pour faciliter les calculs dans Excel. Vous pouvez formater la colonne en pourcentage dans Excel si vous le souhaitez.

#### Pourquoi utiliser une note en pourcentage?

La note en pourcentage permet de **comparer les performances entre différentes compétitions**, ce que l'écart de temps seul ne permet pas. Les temps de compétition changent toujours selon:
- Les conditions météo (neige, température)
- La difficulté du tracé
- Le nombre de portes
- L'état de la piste

**Exemple concret:**
- **Course 1**: Un athlète a un écart de 3,5 secondes sur un temps de 45 sec → Note: **92,22**
- **Course 2**: Le même athlète a un écart de 2,8 secondes sur un temps de 35 sec → Note: **92,00**

Même si l'écart absolu a diminué (3,5 → 2,8 sec), la note révèle une performance légèrement moins bonne. Le pourcentage permet de **voir la vraie amélioration d'une compétition à l'autre**, indépendamment des conditions de course.

## Ouverture du fichier CSV

Le fichier peut être ouvert avec:
- **Excel**: Utiliser "Données > Importer un fichier texte" et spécifier:
  - Séparateur: point-virgule
  - Format décimal: virgule
- **LibreOffice Calc**: S'ouvre automatiquement avec les bons paramètres
- **Google Sheets**: Importer le fichier en spécifiant le séparateur point-virgule

## Compatibilité

Le script est compatible avec les PDFs de résultats générés par:
- Split Second Ver. 8.08 Rev. 4
- TAG HEUER CP 540

Format typique des PDFs traités:
- GRANDS CIRCUITS SLALOM
- Résultats SKIBEC/SQA
- Format de tableau standard avec colonnes: Rang, Dossard, Nom, AN, Classe, Club, NAT, Temps, Écart

## Dépannage

### Usage sans paramètre

Si vous lancez le script sans paramètre:
```bash
python3 extracteur_resultats.py
```

Vous verrez:
```
Usage: python3 extracteur_resultats.py <fichier_pdf>

Exemple:
  python3 extracteur_resultats.py "courses/Sl-Stoneham/298137 Race Results.pdf"
```

### Fichier introuvable

Si le script ne trouve pas le fichier:
```
❌ Erreur: Le fichier 'chemin/vers/fichier.pdf' n'existe pas.
```

Vérifiez:
- Le chemin est correct (absolu ou relatif)
- Le fichier existe bien à cet emplacement
- Utilisez des guillemets pour les noms avec espaces

### Aucun résultat extrait

Si le script ne trouve aucun résultat:
```
⚠️  Aucun résultat extrait du PDF.
```

Vérifiez que:
- Le PDF suit le format standard SKIBEC/SQA
- Le PDF n'est pas protégé ou chiffré
- Le PDF contient bien des résultats de course

### Erreurs d'encodage

Les caractères accentués sont maintenant correctement encodés en UTF-8 avec BOM. Si vous voyez des caractères étranges:

**Dans Excel:**
- Le fichier devrait s'ouvrir correctement automatiquement
- Si les accents ne s'affichent pas: Données > Importer > Fichier texte > Choisir UTF-8

**Dans un éditeur de texte:**
- Utilisez un éditeur qui supporte UTF-8 (VS Code, Notepad++, Sublime Text)
- Vérifiez que l'encodage est bien UTF-8 dans les paramètres de l'éditeur

**Dans le terminal:**
- Assurez-vous que votre terminal supporte UTF-8
- Sur Mac/Linux: `export LANG=fr_CA.UTF-8` ou `export LANG=fr_FR.UTF-8`

## Licence

Ce script est fourni tel quel pour un usage personnel.

## Auteur

Script créé pour faciliter l'analyse des résultats de courses de ski.
