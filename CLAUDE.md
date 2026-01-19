# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Vue d'ensemble du projet

Ce projet extrait automatiquement les résultats de courses de ski depuis des fichiers PDF et les exporte en format CSV. Le projet est entièrement en français et respecte les conventions de format français (virgule pour les décimales).

## Structure du projet

```
résultats/
├── courses/              # Répertoire contenant les PDFs de résultats
│   └── Sl-Stoneham/     # Sous-répertoire par lieu de course
│       └── *.pdf        # Fichiers PDF de résultats
├── extracteur_resultats.py  # Script principal d'extraction
├── requirements.txt     # Dépendances Python (pdfplumber)
├── resultats_courses.csv    # Fichier CSV généré (gitignored)
├── README.md           # Documentation utilisateur
└── CLAUDE.md           # Ce fichier

```

## Commandes principales

### Installation des dépendances
```bash
pip install -r requirements.txt
# ou directement: pip install pdfplumber
```

### Exécution du script principal

**Mode d'utilisation: Un fichier PDF à la fois**

```bash
python3 extracteur_resultats.py <chemin_vers_pdf>
```

**Exemples:**
```bash
# Traiter un seul PDF
python3 extracteur_resultats.py "courses/Sl-Stoneham/298137 Race Results.pdf"

# Traiter plusieurs PDFs en lot
for pdf in courses/Sl-Stoneham/*.pdf; do
    python3 extracteur_resultats.py "$pdf"
done

# Traiter tous les PDFs récursivement
find courses -name "*.pdf" -exec python3 extracteur_resultats.py {} \;
```

Le script:
1. Lit le fichier PDF spécifié en paramètre
2. Extrait les données (date, lieu, type, résultats)
3. Génère un fichier CSV avec un nom descriptif dans le **même répertoire** que le PDF

**Nom du fichier CSV généré:**
- Format: `Lieu_Date_Slalom[N]_[Type].csv`
- Exemple: `Stoneham_2026-01-18_Slalom1_F.csv`

### Test et débogage
```bash
# Voir les CSV générés dans un répertoire
ls -lh courses/Sl-Stoneham/*.csv

# Voir les premières lignes d'un CSV généré
head -20 "courses/Sl-Stoneham/Stoneham_2026-01-18_Slalom1_F.csv"

# Compter le nombre de résultats dans un CSV
wc -l "courses/Sl-Stoneham/Stoneham_2026-01-18_Slalom1_F.csv"
```

## Architecture du code

### extracteur_resultats.py

Le script est organisé en fonctions modulaires:

#### Fonctions d'extraction de métadonnées
- `extraire_date(texte)` : Extrait la date depuis le texte PDF
- `extraire_lieu(texte)` : Extrait le lieu de la course
- `extraire_type_competition(texte)` : Extrait le type de compétition (ex: GRANDS CIRCUITS SLALOM 1)
- `extraire_heure_debut(texte)` : Extrait l'heure de début de la course

#### Fonction d'extraction des résultats
- `extraire_resultats(texte)` : Parse les lignes de résultats avec regex
  - Pattern: `^\s*(\d+)\s+(\d+)\s+(.+?)\s+(20\d{2})\s+([A-D])\s+([A-Z]+)\s+U12\s+([\d:,\.]+)(?:\s+([\d:,\.]+))?\s*$`
  - Extrait: Rang, Dossard, Nom, Année, Classe, Club, Temps, Écart
  - Convertit automatiquement les points en virgules pour les décimales

#### Fonctions de traitement
- `traiter_pdf(chemin_pdf)` : Traite un fichier PDF complet
  - Utilise `pdfplumber` pour extraire le texte
  - Appelle toutes les fonctions d'extraction
  - Retourne un dictionnaire avec toutes les données

#### Fonctions utilitaires
- `nettoyer_nom_fichier(texte)` : Nettoie une chaîne pour un nom de fichier valide
  - Remplace les caractères invalides (/, :, etc.)
  - Remplace les espaces par des underscores

- `generer_nom_fichier_csv(donnees_course)` : Crée le nom du fichier CSV
  - Format: `Lieu_YYYY-MM-DD_Slalom[N]_[F/M].csv`
  - Extrait et formate la date, le numéro de slalom, le type
  - Exemple: `Stoneham_2026-01-18_Slalom1_F.csv`

#### Fonctions d'export
- `generer_csv(donnees_course, fichier_sortie)` : Génère le fichier CSV
  - Séparateur: point-virgule (`;`)
  - Encodage: UTF-8 avec BOM (utf-8-sig) pour compatibilité Excel
  - 11 colonnes (sans: Heure de début, Classe, Fichier source)
  - Nouvelle colonne: "Temps (secondes)" avec conversion automatique
  - Une ligne par résultat de compétiteur
  - Fichier créé dans le même répertoire que le PDF source
  - Gestion correcte des caractères accentués

#### Fonction principale
- `main()` : Orchestre l'ensemble du processus
  - Parse les arguments de ligne de commande (sys.argv)
  - Valide le fichier PDF fourni
  - Traite le PDF unique spécifié
  - Génère le CSV dans le même répertoire avec nom descriptif
  - Gestion d'erreurs avec messages explicites

## Format des données

### Format d'entrée (PDF)
Les PDFs doivent suivre le format standard SKIBEC/SQA:
- Générés par Split Second Ver. 8.08 Rev. 4
- Chronométrage TAG HEUER CP 540
- Structure: Rang | Dossard | Nom | AN | Classe | Club | NAT | Temps | Écart

### Format de sortie (CSV)
```
Date;Lieu;Type de compétition;Rang;Dossard;Nom;Année;Club;Temps;Temps (secondes);Écart
```

**11 colonnes** (retirées: Heure de début, Classe, Fichier source)

**Important**:
- Les décimales utilisent la virgule (`,`) et non le point (`.`)
  - Exemple: `36,16` au lieu de `36.16`
  - Temps en minutes: `1:02,92` au lieu de `1:02.92`
- Encodage: UTF-8 avec BOM pour compatibilité Excel
- Les caractères accentués (é, è, à, etc.) sont correctement encodés
- **Nouvelle colonne "Temps (secondes)"**: Conversion automatique des temps
  - `36,12` → `36,12` (déjà en secondes)
  - `1:02,92` → `62,92` (1 min * 60 + 2,92 sec)

## Conventions de codage

### Langue
- Code: Français (noms de variables, fonctions, commentaires)
- Documentation: Français
- Messages utilisateur: Français

### Style Python
- PEP 8 pour le style général
- Docstrings en français pour toutes les fonctions
- Gestion d'erreurs avec try/except et messages explicites

### Regex
Le pattern principal pour extraire les résultats:
- Commence par le début de ligne avec espaces optionnels: `^\s*`
- Capture le rang: `(\d+)`
- Capture le dossard: `(\d+)`
- Capture le nom (non-greedy jusqu'à l'année): `(.+?)`
- Capture l'année: `(20\d{2})`
- Capture la classe: `([A-D])`
- Capture le club: `([A-Z]+)`
- Literal: `U12`
- Capture le temps: `([\d:,\.]+)`
- Capture l'écart (optionnel): `(?:\s+([\d:,\.]+))?`

## Limitations connues

1. **Format PDF**: Le script est optimisé pour les PDFs SKIBEC/SQA. D'autres formats peuvent nécessiter des ajustements.

2. **Extraction de tableaux**: pdfplumber extrait parfois les tableaux comme une seule cellule. Le script utilise donc du parsing de texte avec regex au lieu de l'extraction de tableaux.

3. **Statuts spéciaux**: Les compétiteurs DNS (Did Not Start), DNF (Did Not Finish) et DSQ (Disqualified) ne sont pas inclus dans le CSV car ils n'ont pas de temps enregistré.

## Ajout de nouveaux types de courses

Pour supporter de nouveaux formats de PDF:

1. Ajuster le pattern regex dans `extraire_resultats()` si nécessaire
2. Modifier `extraire_type_competition()` pour capturer de nouveaux formats de noms
3. Ajuster `generer_nom_fichier_csv()` pour les nouveaux formats de noms
4. Tester avec les nouveaux PDFs

## Workflow typique

### Traiter un nouveau PDF

```bash
# 1. Placer le PDF dans le répertoire approprié
cp nouveau_resultat.pdf courses/Sl-Stoneham/

# 2. Exécuter le script
python3 extracteur_resultats.py "courses/Sl-Stoneham/nouveau_resultat.pdf"

# 3. Le CSV est automatiquement créé au même endroit
# courses/Sl-Stoneham/Stoneham_2026-01-XX_SlalomX_X.csv
```

### Traiter tous les PDFs d'un événement

```bash
# Si plusieurs PDFs arrivent en même temps
for pdf in courses/Sl-Stoneham/*.pdf; do
    if [ ! -f "${pdf%.pdf}.csv" ] && [ ! -f "$(dirname "$pdf")/Stoneham_"*".csv" ]; then
        python3 extracteur_resultats.py "$pdf"
    fi
done
```

## Notes importantes

- **Toujours travailler dans le répertoire `résultats`**: Ne jamais naviguer vers le répertoire parent `/dev`
- **Format français**: Respecter l'utilisation de la virgule pour les décimales
- **Encodage UTF-8**: Important pour les caractères accentués (é, è, à, etc.)
- **Structure des dossiers**: Les PDFs doivent être dans `courses/` ou ses sous-répertoires

## Dépendances

- **Python 3.6+** : Langage principal
- **pdfplumber 0.10.0+** : Extraction de texte depuis les PDFs
  - Dépend de: pdfminer.six, Pillow, pypdfium2
