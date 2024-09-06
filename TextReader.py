import csv
from datetime import datetime

# Fonction pour lire le dictionnaire à partir d'un fichier texte "database.txt"
def lire_dictionnaire_depuis_fichier(nom_fichier):
    dictionnaire = {}
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            parts = ligne.strip().split(',')
            if len(parts) >= 3:  # Assure que chaque ligne a au moins trois valeurs
                mot = parts[0].strip().lower()
                valeur_1 = parts[1].strip() if len(parts) > 1 else "unbekannt"
                valeur_2 = parts[2].strip() if len(parts) > 2 else "unbekannt"
                dictionnaire[mot] = (valeur_1, valeur_2)
    return dictionnaire

# Fonction pour lire la liste des mots à ignorer (stopwords) à partir d'un fichier texte
def lire_stopwords(nom_fichier):
    stopwords = set()
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            stopwords.add(ligne.strip().lower())
    return stopwords

# Fonction pour extraire les mots du texte et les comparer avec le dictionnaire
def extraire_mots_et_comparer(texte, dictionnaire, stopwords):
    mots = texte.split()
    resultat = []
    mots_vus = set()

    for mot in mots:
        mot_nettoye = ''.join(char for char in mot if char.isalpha())  # Enlever la ponctuation
        mot_lower = mot_nettoye.lower()
        if mot_lower and mot_lower not in mots_vus and mot_lower not in stopwords:
            mots_vus.add(mot_lower)
            if mot_lower in dictionnaire:
                valeur_1, valeur_2 = dictionnaire[mot_lower]
                resultat.append((mot_lower, valeur_1, valeur_2))
            else:
                resultat.append((mot_lower, "unbekannt", "unbekannt"))
    return resultat

# Lire le texte à partir d'un fichier en UTF-8
def lire_texte_fichier(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        return fichier.read()

# Obtenir la date et l'heure actuelles pour nommer le fichier CSV
date_heure_actuelle = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nom_fichier_csv = f"mots_comparaison_{date_heure_actuelle}.csv"

# Lire le dictionnaire depuis le fichier externe "database.txt"
nom_fichier_dictionnaire = "database.txt"
dictionnaire_externe = lire_dictionnaire_depuis_fichier(nom_fichier_dictionnaire)

# Lire la liste des mots à ignorer depuis le fichier "german_stopwords.txt"
nom_fichier_stopwords = "german_stopwords.txt"
stopwords = lire_stopwords(nom_fichier_stopwords)

# Lire le texte du fichier
nom_fichier_texte = "votre_texte.txt"
texte = lire_texte_fichier(nom_fichier_texte)

# Extraire les mots et leur statut
mots_avec_statut = extraire_mots_et_comparer(texte, dictionnaire_externe, stopwords)

# Exporter les résultats dans un fichier CSV avec des points-virgules
with open(nom_fichier_csv, mode='w', newline='', encoding='utf_8_sig') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
    writer.writerow(["Mot", "Valeur 1", "Valeur 2"])
    for mot, valeur_1, valeur_2 in mots_avec_statut:
        writer.writerow([mot, valeur_1, valeur_2])

print(f"Les mots et leur statut ont été exportés dans '{nom_fichier_csv}'.")