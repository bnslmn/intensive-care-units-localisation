# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 12:22:55 2020

@author: GIANG Cécile
"""

####### --- PROJET MOGPL: OPTIMISATION APPLIQUEE A LA GEOLOCALISATION --- #######
####### --- D'UNITES DE SOIN ET A LA PRISE EN CHARGE DES PATIENTS     --- #######


import numpy as np
from gurobipy import *


# ------------------------- PREPARATION DES DONNEES -------------------------

import csv

with open('villes.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    csv_data = [row for row in csv_reader]
    

# Vecteur des populations par ville
v = np.array([row[0] for row in csv_data[1:]], dtype=int)

# Matrice des distances entre deux villes
# Nous avons choisi de créér une matrice symétrique pour faciliter nos calculs

d = np.array([[0 if i=='' else int(i) for i in row[2:]] for row in csv_data[1:]])
d += d.T

# Création du dictionnaire reliant chaque ville à son indice
villes = dict()
tmp = csv_data[0][2:]
for i in csv_data[0][2:]:
    villes[csv_data[0][2:].index(i)] = i.replace(" ", "")



# ------- EXERCICE 1: REPARTITION DES PATIENTS DANS LES UNITES DE SOIN -------


m = Model('exo1')

# I ensemble des indices de villes.
# On note n son cardinal.
I = [i for i in range(len(d))]
n = len(I)

# J ensemble des indices des villes où il y a une unité de soins.
# On note k son cardinal.
# e.g: Nice, Le Havre, Dijon : J = [1,11,13]
#J = [0,1,2,3,4,5,6,7]
#J=[0,3,4,8,14]
#J = [2,7,14]
#J=[1,4,5,7]

J = [1,3,10,12]
k = len(J)



# declaration variables de decision
x = m.addVars(n, k, vtype=GRB.BINARY, lb=0)


# maj du modele pour integrer les nouvelles variables
m.update()


# On veut minimiser GLOBALEMENT la distance entre les villes et leur secteur: cela peut 
# mener à quelques problèmes: (ex1: les habitants d'une villes-secteurs doivent
# aller très loin car pop. faible, au profit de plus grandes villes)

obj = LinExpr();
for i in range(n):
    for j in range(k):
        obj += d[i,J[j]]* v[i] * x[i,j]
obj /= np.sum(v)



# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)


# Definition des contraintes

# Contrainte 1: Pour un secteur j fixé, la population totale des villes composant
#               ce secteur ne doit pas dépasser gamma

alpha = 1.281857203
gamma = ((1 + alpha)/k) * np.sum(v)

for j in range(k):
    m.addConstr(quicksum(v[i]*x[i,j] for i in range(n)) <= gamma)

# Contrainte 2: Les secteurs forment une partition des n villes 
#               (autrement dit, la somme des xij est égale à n)

m.addConstr(quicksum(quicksum(x[i,j] for j in range(k)) for i in range(n)) == n)


# Contrainte 3: Une ville n'appartient qu'à un unique secteur

for i in range(n):
    m.addConstr(quicksum(x[i,j] for j in range(k)) == 1)


# Fonction d'affichage du résultat en format texte
def affiche_secteurs(M, I, J, display = True):
    """ Retourne l'affichage texte des secteurs correspondant
        à la solution optimale M.
        @param M: int array x array, matrice de la solution optimale
        @param I: int array, liste de toutes les villes
        @param J: int array, liste des villes-secteurs
        @return None
    """
    sol = dict()
    
    # Initialisation des clés et valeurs du dictionnaire
    for j in J:
        sol[villes[j]] = []
    
    # Liste ordonnée des indices j dans M où M[i,j] vaut 1
    index = [np.where(row == 1)[0][0] for row in M]
    
    for i in range(len(index)):
        sol[villes[J[index[i]]]].append(villes[i])
    
    if display:
        print('\nLes secteurs sont:')
        for key in sol:
            print('\tSecteur', key, ': ', sol[key])


# Resolution
m.optimize()

print('\nValeur de la fonction objectif pour alpha =', alpha, ':', m.objVal)

# -- Autre affichage:
    
solution = np.zeros((n,k), dtype=int)
for i in range(n):
    for j in range(k):
        solution[i, j] = x[i, j].x

### ERREUR SI ALPHA TROP PETIT:
if np.sum(solution) < n:
    raise ValueError('Aucune solution satisfiable: augmenter alpha !')

print('\nSolution optimale:\n', solution)
print('\n', affiche_secteurs(solution, I, J))