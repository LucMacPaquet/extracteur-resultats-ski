# Répertoire des PDFs de résultats

Placez vos fichiers PDF de résultats de courses dans ce répertoire.

## Structure recommandée

Organisez les PDFs par lieu ou par événement:

```
courses/
├── Sl-Stoneham/
│   ├── 298137 Race Results.pdf
│   ├── 298139 Race Results.pdf
│   ├── Stoneham_2026-01-18_Slalom1_F.csv  (généré)
│   └── Stoneham_2026-01-18_Slalom2_F.csv  (généré)
├── Mont-Sainte-Anne/
│   └── ...
└── Autre-Lieu/
    └── ...
```

## Utilisation

Pour traiter un PDF et générer son CSV:

```bash
python3 extracteur_resultats.py "courses/Sl-Stoneham/298137 Race Results.pdf"
```

Le fichier CSV sera automatiquement créé dans le même répertoire que le PDF source.

## Notes

- Les fichiers CSV générés ne sont **pas** versionnés dans Git (voir `.gitignore`)
- Seuls les PDFs sources sont importants à conserver
- Les CSV peuvent être régénérés à tout moment à partir des PDFs
