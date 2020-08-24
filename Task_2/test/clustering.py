from openalea.mtg.draw import *
from oawidgets.plantgl import PlantGL
from oawidgets.mtg import *
import timeit
import os
from scipy.stats import poisson, binom
from openalea.mtg.traversal import *
from openalea.mtg.io import *
from openalea.mtg.algo import ancestors
from openalea.mtg.mtg import *
from oawidgets.mtg import plot

import sys

sys.path.append("../../Task_2/src/")
from algo import *




my1_mtg = MTG('../data/consolidated_mango3d.mtg')


