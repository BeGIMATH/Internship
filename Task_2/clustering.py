from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math
import os
import timeit
import sys
sys.path.insert(0, '/Task_2/Queue.py/')


from Queue import *


from scipy.stats import poisson, binom 

my_mtg = MTG()
my_mtg1 = MTG()
my_mtg2 = MTG()
dist = poisson(1., loc=1).rvs
#random_tree(my_mtg,my_mtg.root, nb_children=dist,nb_vertices=999)
random_tree(my_mtg1,my_mtg1.root, nb_children=dist,nb_vertices=999)
random_tree(my_mtg2,my_mtg2.root, nb_children=dist,nb_vertices=999)


t1 = timeit.default_timer()
clusters = SFC_BF(my_mtg,10,0)
t2 = timeit.default_timer()

t3 = timeit.default_timer()
clusters_1 = SFC_FF(my_mtg1,10)
t4 = timeit.default_timer()


t5 = timeit.default_timer()
clusters_2 = SFC_FF_1(my_mtg2,10)
t6 = timeit.default_timer()



print("Time for clustering with the first algorithm ",t2-t1)
print("Time for clustering with the second algorithm",t4-t3)
print("Time for clustering with the third algorithm",t6-t5)


