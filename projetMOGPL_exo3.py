#!/usr/bin/python
#@AUTHOR : Benslimane Amine
# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *



nbcont=5
nbvar=6

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1,1,0,0,0,0],
     [0,0,1,1,0,0],
     [0,0,0,0,1,1],
     [1,0,1,0,1,0],     
     [0,1,0,1,0,1]]

# Second membre
b = [40, 20, 6, 40, 26]

# Coefficients de la fonction objectif
c = [242, 812, 791, 347, 894, 483]

m = Model("exo3")     
        
# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    if i==3 or i==4:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d" % i)
    else:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
   

# Resolution
m.optimize()


print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)

   
