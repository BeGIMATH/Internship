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

from algo_bench import *
from algo_distributed_mpi import *
from oawidgets.mtg import plot
from oawidgets.plantgl import PlantGL
from IPython.display import HTML
from IPython.display import IFrame

from mpi4py import MPI

test_mtg = MTG()#'../data/noylum2.mtg')
dist = poisson(1., loc=1).rvs

vid = test_mtg.add_component(test_mtg.root)

random_tree(test_mtg,vid,nb_children=dist,nb_vertices=99)

distributed_tree_traversal(test_mtg,Best_Fit_Clustering_Queue,"bottom_up")

distributed_tree_traversal(test_mtg,Best_Fit_Clustering_Paper,"top_down")
