from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scipy.stats import poisson, binom
import os
import timeit
import sys
from oawidgets.mtg import *
from oawidgets.plantgl import PlantGL
from openalea.mtg.draw import *
import sys

sys.path.append("../../Task_2/src/")

from algo import *

from oawidgets.mtg import plot
from oawidgets.plantgl import PlantGL


my_mtg = MTG()
#my_mtg = MTG('consolidated_mango3d.mtg')

dist = poisson(1., loc=1).rvs

vid = my_mtg.add_component(my_mtg.root)

random_tree(my_mtg,vid,nb_children=dist,nb_vertices=99)


#random_tree(my_mtg,vid, nb_children=dist,nb_vertices=99)

"""
t5 = timeit.default_timer()
clusters_1 = SFC_FF(my_mtg,vid,10)
t6 = timeit.default_timer()
"""
p = 10
t3 = timeit.default_timer()
Best_Fit_Clustering_1(my_mtg,vid,p,0.4)
t4 = timeit.default_timer()

#print("Time for clustering with the first algorithm based on paper",t2-t1)
print("Time for clustering with the first algorithm using the queue",t4-t3)
#print("Time for clustering with the second algorithm using queue removing the subtree",t6-t5)
#color = my_mtg.property('cluster')
#print(color)
"""
for i in range(p):
    print("------------------------")
    print("Cluster",i,"with lenght",len(clusters_2[i]))
    print("with nodes ",clusters_2[i])
""" 
#plot_clusters(my_copy,cluster=clusters_2)
cluster = my_mtg.property('cluster')
print("Clusters",cluster)
groups = my_mtg.property('color')
for j in [k for k,v in cluster.items() if v == 0]:
    groups[j] = 0
print(groups)