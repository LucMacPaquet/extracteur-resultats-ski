# Guide pour débutants - Extracteur de résultats de ski

Ce guide est conçu pour les personnes qui ne sont pas familières avec GitHub, la programmation ou les outils informatiques. Suivez ces étapes **une par une** et vous pourrez utiliser ce script facilement!

## 📚 Table des matières

1. [Qu'est-ce que c'est?](#quest-ce-que-cest)
2. [Ce dont vous avez besoin](#ce-dont-vous-avez-besoin)
3. [Étape 1: Installer Python](#étape-1-installer-python)
4. [Étape 2: Télécharger le projet](#étape-2-télécharger-le-projet)
5. [Étape 3: Installer les dépendances](#étape-3-installer-les-dépendances)
6. [Étape 4: Utiliser le script](#étape-4-utiliser-le-script)
7. [Résolution de problèmes](#résolution-de-problèmes)
8. [Glossaire](#glossaire)

---

## Qu'est-ce que c'est?

Ce projet est un **script** (un petit programme) qui lit des fichiers PDF contenant des résultats de courses de ski et crée automatiquement un fichier Excel (CSV) avec toutes les données organisées.

**Avant:**
- Vous avez un PDF avec 50 résultats de course
- Vous devez copier-coller chaque ligne manuellement dans Excel
- ⏱️ Temps: 30-60 minutes de travail fastidieux

**Après:**
- Vous lancez le script avec une commande
- Le fichier Excel est créé automatiquement
- ⏱️ Temps: 10 secondes!

---

## Ce dont vous avez besoin

✅ Un ordinateur (Mac, Windows ou Linux)
✅ Une connexion Internet (pour télécharger Python et le projet)
✅ Environ 15 minutes pour l'installation (à faire une seule fois)
✅ Vos fichiers PDF de résultats de courses

❌ **PAS besoin** de connaître la programmation
❌ **PAS besoin** d'être un expert en informatique

---

## Étape 1: Installer Python

Python est le **langage de programmation** utilisé par ce script. C'est gratuit et facile à installer.

### Sur Windows

1. **Aller sur le site officiel:** Ouvrez votre navigateur et allez sur https://www.python.org/downloads/
2. **Télécharger:** Cliquez sur le gros bouton jaune "Download Python 3.x.x"
3. **Installer:**
   - Double-cliquez sur le fichier téléchargé
   - ⚠️ **IMPORTANT:** Cochez la case "Add Python to PATH" en bas de la fenêtre
   - Cliquez sur "Install Now"
   - Attendez que l'installation se termine (2-3 minutes)
4. **Vérifier:** Ouvrez le "Command Prompt" (cherchez "cmd" dans le menu Démarrer) et tapez:
   ```
   python --version
   ```
   Vous devriez voir quelque chose comme "Python 3.12.1"

### Sur Mac

1. **Ouvrir le Terminal:**
   - Appuyez sur `Cmd + Espace`
   - Tapez "Terminal"
   - Appuyez sur Entrée
2. **Installer Homebrew** (un gestionnaire de logiciels pour Mac):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   Attendez que l'installation se termine (5-10 minutes)
3. **Installer Python:**
   ```bash
   brew install python
   ```
4. **Vérifier:**
   ```bash
   python3 --version
   ```
   Vous devriez voir "Python 3.x.x"

### Sur Linux

Python est probablement déjà installé! Pour vérifier, ouvrez un terminal et tapez:
```bash
python3 --version
```

Si Python n'est pas installé:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## Étape 2: Télécharger le projet

Il y a deux façons de télécharger le projet. Choisissez la méthode qui vous convient.

### Méthode A: Téléchargement direct (le plus simple)

1. **Aller sur GitHub:** Ouvrez votre navigateur et allez sur:
   ```
   https://github.com/LucMacPaquet/extracteur-resultats-ski
   ```

2. **Télécharger:**
   - Cliquez sur le bouton vert "Code"
   - Cliquez sur "Download ZIP"
   - Le fichier ZIP sera téléchargé dans votre dossier "Téléchargements"

3. **Décompresser:**
   - Allez dans votre dossier "Téléchargements"
   - Double-cliquez sur le fichier "extracteur-resultats-ski-main.zip"
   - Un nouveau dossier sera créé
   - **Déplacez ce dossier** où vous voulez (par exemple: Documents)

### Méthode B: Avec Git (pour les plus aventureux)

Si vous voulez pouvoir facilement mettre à jour le projet plus tard:

1. **Installer Git:**
   - Windows: https://git-scm.com/download/win
   - Mac: `brew install git`
   - Linux: `sudo apt install git`

2. **Cloner le projet:**
   Ouvrez votre terminal/invite de commandes, allez dans le dossier où vous voulez le projet:
   ```bash
   cd Documents
   git clone https://github.com/LucMacPaquet/extracteur-resultats-ski.git
   ```

---

## Étape 3: Installer les dépendances

Le script a besoin d'une bibliothèque appelée "pdfplumber" pour lire les PDF.

### Sur tous les systèmes

1. **Ouvrir le terminal/invite de commandes**

2. **Aller dans le dossier du projet:**

   **Windows:**
   ```
   cd C:\Users\VotreNom\Documents\extracteur-resultats-ski-main
   ```

   **Mac/Linux:**
   ```bash
   cd ~/Documents/extracteur-resultats-ski
   ```

   💡 **Astuce:** Sur Mac et Windows, vous pouvez glisser-déposer le dossier dans le terminal pour obtenir le chemin complet!

3. **Installer les dépendances:**

   **Windows:**
   ```
   pip install -r requirements.txt
   ```

   **Mac/Linux:**
   ```bash
   pip3 install -r requirements.txt
   ```

   Attendez quelques secondes, vous verrez des messages défiler.

4. **Vérifier:**
   Vous devriez voir "Successfully installed pdfplumber..." à la fin.

---

## Étape 4: Utiliser le script

Maintenant que tout est installé, voici comment utiliser le script!

### Préparer vos fichiers

1. **Copier votre PDF** dans le dossier du projet:
   - Ouvrez le dossier `extracteur-resultats-ski`
   - Ouvrez le sous-dossier `courses`
   - Créez un dossier pour votre événement (par exemple: `Sl-Stoneham`)
   - Mettez votre PDF dedans

   Structure finale:
   ```
   extracteur-resultats-ski/
   ├── courses/
   │   └── Sl-Stoneham/
   │       └── 298137 Race Results.pdf  ← Votre PDF ici
   └── extracteur_resultats.py
   ```

### Lancer le script

Le script peut fonctionner de deux façons:

#### Option A: Traiter un seul fichier PDF

1. **Ouvrir le terminal** dans le dossier du projet (comme à l'étape 3)

2. **Lancer la commande:**

   **Windows:**
   ```
   python extracteur_resultats.py "courses\Sl-Stoneham\298137 Race Results.pdf"
   ```

   **Mac/Linux:**
   ```bash
   python3 extracteur_resultats.py "courses/Sl-Stoneham/298137 Race Results.pdf"
   ```

3. **Attendre 10 secondes** ⏳

4. **C'est fait!** 🎉
   - Le fichier CSV est créé dans le même dossier que le PDF
   - Son nom sera quelque chose comme: `Stoneham_2026-01-18_Slalom1_F.csv`

#### Option B: Traiter tous les PDFs d'un dossier (RECOMMANDÉ!)

C'est la méthode la plus simple si vous avez plusieurs PDFs à traiter!

1. **Ouvrir le terminal** dans le dossier du projet (comme à l'étape 3)

2. **Lancer la commande avec le nom du dossier:**

   **Windows:**
   ```
   python extracteur_resultats.py "courses\Sl-Stoneham"
   ```

   **Mac/Linux:**
   ```bash
   python3 extracteur_resultats.py courses/Sl-Stoneham
   ```

3. **Regarder la magie opérer!** ✨
   - Le script trouve automatiquement tous les PDFs dans le dossier
   - Il les traite un par un
   - Il affiche sa progression: `[1/4] Traitement...`, `[2/4] Traitement...`
   - À la fin, il affiche un résumé complet

4. **Résultat:** 🎉
   ```
   ✅ Fichiers traités avec succès: 4/4

   Fichiers CSV générés:
     ✓ 298137 Race Results.pdf
     ✓ 298138 Race Results.pdf
     ✓ 298139 Race Results.pdf
     ✓ 298140 Race Results.pdf
   ```

**Avantage de l'option B:**
- Pas besoin de lancer la commande 10 fois pour 10 PDFs!
- Un seul clic et tout est traité
- Gain de temps énorme si vous avez beaucoup de courses

### Ouvrir le fichier CSV

**Dans Excel:**
1. Ouvrez Excel
2. Menu "Fichier" → "Ouvrir"
3. Sélectionnez votre fichier CSV
4. Les données s'affichent correctement avec les colonnes séparées

**Dans Google Sheets:**
1. Allez sur https://sheets.google.com
2. "Fichier" → "Importer"
3. Sélectionnez votre fichier CSV
4. Choisissez "Point-virgule" comme séparateur

---

## Résolution de problèmes

### "Python n'est pas reconnu..."

**Problème:** Windows ne trouve pas Python.

**Solution:**
1. Réinstallez Python en cochant bien "Add Python to PATH"
2. Ou redémarrez votre ordinateur après l'installation

### "pip n'est pas reconnu..."

**Problème:** La commande `pip` ne fonctionne pas.

**Solution:**
- Sur Windows: Essayez `py -m pip install -r requirements.txt`
- Sur Mac/Linux: Essayez `python3 -m pip install -r requirements.txt`

### "Aucun fichier trouvé"

**Problème:** Le script ne trouve pas votre PDF.

**Solution:**
1. Vérifiez le chemin du fichier (avec les bons slashes `/` ou `\`)
2. Vérifiez que le nom du fichier est exact (avec les espaces)
3. Utilisez les guillemets `"` autour du chemin

### "Permission denied"

**Problème:** Le script n'a pas la permission d'écrire le fichier.

**Solution:**
1. Fermez Excel si le fichier CSV est déjà ouvert
2. Vérifiez que vous avez les droits d'écriture dans le dossier

### Les accents ne s'affichent pas correctement

**Problème:** Les é, è, à apparaissent bizarrement.

**Solution:**
- Dans Excel: "Données" → "Importer" → Choisir "UTF-8" comme encodage
- Dans Google Sheets: Le fichier devrait s'ouvrir correctement automatiquement

### Besoin d'aide?

Si vous rencontrez un problème non listé ici:
1. Lisez attentivement le message d'erreur
2. Vérifiez que vous avez suivi toutes les étapes dans l'ordre
3. Ouvrez une "Issue" sur GitHub (bouton "Issues" en haut de la page) avec:
   - Votre système d'exploitation (Windows, Mac, Linux)
   - Le message d'erreur complet
   - Ce que vous essayiez de faire

---

## Glossaire

Voici les termes techniques expliqués simplement:

**CSV** (Comma-Separated Values)
- Un format de fichier pour les tableaux
- Peut être ouvert avec Excel, Google Sheets, etc.
- Les colonnes sont séparées par des points-virgules (;)

**Python**
- Un langage de programmation
- Gratuit et très populaire
- Utilisé par des millions de personnes dans le monde

**Script**
- Un petit programme qui automatise une tâche
- Comme une recette de cuisine pour l'ordinateur

**Terminal / Invite de commandes**
- Une fenêtre où on tape des commandes textuelles
- Ancien mode d'utilisation des ordinateurs (mais toujours très utile!)
- Sur Windows: "Command Prompt" ou "PowerShell"
- Sur Mac: "Terminal"

**GitHub**
- Un site web pour partager du code
- Comme un "Google Drive" pour les programmeurs
- Gratuit et utilisé par des millions de développeurs

**Dépendance / Bibliothèque**
- Du code créé par d'autres personnes qu'on réutilise
- Évite de "réinventer la roue"
- Exemple: `pdfplumber` sait lire les PDF, on l'utilise dans notre script

**Repository / Repo**
- Un dossier de projet sur GitHub
- Contient tout le code et les fichiers du projet

**PDF** (Portable Document Format)
- Format de fichier pour les documents
- Garde le même aspect sur tous les ordinateurs
- Difficile à extraire automatiquement (d'où l'utilité de ce script!)

**UTF-8**
- Un système d'encodage de caractères
- Permet d'afficher correctement les accents (é, è, à, etc.)
- Standard international

---

## 🎓 Vous avez terminé!

Félicitations! Vous savez maintenant:
- ✅ Installer Python
- ✅ Télécharger un projet depuis GitHub
- ✅ Installer des dépendances
- ✅ Lancer un script Python
- ✅ Ouvrir et utiliser les fichiers CSV générés

**Conseil:** Gardez ce guide sous la main pour la prochaine fois que vous utiliserez le script!

**Pour aller plus loin:**
- Explorez les autres fichiers du projet
- Lisez le [README.md](README.md) principal pour plus de détails techniques
- Consultez [CLAUDE.md](CLAUDE.md) si vous voulez comprendre comment fonctionne le code

---

## 📞 Support

Des questions? Des suggestions pour améliorer ce guide?
- Ouvrez une "Issue" sur GitHub: https://github.com/LucMacPaquet/extracteur-resultats-ski/issues
- Proposez des améliorations au guide!

**Bon courage avec vos résultats de courses de ski!** 🎿
