# mogplProject
Modélisation et optimisation des charges d'unités de soins par la programmation linéaire et les graphes

Ce travail a été fait dans le cadre d'un projet de l'UE MOGPL du semestre 1 Master 1 STL 2020 / 2021 par Benslimane Amine et Cécile Giang.

=== EXERCICE 1: 'projetMOGPL_exo1.py'

Pour faire fonctionner le code:

Modifier la variable J pour changer les secteurs, J correspondant aux villes
(indices) où sont localisés les secteurs. Il est aussi possible de changer la 
variable alpha.

*******      Indexation à respecter pour I et J:     *******
Toulouse      : 0
Nice          : 1
Nantes        : 2
Montpellier   : 3
Strasbourg    : 4
Bordeaux      : 5
Lille         : 6
Rennes        : 7
Reims         : 8
Saint-Étienne : 9
Toulon        : 10
Le Havre      : 11
Grenoble      : 12
Dijon         : 13
Angers        : 14

Ainsi pour tester le programme linéaire avec les secteurs Nantes, Rennes et 
Grenoble, il faudra changer la variable J en:
J = [2, 7, 12]

La valeur de l'objectif correspond à la distance moyenne que doit parcourir un 
habitant pour se rendre à sa ville-secteur, pour la liste de secteurs J choisie.

=== EXERCICE 2.1: 'projetMOGPL_exo2.1.py'

Pour faire fonctionner le code:

Il suffit d'exécuter le code, après avoir éventuellement changé la valeur de 
alpha manuellement dans le script.
A l'exécution, il vous sera demandé de rentrer un nombre k. Il s'agit du nombre
de villes-secteurs (ie le nombre de villes avec une unité de soins) que vous 
voulez. Si le programme ne marche pas il faudra probablement augmenter le alpha.
(alpha > 0.3 pour k = 3).

La valeur de l'objectif correspond à la distance moyenne que doit parcourir un 
habitant pour se rendre à sa ville-secteur. La solution optimale affichée 
correspond aux affectation ville / ville-secteur. Un affichage textuel est 
fourni pour faciliter la lecture.
On affiche également la distance maximale que doit parcourir un habitant pour une
telle répartition en secteurs, afin de pouvoir comparer avec le résultat obtenu
en question 2.2 (comparer l'affichage de la distance maximal avec la valeur de
l'objectif obtenu en 2.2).


=== EXERCICE 2.2: 'projetMOGPL_exo2.2.py'

Pour faire fonctionner le code:

Il suffit d'exécuter le code, après avoir éventuellement changé la valeur de 
alpha manuellement dans le script.
A l'exécution, il vous sera demandé de rentrer un nombre k. Il s'agit du nombre
de villes-secteurs (ie le nombre de villes avec une unité de soins) que vous 
voulez. Si le programme ne marche pas il faudra probablement augmenter le alpha.
(alpha > 0.3 pour k = 3).

La valeur de l'objectif correspond à la distance maximale que doit parcourir un 
habitant pour se rendre à sa ville-secteur. A comparer avec l'affichage de la 
distance maximale obtenu pour le programme de la question 2.1
La solution optimale affichée correspond aux affectation ville / ville-secteur. Un affichage textuel est 
fourni pour faciliter la lecture.

=== EXERCICE 3: 'projetMOGPL_exo3.py'
Pour faire fonctionner le code:

il suffit d'executer le code, dans le rapport nous utilisons la notation x_{ij} qui est plus claire et plus mnémonique
mais dans le code nous préférons utiliser x_i pour ainsi faciliter l'implémentation. Toutefois il n'y a pas confusion.

Nous attirons votre attention que notre modèle s'applique pour chaque vecteur P donné, toutefois il va sans dire modifier
le PL pour chaque p_i.
Si par exemple nous prenons P=(50,150,275,25,0), on aura comme secteur donnant : Montpellier et Strasbourg
alors que Toulouse, Rennes et Reims seront des secteurs recevants, et cela va changer le programme linéaire.

Cependant la méthode reste simple à réaliser et sûrtout optimale.
