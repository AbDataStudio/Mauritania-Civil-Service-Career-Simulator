import random
N = 10000

def generer_corps():
    corps = ["MEN", "MESRS", "Autres"]
    poids = [10, 10, 80]
    return random.choices(corps, weights=poids, k=1)[0]

def generer_annee_naissance():
    annee = int(random.gauss(1982, 10))
    annee = max(1963, min(2004, annee))
    return annee

def generer_diplome(corps):
    if corps in ["MEN", "MESRS"]:
        return "Bac+2"
    else:
        diplomes = ["Bac+2", "Bac", "Brevet"]
        poids = [75, 14, 12]
        return random.choices(
            diplomes, weights=poids, k=1)[0]

def generer_position():
    positions = [
        "En activite",
        "Detachement",
        "Sous les drapeaux",
        "Disponibilite",
        "Hors cadres"
    ]
    poids = [80, 8, 5, 4, 3]
    return random.choices(
        positions, weights=poids, k=1)[0]

def generer_note():
    return random.randint(0, 20)

def generer_reclassement(diplome):
    if diplome == "Brevet":
        valeurs = ["Non reclasse",
                   "Reclasse C->B"]
        poids = [80, 20]
    elif diplome == "Bac":
        valeurs = ["Non reclasse",
                   "Reclasse B->A"]
        poids = [80, 20]
    else:

        return "Non reclasse"
    return random.choices(
        valeurs, weights=poids, k=1)[0]

def generer_annee_recrutement(annee_naissance):
    min_recrut = annee_naissance + 22
    max_recrut = min(annee_naissance + 40, 2026)
    age_recrut = int(random.gauss(28, 4.3))
    age_recrut = max(22, min(40, age_recrut))
    annee = annee_naissance + age_recrut
    annee = max(min_recrut, min(max_recrut, annee))
    return annee

def generer_duree_dispo(position, annee_recrut):
    if position != "Disponibilite":
        return 0
    temps_brut = 2026 - annee_recrut
    return round(random.uniform(1, temps_brut), 1)

def generer_duree_hc(position, annee_recrut, duree_dispo):
    if position != "Hors cadres":
        return 0
    temps_brut = 2026 - annee_recrut
    max_hc = temps_brut - duree_dispo
    if max_hc <= 0:
        return 0
    return round(random.uniform(1, max_hc), 1)

def generer_categorie(diplome, reclassement):
    if reclassement == "Reclasse C->B":
        return "B"
    elif reclassement == "Reclasse B->A":
        return "A"


    if diplome == "Bac+2":
        return "A"
    elif diplome == "Bac":
        return "B"
    else:
        return "C"

def generer_etat_service(annee_recrut,
                          duree_dispo,
                          duree_hc):
    es = (2026 - annee_recrut) - duree_dispo - duree_hc
    return max(0, es)


def generer_grade(corps, es, note):

    if corps == "MEN":
        return "Grade Unique MEN"

    elif corps == "MESRS":
        return "Grade Unique MESRS"

    else:
        # Autres corps
        if es >= 8 and note >= 12:
            return "Grade 1"
        else:
            return "Grade 2"

def generer_echelon(corps, grade, es, note):

    # MEN :
    if corps == "MEN":
        ech = int(es / 2) + 1
        ech = min(13, ech)
        # Avancement au choix echelon 10
        if ech >= 10 and note >= 12:
            ech = min(13, ech + 1)
        return ech

    # MESRS :
    elif corps == "MESRS":
        ech = int(es / 2) + 1
        ech = min(13, ech)
        # Avancement au choix echelon 6
        if ech >= 6 and note >= 12:
            ech = min(13, ech + 1)
        return ech

    # Autres corps Grade 2 :
    # Echelon basé sur ES total
    elif grade in ["Grade 2",
                   "Grade Unique MEN",
                   "Grade Unique MESRS"]:
        ech = int(es / 2) + 1
        return min(13, ech)

    # Autres corps Grade 1 :
    # Echelon repart à 1 après 8 ans
    else:  # Grade 1
        ech = int((es - 8) / 2) + 1
        return min(13, max(1, ech))

def generer_anciennete(echelon, es):
    anciennete = es - (echelon - 1) * 2
    return max(0, round(anciennete, 1))

def generer_age_retraite(annee_naissance):
    return annee_naissance + 63



# GENERATION 10 000 AGENTS - VERSION SIMPLIFIÉE

agents = []

for i in range(N):
    corps = generer_corps()
    diplome = generer_diplome(corps)
    annee_naiss = generer_annee_naissance()
    position = generer_position()
    note = generer_note()
    annee_recrut = generer_annee_recrutement(annee_naiss)
    duree_dispo = generer_duree_dispo(position, annee_recrut)
    duree_hc = generer_duree_hc(position, annee_recrut, duree_dispo)
    reclassement = generer_reclassement(diplome)
    categorie = generer_categorie(diplome, reclassement)
    es = generer_etat_service(annee_recrut, duree_dispo, duree_hc)
    grade = generer_grade(corps, es, note)
    echelon = generer_echelon(corps, grade, es, note)
    anciennete = generer_anciennete(echelon, es)
    age_retraite = generer_age_retraite(annee_naiss)

    # Agent complet
    agent = {
        'id_agent': i,
        'age_naissance': annee_naiss,
        'age_actuel': 2026 - annee_naiss,
        'corps': corps,
        'diplome': diplome,
        'reclassement': reclassement,
        'categorie': categorie,
        'position': position,
        'duree_dispo': duree_dispo,
        'duree_hc': duree_hc,
        'annee_recrutement': annee_recrut,
        'anciennete_totale': 2026 - annee_recrut,
        'etat_service': es,
        'note': note,
        'grade': grade,
        'echelon': echelon,
        'anciennete_echelon': anciennete,
        'age_retraite': age_retraite,
        'statut': 'Actif'
    }

    agents.append(agent)

# CRÉATION DU DATAFRAME
import pandas as pd

df = pd.DataFrame(agents)

# Mise à jour du statut Retraite
df.loc[df['age_actuel'] >= 63, 'statut'] = 'Retraite'

# AFFICHAGE
from tabulate import tabulate

# Configuration d'affichage
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("\n" + "="*160)
print("                  DATAFRAME COMPLET ")
print("="*160)

# Réorganisation des colonnes (les plus importantes en premier)
cols_ordre = [
    'id_agent', 'age_actuel', 'corps', 'grade', 'echelon',
    'etat_service', 'note', 'age_naissance',
    'annee_recrutement', 'anciennete_totale', 'diplome',
    'categorie', 'position', 'duree_dispo', 'duree_hc',
    'reclassement', 'anciennete_echelon', 'age_retraite', 'statut'
]

df_ordre = df[cols_ordre]

# Affichage du tableau
print(tabulate(df_ordre.sample(500),
               headers='keys',
               tablefmt='pretty',
               showindex=False))

print("\n" + "="*160)
print(f"Total Agents : {df.shape[0]:,} | Total Colonnes : {df.shape[1]}")
print("="*160)


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from collections import Counter
import numpy as np

# ====================== PALETTE - FOND BLANC 100% ======================
plt.style.use('seaborn-v0_8-whitegrid')

BG = '#ffffff'      # ← Fond blanc pur
CARD = '#ffffff'    # Cartes aussi blanches
TEXT = '#1a2e1f'
MUTED = '#556655'
BORDER = '#e0e0e0'  # Bordures légèrement plus visibles sur fond blanc

COLORS = ['#006400', '#C8102E', '#228B22', '#8B0000', '#DAA520',
          '#2E8B57', '#B22222', '#32CD32', '#FFD700']

N = len(df)

# Extraction des listes
liste_corps = df['corps'].tolist()
liste_annee = df['age_naissance'].tolist()
liste_diplome = df['diplome'].tolist()
liste_position = df['position'].tolist()
liste_note = df['note'].tolist()
liste_grade = df['grade'].tolist()
liste_echelon = df['echelon'].tolist()
liste_es = df['etat_service'].tolist()
liste_anciennete = df['anciennete_echelon'].tolist()

