#!/usr/bin/env python3
"""
Script d'extraction des résultats de courses de ski depuis des PDFs
Génère un fichier CSV avec les informations pertinentes
Format décimal: virgule (,) au lieu de point (.)

Usage: python3 extracteur_resultats.py <fichier_pdf>
"""

import pdfplumber
import csv
import re
import sys
from pathlib import Path
from datetime import datetime


def extraire_date(texte):
    """Extrait la date du PDF"""
    match = re.search(r'(Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)\s+(\d{1,2}/\d{1,2}/\d{4})', texte)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return ""


def extraire_lieu(texte):
    """Extrait le lieu de la course"""
    # Cherche STONEHAM ou autres lieux
    if 'STONEHAM' in texte:
        return 'STONEHAM'
    return ""


def extraire_type_competition(texte):
    """Extrait le type de compétition"""
    match1 = re.search(r'GRANDS CIRCUITS SLALOM \d+', texte)
    match2 = re.search(r'SLALOM [A-ZÉÈÊ]+', texte)

    if match1 and match2:
        return f"{match1.group(0)} - {match2.group(0)}"
    return ""


def extraire_heure_debut(texte):
    """Extrait l'heure de début"""
    match = re.search(r'Heure de début[:\s]+(\d{1,2}:\d{2})', texte)
    if match:
        return match.group(1)
    return ""


def convertir_temps_en_secondes(temps_str):
    """Convertit un temps au format MM:SS,cc ou SS,cc en secondes totales

    Exemples:
        "36,12" -> 36.12
        "1:02,3" -> 62.3
        "1:23,45" -> 83.45

    Args:
        temps_str: Chaîne représentant un temps (avec virgules pour décimales)

    Returns:
        float: Temps en secondes, ou None si conversion impossible
    """
    if not temps_str or temps_str == '':
        return None

    try:
        # Remplacer virgule par point pour la conversion en float
        temps_normalise = temps_str.replace(',', '.')

        if ':' in temps_normalise:
            # Format MM:SS.cc
            parties = temps_normalise.split(':')
            minutes = int(parties[0])
            secondes = float(parties[1])
            return minutes * 60 + secondes
        else:
            # Format SS.cc - déjà en secondes
            return float(temps_normalise)
    except Exception as e:
        return None


def calculer_note(temps_secondes, ecart_secondes):
    """Calcule la note en pourcentage basée sur l'écart par rapport au temps

    La formule est: (1 - écart/temps) * 100

    Exemples:
        temps=40.07, écart=2.49 -> 93.79%
        temps=37.58, écart=0.00 -> 100.00%
        temps=62.92, écart=25.34 -> 59.71%

    Args:
        temps_secondes: Temps du participant en secondes
        ecart_secondes: Écart avec le premier en secondes

    Returns:
        float: Note en pourcentage, ou None si calcul impossible
    """
    if temps_secondes is None or ecart_secondes is None:
        return None

    if temps_secondes <= 0:
        return None

    try:
        note = (1 - (ecart_secondes / temps_secondes)) * 100
        return note
    except Exception as e:
        return None


def extraire_resultats(texte):
    """Extrait les résultats des compétiteurs depuis le texte"""
    resultats = []

    # Pattern pour les lignes de résultats
    # Format: Rang Dos Nom AN Classe Club NAT Heure Écart
    # Le pattern capture: rang, dossard, nom (tout jusqu'à l'année), année, classe, club, temps, écart (optionnel)
    pattern = r'^\s*(\d+)\s+(\d+)\s+(.+?)\s+(20\d{2})\s+([A-D])\s+([A-Z]+)\s+U12\s+([\d:,\.]+)(?:\s+([\d:,\.]+))?\s*$'

    for ligne in texte.split('\n'):
        match = re.match(pattern, ligne)
        if match:
            rang = match.group(1)
            dossard = match.group(2)
            nom = match.group(3).strip()
            annee = match.group(4)
            classe = match.group(5)
            club = match.group(6)
            temps = match.group(7)
            ecart = match.group(8) if match.group(8) else "0.00"

            # Convertir les points en virgules
            temps = temps.replace('.', ',')
            ecart = ecart.replace('.', ',')

            resultats.append({
                'rang': rang,
                'dossard': dossard,
                'nom': nom,
                'annee': annee,
                'classe': classe,
                'club': club,
                'temps': temps,
                'ecart': ecart
            })

    return resultats


def traiter_pdf(chemin_pdf):
    """Traite un fichier PDF et extrait toutes les informations"""
    print(f"Traitement de {chemin_pdf}...")

    try:
        with pdfplumber.open(chemin_pdf) as pdf:
            # Extraire le texte de toutes les pages
            texte_complet = ""
            for page in pdf.pages:
                texte_complet += page.extract_text() + "\n"

            # Extraire les informations
            date = extraire_date(texte_complet)
            lieu = extraire_lieu(texte_complet)
            type_competition = extraire_type_competition(texte_complet)
            heure_debut = extraire_heure_debut(texte_complet)
            resultats = extraire_resultats(texte_complet)

            return {
                'fichier': chemin_pdf.name,
                'date': date,
                'lieu': lieu,
                'type_competition': type_competition,
                'heure_debut': heure_debut,
                'resultats': resultats
            }
    except Exception as e:
        print(f"Erreur lors du traitement de {chemin_pdf}: {e}")
        import traceback
        traceback.print_exc()
        return None


def nettoyer_nom_fichier(texte):
    """Nettoie une chaîne pour en faire un nom de fichier valide"""
    # Remplacer les caractères invalides
    texte = texte.replace('/', '-')
    texte = texte.replace(':', '-')
    texte = texte.replace(' ', '_')
    texte = re.sub(r'[<>:"|?*]', '', texte)
    return texte


def generer_nom_fichier_csv(donnees_course):
    """Génère un nom de fichier CSV basé sur lieu, date et épreuve"""
    lieu = donnees_course.get('lieu', 'Course').replace('STONEHAM', 'Stoneham')

    # Extraire juste la date sans le jour de la semaine
    date_brute = donnees_course.get('date', '')
    # Format: "Dimanche 1/18/2026" -> "2026-01-18"
    match_date = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_brute)
    if match_date:
        mois, jour, annee = match_date.groups()
        date_formatee = f"{annee}-{mois.zfill(2)}-{jour.zfill(2)}"
    else:
        date_formatee = "date_inconnue"

    # Extraire le numéro de slalom et le type
    type_comp = donnees_course.get('type_competition', '')
    match_slalom = re.search(r'SLALOM\s+(\d+)', type_comp)
    match_type = re.search(r'SLALOM\s+(FÉMININ|MASCULIN|F[EÉ]MININ|M[AÂ]LE)', type_comp)

    numero_slalom = f"Slalom{match_slalom.group(1)}" if match_slalom else "Slalom"
    type_slalom = match_type.group(1).replace('FÉMININ', 'F').replace('MASCULIN', 'M') if match_type else ""

    # Construire le nom: Lieu_Date_Slalom1_F.csv
    nom = f"{lieu}_{date_formatee}_{numero_slalom}"
    if type_slalom:
        nom += f"_{type_slalom}"

    nom = nettoyer_nom_fichier(nom)
    return f"{nom}.csv"


def generer_csv(donnees_course, fichier_sortie):
    """Génère un fichier CSV avec les résultats d'une course"""
    print(f"\nGénération du fichier CSV: {fichier_sortie}")

    # Utiliser UTF-8 avec BOM pour meilleure compatibilité Excel
    with open(fichier_sortie, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        # En-tête (avec colonnes "Temps (secondes)" et "Note")
        writer.writerow([
            'Date', 'Lieu', 'Type de compétition',
            'Rang', 'Dossard', 'Nom', 'Année', 'Club',
            'Temps', 'Temps (secondes)', 'Écart', 'Note'
        ])

        # Données
        if donnees_course and donnees_course['resultats']:
            for resultat in donnees_course['resultats']:
                # Convertir le temps et l'écart en secondes
                temps_secondes = convertir_temps_en_secondes(resultat['temps'])
                ecart_secondes = convertir_temps_en_secondes(resultat['ecart'])

                # Formater temps avec virgule pour le CSV
                if temps_secondes is not None:
                    temps_secondes_str = f"{temps_secondes:.2f}".replace('.', ',')
                else:
                    temps_secondes_str = ""

                # Calculer la note
                note = calculer_note(temps_secondes, ecart_secondes)

                # Formater note avec virgule et symbole %
                if note is not None:
                    note_str = f"{note:.2f}".replace('.', ',') + "%"
                else:
                    note_str = ""

                writer.writerow([
                    donnees_course['date'],
                    donnees_course['lieu'],
                    donnees_course['type_competition'],
                    resultat['rang'],
                    resultat['dossard'],
                    resultat['nom'],
                    resultat['annee'],
                    resultat['club'],
                    resultat['temps'],
                    temps_secondes_str,
                    resultat['ecart'],
                    note_str
                ])

    print(f"✓ Fichier CSV généré avec succès: {fichier_sortie}")


def lister_pdfs_dossier(chemin_dossier):
    """Liste tous les fichiers PDF dans un dossier (récursivement)

    Args:
        chemin_dossier: Path vers le dossier à scanner

    Returns:
        Liste de Path vers les fichiers PDF trouvés
    """
    pdfs = []

    # Recherche récursive de tous les PDFs
    for pdf in chemin_dossier.rglob('*.pdf'):
        if pdf.is_file():
            pdfs.append(pdf)

    # Trier par nom pour un traitement cohérent
    pdfs.sort()

    return pdfs


def traiter_fichier_unique(chemin_pdf):
    """Traite un seul fichier PDF

    Args:
        chemin_pdf: Path vers le fichier PDF

    Returns:
        True si succès, False sinon
    """
    print(f"\nTraitement de {chemin_pdf}...")

    # Traiter le PDF
    donnees = traiter_pdf(chemin_pdf)

    if not donnees:
        print(f"  ❌ Impossible d'extraire les données")
        return False

    if not donnees['resultats']:
        print(f"  ⚠️  Aucun résultat extrait")
        return False

    print(f"  ✓ {len(donnees['resultats'])} résultats extraits")

    # Générer le nom du fichier CSV
    nom_csv = generer_nom_fichier_csv(donnees)

    # Placer le CSV dans le même répertoire que le PDF source
    repertoire_source = chemin_pdf.parent
    chemin_csv = repertoire_source / nom_csv

    # Générer le CSV
    generer_csv(donnees, chemin_csv)

    return True


def main():
    """Fonction principale"""
    print("=" * 70)
    print("EXTRACTEUR DE RÉSULTATS DE COURSES DE SKI")
    print("=" * 70)

    # Vérifier les arguments de ligne de commande
    if len(sys.argv) < 2:
        print("\nUsage: python3 extracteur_resultats.py <fichier_pdf_ou_dossier>")
        print("\nExemples:")
        print("  # Traiter un seul fichier PDF:")
        print("  python3 extracteur_resultats.py \"courses/Sl-Stoneham/298137 Race Results.pdf\"")
        print("\n  # Traiter tous les PDFs d'un dossier:")
        print("  python3 extracteur_resultats.py courses/Sl-Stoneham")
        print("  python3 extracteur_resultats.py courses")
        sys.exit(1)

    # Récupérer le chemin (fichier ou dossier)
    chemin = Path(sys.argv[1])

    # Vérifier que le chemin existe
    if not chemin.exists():
        print(f"\n❌ Erreur: Le chemin '{chemin}' n'existe pas.")
        sys.exit(1)

    # Cas 1: C'est un fichier PDF unique
    if chemin.is_file():
        # Vérifier que c'est bien un fichier PDF
        if chemin.suffix.lower() != '.pdf':
            print(f"\n❌ Erreur: Le fichier doit être un PDF (.pdf)")
            sys.exit(1)

        print(f"\nMode: Fichier unique")
        print(f"Fichier: {chemin}\n")

        succes = traiter_fichier_unique(chemin)

        if succes:
            print(f"\n✅ Traitement terminé!")
            print(f"📁 Répertoire: {chemin.parent}")
        else:
            print(f"\n❌ Échec du traitement")
            sys.exit(1)

    # Cas 2: C'est un dossier
    elif chemin.is_dir():
        print(f"\nMode: Dossier")
        print(f"Dossier: {chemin}")

        # Lister tous les PDFs
        pdfs = lister_pdfs_dossier(chemin)

        if not pdfs:
            print(f"\n⚠️  Aucun fichier PDF trouvé dans {chemin}")
            sys.exit(1)

        print(f"\n📄 {len(pdfs)} fichier(s) PDF trouvé(s):")
        for pdf in pdfs:
            print(f"  - {pdf.relative_to(chemin.parent)}")

        print(f"\n{'=' * 70}")
        print("DÉBUT DU TRAITEMENT")
        print('=' * 70)

        # Traiter chaque PDF
        resultats = {
            'succes': 0,
            'echecs': 0,
            'fichiers_succes': [],
            'fichiers_echecs': []
        }

        for i, pdf in enumerate(pdfs, 1):
            print(f"\n[{i}/{len(pdfs)}] {pdf.name}")

            if traiter_fichier_unique(pdf):
                resultats['succes'] += 1
                resultats['fichiers_succes'].append(pdf.name)
            else:
                resultats['echecs'] += 1
                resultats['fichiers_echecs'].append(pdf.name)

        # Afficher le résumé
        print(f"\n{'=' * 70}")
        print("RÉSUMÉ DU TRAITEMENT")
        print('=' * 70)
        print(f"\n✅ Fichiers traités avec succès: {resultats['succes']}/{len(pdfs)}")

        if resultats['fichiers_succes']:
            print("\nFichiers CSV générés:")
            for fichier in resultats['fichiers_succes']:
                print(f"  ✓ {fichier}")

        if resultats['echecs'] > 0:
            print(f"\n❌ Fichiers en échec: {resultats['echecs']}/{len(pdfs)}")
            if resultats['fichiers_echecs']:
                print("\nFichiers non traités:")
                for fichier in resultats['fichiers_echecs']:
                    print(f"  ✗ {fichier}")

        print(f"\n📁 Dossier de sortie: {chemin}")

        if resultats['echecs'] > 0:
            sys.exit(1)

    else:
        print(f"\n❌ Erreur: '{chemin}' n'est ni un fichier ni un dossier valide.")
        sys.exit(1)


if __name__ == '__main__':
    main()
