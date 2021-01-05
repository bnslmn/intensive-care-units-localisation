# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 14:23:07 2020

@author: GIANG
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



# ------- EXERCICE 2.2: LOCALISATION OPTIMALE DES UNITES DE SOIN -------


m = Model('exo2.2')

# I ensemble des indices de villes.
# On note n son cardinal.
I = [i for i in range(len(d))]
n = len(I)

# On demande à l'utilisateur d'entrer le nombre k de secteurs voulus
print('Entrer le nombre k de secteurs : ')
k = int(input())

while k==0:
    print('On ne peut avoir k = 0 secteur. Rentrer k encore une fois: ')
    k = int(input())

# ----- declaration variables de decision

# Variables xij qui valent 1 si les patients de la ville i sont affectés au 
# secteur j, 0 sinon
x = m.addVars(n, n, vtype=GRB.BINARY, lb=0)

# Variables zj qui valent 1 si la ville j est un secteur, 0 sinon
z = m.addVars(n, vtype=GRB.BINARY, lb=0)

# Variable d qui est la distance maximale d'un habitant à son secteur pour un 
# certain k, et qu'il faut minimiser
d_max = m.addVar(vtype=GRB.CONTINUOUS, lb=0)


# maj du modele pour integrer les nouvelles variables
m.update()


# On veut minimiser la distance maximale entre les villes et leur secteur
obj = LinExpr();
obj += d_max


# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)


# Definition des contraintes

# Contrainte 1: Pour un secteur j fixé, la population totale des villes composant
#               ce secteur ne doit pas dépasser gamma

alpha = 0.5
gamma = ((1 + alpha)/k) * np.sum(v)

for j in range(n):
    m.addConstr(quicksum(v[i]*x[i,j] for i in range(n)) <= gamma)

# Contrainte 2: Les secteurs forment une partition des n villes 
#               (autrement dit, la somme des xij est égale à n)

m.addConstr(quicksum(quicksum(x[i,j]*z[j] for j in range(n)) for i in range(n)) == n)


# Contrainte 3: Une ville n'appartient qu'à un unique secteur

for i in range(n):
    m.addConstr(quicksum(x[i,j] for j in range(n)) == 1)
    
# Contrainte 4: les variables zi valent 0 ou 1

for i in range(n):
    m.addConstr(z[i] <= 1)

# Contrainte 5: il y a en tout k variables zi

m.addConstr(quicksum(z[i] for i in range(n)) == k)

# Contrainte 6: d est la distance maximale entre un habitant d'une ville i et 
#               un secteur j
for i in range(n):
    for j in range(n):
        m.addConstr(d[i,j] * x[i,j] * z[j] <= d_max)


# Fonction d'affichage du résultat en format texte
def affiche_secteurs(M, I, J, display = True):
    """ Retourne l'affichage texte des secteurs correspondant
        à la solution optimale M.
        @param M: int array x array, matrice n x n de la solution optimale
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

# J est la liste des villes-secteurs
J = np.where(np.array([z[i].x for i in range(n)]) == 1.0)[0]


####### ERREUR SI ALPHA EST TROP PETIT :

if len(J) < k:
    raise ValueError('Aucune solution satisfiable, augmenter alpha !')

# solution est la matrice n x k correspondant à la solution optimale

solution = np.zeros((n,k), dtype=int)

for i in range(n):
    for j in range(k):
        solution[i, j] = x[i, J[j]].x
        
print('\nSolution optimale:\n', solution)
print('\n', affiche_secteurs(solution, I, J))