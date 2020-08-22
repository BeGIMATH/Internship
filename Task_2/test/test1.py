

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
np.random.seed(seed=233423)
dist = poisson(1., loc=1).rvs

vid = my_mtg.add_component(my_mtg.root)

random_tree(my_mtg, vid, nb_children=dist, nb_vertices=99)
#simple_tree(my_mtg, vid, nb_children=2, nb_vertices=99999)


#random_tree(my_mtg,vid, nb_children=dist,nb_vertices=99)

p = 10
algos = [Best_Fit_Clustering_level_order,First_Fit_Clustering_level_order]
tree_size = [10000,100000,100000]
nb_clusters = [5,10,20]      
for t_size in tree_size:
    my_mtg = MTG()
    dist = poisson(1., loc=1).rvs         
    vid = my_mtg.add_component(my_mtg.root)
    random_tree(my_mtg,vid,nb_children=dist,nb_vertices=t_size)
    for nb_clust in nb_clusters:
        for algo in algos:
            if my_mtg.property('cluster') != {}:
                my_mtg.remove_property('cluster')
            if my_mtg.property('sub_tree') != {}:
                my_mtg.remove_property('sub_tree')
    
            t1 = timeit.default_timer()
            if algo != First_Fit_Clustering_Paper:
                algo(my_mtg,p,0.4)
            else:
                algo(my_mtg,p)
    
            t2 = timeit.default_timer()
  
            print("Time for clustering with the ", algo.__name__ ," algorithm", t2-t1)
    
            plot_clusters_dependecy(my_mtg,nb_cluster=p,file_name = algo.__name__ + '_dependecy')
    