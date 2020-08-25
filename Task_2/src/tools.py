from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
import numpy as np
import math


class Priority_queue:
    def __init__(self, weights):
        self.heapList = [0]
        self.currentSize = 0
        self.weights = weights

    def Empty(self):
        return self.currentSize == 0

    def percUp(self, i):
        while i // 2 > 0:
            if self.weights[self.heapList[i]] > self.weights[self.heapList[i // 2]]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def append(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.maxChild(i)
            if self.weights[self.heapList[i]] < self.weights[self.heapList[mc]]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def maxChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.weights[self.heapList[i*2]] > self.weights[self.heapList[i*2+1]]:
                return i * 2
            else:
                return i * 2 + 1

    def pop(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def size(self):
        return self.currentSize

    def last(self):
        return self.heapList[1]

# Iterative Method to traverse the tree in level-order
def level_order(T, vtx_id):
    # Create an empty queue for level order traversal
    queue = []
    # Enqueue Root and initialize height
    queue.append(vtx_id)
    while len(queue) > 0:
        node = queue.pop(0)
        for vid in T.children(node):
            queue.append(vid)
        yield node

# Iterative Method to traverse the tree in level-order
def level_order2(T, vtx_id, visitor_filter=None):
    # Create an empty queue for level order traversal
    queue = []
    if visitor_filter is None:
        visitor_filter = lambda x: True
    # Enqueue Root and initialize height
    queue.append(vtx_id)
    while len(queue) > 0:
        node = queue.pop(0)
        for vid in T.children(node):
            if visitor_filter(vid):
                queue.append(vid)
        yield node
# Check how well the clusters are balanced


def balance_valuation(T, clusters):
    nb_clusters = len(clusters)
    optimal_size = len(T)/nb_clusters
    max = 0
    for i in range(nb_clusters):
        if len(clusters[i]) > max:
            max = len(clusters[i])

    return max - optimal_size

# Compute the number of dependecies
def number_of_dependencies(T):
    cluster = T.property('cluster')
    max_dependecy = 0
    previous_node = None
    depth = 0
    same_cluster = False
    for node in T.property('sub_tree'):
        if previous_node is not None:
            #Reset depth to zero
            if cluster[previous_node] != cluster[node]:
                depth = 0

        while T.parent(node) != None:
            if cluster[T.parent(node)] != cluster[node]:
                depth += 1
            node = T.parent(node)
        previous_node = node
        max_dependecy = max(depth,max_dependecy)
        
    return max_dependecy

def Max_depth(node):
    childs = my_mtg.children(node)
    nodes = []
    leafs = []
    #Classify nodes either as leafs or as nodes
    for i in childs:
        if my_mtg.children(i) == None:
            leafs.append(i)
        else:
            nodes.append(i)
    #If the all
    if len(nodes) == 0:
        return 1
    if len(nodes) == 1:
        return Max_depth(nodes[0]) + 1
    else:
         return max(map(Max_depth,[nodes[i] for i in range(len(nodes))] )) + 1


def max_nb_dependecies(T):
    cluster = T.property('cluster')
    sub_tree = T.property('sub_tree')
    g.insert_scale(my_mtg.max_scale(), lambda vid: my_mtg.property('sub_tree').get(vid,None) != None)
    
    root = my_mtg.component_roots_at_scale_iter(my_mtg.root,scale=my_mtg.max_scale()-1)
    
    a = list(root)
    result = Max_depth(a[0])
    my_mtg.remove_scale(my_mtg.max_scale()-1)
    return result


