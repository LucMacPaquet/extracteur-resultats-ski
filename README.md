# Extracteur de Résultats de Courses de Ski

Ce projet contient un script Python pour extraire automatiquement les résultats de courses de ski depuis des fichiers PDF et les exporter en format CSV.

## Fonctionnalités

- 📄 Extraction automatique des données depuis des PDFs de résultats de courses
- 📊 Génération d'un fichier CSV avec toutes les informations pertinentes
- 🇫🇷 Format décimal français (virgule au lieu de point)
- 📁 Traitement par lots de tous les PDFs dans le répertoire `courses/`

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
- **Note**: Pourcentage calculé avec la formule: (1 - écart/temps) × 100

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

Le script s'utilise en ligne de commande en spécifiant le fichier PDF à traiter:

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

Le script va:
1. Lire et analyser le fichier PDF spécifié
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

### Traitement par lots

Pour traiter plusieurs PDFs, utilisez une boucle shell:

```bash
# Traiter tous les PDFs dans un répertoire
for pdf in courses/Sl-Stoneham/*.pdf; do
    python3 extracteur_resultats.py "$pdf"
done

# Traiter tous les PDFs récursivement
find courses -name "*.pdf" -exec python3 extracteur_resultats.py {} \;
```

## Format du fichier CSV

Le fichier CSV généré utilise:
- **Séparateur**: point-virgule (`;`)
- **Encodage**: UTF-8 avec BOM (meilleure compatibilité Excel)
- **Format décimal**: virgule (`,`) au lieu de point (`.`)
- **Caractères accentués**: Correctement encodés en UTF-8

### Exemple de contenu

```csv
Date;Lieu;Type de compétition;Rang;Dossard;Nom;Année;Club;Temps;Temps (secondes);Écart;Note
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;1;38;Léa, Doyon;2014;REL;37,58;37,58;0,00;100,00%
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;2;15;Mélya, Ménard;2015;REL;40,07;40,07;2,49;93,79%
Dimanche 1/18/2026;STONEHAM;GRANDS CIRCUITS SLALOM 1 - SLALOM FÉMININ;48;12;Alice, Pronovost;2015;MASS;1:02,92;62,92;25,34;59,73%
```

**Colonnes (12 au total):**
1. Date
2. Lieu
3. Type de compétition
4. Rang
5. Dossard
6. Nom
7. Année
8. Club
9. Temps (format original MM:SS,cc ou SS,cc)
10. Temps (secondes)
11. Écart
12. Note - **Nouvelle colonne!**

### Conversion automatique des temps

La colonne "Temps (secondes)" convertit automatiquement tous les temps en secondes:
- `36,12` secondes → `36,12` (déjà en secondes)
- `1:02,30` (1 minute 2,30 sec) → `62,30` secondes
- `1:23,45` (1 minute 23,45 sec) → `83,45` secondes

### Calcul automatique de la note

La colonne "Note" calcule le pourcentage de performance par rapport au meilleur temps:

**Formule:** `Note = (1 - écart/temps) × 100`

**Exemples:**
- Temps: 37,58 sec, Écart: 0,00 sec → Note: **100,00%** (premier)
- Temps: 40,07 sec, Écart: 2,49 sec → Note: **93,79%**
- Temps: 62,92 sec, Écart: 25,34 sec → Note: **59,73%**

#### Pourquoi utiliser une note en pourcentage?

La note en pourcentage permet de **comparer les performances entre différentes compétitions**, ce que l'écart de temps seul ne permet pas. Les temps de compétition changent toujours selon:
- Les conditions météo (neige, température)
- La difficulté du tracé
- Le nombre de portes
- L'état de la piste

**Exemple concret:**
- **Course 1**: Un athlète a un écart de 3,5 secondes sur un temps de 45 sec → **92,22%**
- **Course 2**: Le même athlète a un écart de 2,8 secondes sur un temps de 35 sec → **92,00%**

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
