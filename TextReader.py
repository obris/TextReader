import csv
import sys
from datetime import datetime

def lire_dictionnaire_depuis_fichier(nom_fichier):
    dictionnaire = {}
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            parts = ligne.strip().split(',')
            if len(parts) >= 3:
                mot = parts[0].strip().lower()
                valeur_1 = parts[1].strip() if len(parts) > 1 else "unbekannt"
                valeur_2 = parts[2].strip() if len(parts) > 2 else "unbekannt"
                dictionnaire[mot] = (valeur_1, valeur_2)
    return dictionnaire

def lire_stopwords(nom_fichier):
    stopwords = set()
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            stopwords.add(ligne.strip().lower())
    return stopwords

def extraire_mots_et_comparer(texte, dictionnaire, stopwords):
    mots = texte.split()
    resultat = []
    mots_vus = set()

    for mot in mots:
        mot_nettoye = ''.join(char for char in mot if char.isalpha())  # Supprimer la ponctuation
        mot_lower = mot_nettoye.lower()
        if mot_lower and mot_lower not in mots_vus and mot_lower not in stopwords:
            mots_vus.add(mot_lower)
            if mot_lower in dictionnaire:
                valeur_1, valeur_2 = dictionnaire[mot_lower]
                resultat.append((mot_lower, valeur_1, valeur_2))
            else:
                resultat.append((mot_lower, "unbekannt", "unbekannt"))
    return resultat

def lire_texte_fichier(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        return fichier.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <votre_texte.txt>")
        sys.exit(1)

    nom_fichier_texte = sys.argv[1]
    nom_fichier_dictionnaire = "database.txt"
    nom_fichier_stopwords = "german_stopwords.txt"

    date_heure_actuelle = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier_csv = f"mots_comparaison_{date_heure_actuelle}.csv"

    dictionnaire_externe = lire_dictionnaire_depuis_fichier(nom_fichier_dictionnaire)
    stopwords = lire_stopwords(nom_fichier_stopwords)
    texte = lire_texte_fichier(nom_fichier_texte)

    mots_avec_statut = extraire_mots_et_comparer(texte, dictionnaire_externe, stopwords)

    with open(nom_fichier_csv, mode='w', newline='', encoding='utf_8_sig') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';', quoting=csv.QUOTE_NONE, escapechar=' ')
        writer.writerow(["Mot", "Valeur 1", "Valeur 2"])
        for mot, valeur_1, valeur_2 in mots_avec_statut:
            writer.writerow([mot, valeur_1, valeur_2])

    print(f"Les mots et leur statut ont été exportés dans '{nom_fichier_csv}'.")

if __name__ == "__main__":
    main()
