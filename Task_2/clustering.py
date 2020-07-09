from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scipy.stats import poisson, binom
import os
import timeit
import sys
from oawidgets.mtg import plot
from oawidgets.plantgl import PlantGL
sys.path.insert(0, '/Task_2/Queue.py/')

from Queue import *


from oawidgets.mtg import plot
from oawidgets.plantgl import PlantGL

my_mtg = MTG()
dist = poisson(1., loc=1).rvs
vid = my_mtg.add_component(my_mtg.root)

my_mtg_1 = MTG()

random_tree(my_mtg,vid,nb_children=dist,nb_vertices=99)

random_tree(my_mtg_1,my_mtg_1.root, nb_children=dist,nb_vertices=99)

#random_tree(my_mtg,vid, nb_children=dist,nb_vertices=99)

#plot(my_mtg)

t5 = timeit.default_timer()
clusters_2 = SFC_FF(my_mtg,10)
t6 = timeit.default_timer()

t3 = timeit.default_timer()
clusters_1 = SFC_BF(my_mtg_1,10,0)
t4 = timeit.default_timer()


#print("Time for clustering with the first algorithm based on paper",t2-t1)
print("Time for clustering with the first algorithm using the queue",t4-t3)
print("Time for clustering with the second algorithm ",t6-t5)


for i in range(10):
    print("Cluster ",i,"using a queue")
    print("-------------------")
    print(clusters_1[i])



    print("Cluster ",i,"using a weight ordering")
    print("-------------------")
    print(clusters_2[i])


