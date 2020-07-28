

from openalea.mtg.draw import *
from oawidgets.plantgl import PlantGL
from oawidgets.mtg import *

from oawidgets.mtg import plot

from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scipy.stats import poisson, binom
import os
import timeit
import sys
sys.path.append("../../Task_2/src/")
from algo_bench import *

my_mtg = MTG()
#my_mtg = MTG('consolidated_mango3d.mtg')

dist = poisson(1., loc=1).rvs

vid = my_mtg.add_component(my_mtg.root)

random_tree(my_mtg, vid, nb_children=dist, nb_vertices=99)


#random_tree(my_mtg,vid, nb_children=dist,nb_vertices=99)

"""
t5 = timeit.default_timer()
clusters_1 = SFC_FF(my_mtg,vid,10)
t6 = timeit.default_timer()
"""
p = 10
t3 = timeit.default_timer()
First_Fit_Clustering_Paper(my_mtg,p)
t4 = timeit.default_timer()

print("Time for clustering with the first algorithm using the queue", t4-t3)

"""
for i in range(p):
    print("------------------------")
    print("Cluster",i,"with lenght",len(clusters_2[i]))
    print("with nodes ",clusters_2[i])
"""

print("Clusters ",my_mtg.property('cluster'))
print("Sub_tree roots ",my_mtg.property('sub_tree'))

