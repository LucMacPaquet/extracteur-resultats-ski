#!/bin/bash
# Script helper pour traiter tous les PDFs dans le répertoire courses/

echo "================================================================"
echo "TRAITEMENT PAR LOTS - Extracteur de résultats"
echo "================================================================"
echo ""

# Compter le nombre de PDFs
nb_pdfs=$(find courses -name "*.pdf" | wc -l | tr -d ' ')

if [ "$nb_pdfs" -eq 0 ]; then
    echo "Aucun fichier PDF trouvé dans le répertoire courses/"
    exit 0
fi

echo "Nombre de fichiers PDF trouvés: $nb_pdfs"
echo ""

# Compteurs
compteur=0
succes=0
echecs=0

# Traiter chaque PDF
while IFS= read -r pdf; do
    compteur=$((compteur + 1))
    echo "[$compteur/$nb_pdfs] Traitement de: $pdf"
    echo ""

    if python3 extracteur_resultats.py "$pdf"; then
        succes=$((succes + 1))
        echo ""
    else
        echecs=$((echecs + 1))
        echo "❌ Échec du traitement"
        echo ""
    fi

    echo "---"
    echo ""
done < <(find courses -name "*.pdf")

# Résumé
echo "================================================================"
echo "RÉSUMÉ"
echo "================================================================"
echo "Total de PDFs traités: $nb_pdfs"
echo "Succès: $succes"
echo "Échecs: $echecs"
echo ""
echo "Les fichiers CSV ont été générés dans les mêmes répertoires"
echo "que les fichiers PDF sources."
