

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
import pickle 
sys.path.append("../../Task_2/src/")
from algo_bench import *
t3 = timeit.default_timer()
my_mtg = MTG()
#my_mtg = MTG('consolidated_mango3d.mtg')

dist = poisson(1., loc=1).rvs

vid = my_mtg.add_component(my_mtg.root)

#random_tree(my_mtg, vid, nb_children=dist, nb_vertices=99)
random_tree(my_mtg, vid, nb_children=dist, nb_vertices=999999)


#random_tree(my_mtg,vid, nb_children=dist,nb_vertices=99)

"""
t5 = timeit.default_timer()
clusters_1 = SFC_FF(my_mtg,vid,10)
t6 = timeit.default_timer()
"""
p = 10
t4 = timeit.default_timer()


print("Time it takes to create a mtg", t4-t3)

t1 = timeit.default_timer()
test1_mtg = my_mtg.copy()
t2 = timeit.default_timer()
print("Time it takes to copy a mtg", t2-t1)



t1 = timeit.default_timer()
filename = 'dogs'
outfile = open(filename,'wb')
pickle.dump(my_mtg,outfile,protocol=3)
outfile.close()
t2 = timeit.default_timer()
print("Time for serializing using pickle", t2-t1)


t1 = timeit.default_timer()
infile = open(filename,'rb')
test_mtg = pickle.load(infile)
infile.close()
t2 = timeit.default_timer()
print("Time for de-serializing using pickle", t2-t1)

algos = [Best_Fit_Clustering_Queue,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order]
for algo in algos:
    t1 = timeit.default_timer()
    algo(test_mtg,p,0.4)
    t2 = timeit.default_timer()
    print("Time for clustering with the ", algo.__name__ ," algorithm", t2-t1)
