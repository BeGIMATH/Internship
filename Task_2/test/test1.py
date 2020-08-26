

from openalea.mtg.draw import *
from oawidgets.plantgl import PlantGL
from oawidgets.mtg import *

from oawidgets.mtg import *

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
from tools import *
from algo_bench_mtg import *
from algo_mtg import *

algos = [Best_Fit_Clustering_Paper_MTG,First_Fit_Clustering_Paper_MTG,Best_Fit_Clustering_post_order_MTG,Best_Fit_Clustering_level_order_MTG]

my_mtg = MTG()
#np.random.seed(seed=233423)
dist = poisson(1., loc=1).rvs

vid = my_mtg.add_component(my_mtg.root)

random_tree(my_mtg, vid, nb_children=dist, nb_vertices=99999)
#plot(my_mtg)
for p in [8,16,32,64,128]:
    for algo in algos:
        if my_mtg.property('cluster') != {}:
            my_mtg.remove_property('cluster')
        if my_mtg.property('sub_tree') != {}:
            my_mtg.remove_property('sub_tree')
        if algo != First_Fit_Clustering_Paper_MTG:
            algo(my_mtg,p,0.4)
            print("Longest path for ",algo.__name__ ,longest_path(my_mtg,p))

        #plot_clusters_dict(my_mtg,nb_cluster=10,file_name = algo.__name__ + 'clusters')
        #plot_clusters_dependecy(my_mtg,nb_cluster=10,file_name = algo.__name__ + '_dependecy')
        else:
            algo(my_mtg,p) 
            print("Longest path for ",algo.__name__ ,longest_path(my_mtg,p))

        #plot_clusters_dict(my_mtg,nb_cluster=10,file_name = algo.__name__ + 'clusters')
        #plot_clusters_dependecy(my_mtg,nb_cluster=10,file_name = algo.__name__ + '_dependecy')
