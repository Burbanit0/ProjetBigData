# Importation des librairies
import pandas as pd
import numpy as np
from joblib import dump, load

## Nettayage des donnees

# Importation des données 
df = pd.read_csv("xdata.csv")

# Suppression colonne Identifiant et Url
if ('Unnamed: 0' in df.columns):
    df.drop(columns=['Unnamed: 0'],inplace = True)
df.drop(columns=["Identifiant", "Url"],inplace = True)

# Supprimer colonne conditions_annulation
df.drop(columns=["conditions_annulation"],inplace = True)

# 0 si pas d'animaux 1 sinon
df.loc[df.Animal_sur_place.isnull(),'Animal_sur_place']=0
df.loc[df.Animal_sur_place!=0,'Animal_sur_place']=1

# 1 si vrai lit 0 sinon
df.loc[df.type_lit.isnull(),'type_lit']=1
df.loc[df.type_lit=="Vrai lit",'type_lit']=1
df.loc[df.type_lit!=1,'type_lit']=0

#Supprimer colonne reglement_interieur
df.drop(columns=["reglement_interieur"],inplace = True)

# Suppression ligne résumé null
#df.dropna(subset = ["Resume","Description"],inplace = True)

# Creation d'une colonne pour chaque type de propriété
dummy_df = pd.get_dummies(df["type_propriete"])
df = pd.concat([df, dummy_df], axis=1)
df = df.drop("type_propriete", axis=1)

# Type de logement
df.loc[df.Type_logement=="Logement entier",'Type_logement']=1
df.loc[df.Type_logement=="Chambre privée",'Type_logement']=2
df.loc[df.Type_logement=="Chambre partagée",'Type_logement']=3

# Suppression colonne Description, Titre et Resume
df.drop(columns=["Description", "Titre","Resume"],inplace = True)

# Ajout des colonnes non existantes
columns = ['Latitude', 'Longitude', 'Capacite_accueil', 'NombreSdB', 'NbChambres',
       'NbLits', 'Type_logement', 'type_lit', 'Animal_sur_place', 'Cuisine',
       'Internet', 'television', 'produits_base', 'Shampooing', 'Chauffage',
       'Climatisation', 'machine_laver', 'seche_linge', 'parking_sur-place',
       'wifi', 'television_cable', 'petit_dejeuner', 'animaux_acceptes',
       'pourEnfants_famille', 'adapte_evenements', 'logement_fumeur',
       'accessibilite', 'Ascenseur', 'cheminee_interieur', 'Interphone',
       'Portier', 'Piscine', 'Jacuzzi', 'salle_sport', 'Entree_24-24',
       'Cintres', 'fer_repasser', 'seche_cheveux', 'espace_travail_ordi',
       'detecteur_fumee', 'monoxyde_carbone_detect', 'kit_secours',
       'fiche_securite', 'extincteur', 'porte_chambre_verrou',
       'rection_semaine', 'reduction_mois', 'surcout_voyageur_supp',
       'frais_menage', 'Caution', 'duree_minimale_sejour', 'Appartement',
       'Appartement en résidence', 'Autre', 'Bed & Breakfast', 'Bungalow',
       'Cabane', 'Dortoir', 'Inconnue', 'Loft', 'Maison', 'Maison de ville',
       'Maison écologique', 'Villa']

columnsDf = df.columns

columnsSomme = [*columnsDf,*columns]

columnsNoExisting = [n for n in columnsSomme if columnsSomme.count(n) == 1]

# Ajout des colonnes qui n'existent pas 
for i in range(len(columnsNoExisting)):
    df[columnsNoExisting[i]]=0

# réorganisation des colonnes 
df = df[columns]

## Prediction

# Chargement du modele
modele = load('modeleLineaire.modele')

# Chargement scaler
scaler = load('scaler.modele')

# Scaled données
df=scaler.transform(df)

# Création de la prédiction
res = []
for i in range(df.shape[0]):
    res.append(modele.predict([df[i]]).tolist()[0])

# Importation des données 
df = pd.read_csv("xdata.csv")
df['result']=res

# Création du csv
df.to_csv('resultat.csv')