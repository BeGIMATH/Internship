from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 


class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def percUp(self,i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                #Swap places
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp 
            i = i // 2
    
    def insert(self,x):
        #Insert the element at the end of the list 
        self.heapList.append(x)
        #Increment the size variable
        self.currentSize = self.currentSize + 1 
        #Place the element based on its size
        self.percUp(self.currentSize)
    
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                #Swap the places 
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc] 
                self.heapList[mc] = tmp 
            i = mc 
    
    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i* 2
        else:
            if self.heapList[i * 2] < self.heapList[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1 
        self.heapList.pop()
        self.percDown(1)
        return retval 

    def delMax(self):
        retval = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        return retval
        
    def buildHeap(self,alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while i > 0:
            self.percDown(i)
            i = i - 1



"""
Function clustering
Parameters: Tree T, number of clusters p, parameter alpha
"""
def SFC_BF(T,p,alpha = 0.4,"algo",c):
    #Initializa the cluster
    C = [[] for i in range(p)]
    remain = np.zeros(p)
    target = 0     
    if "algo" = "BF":
        for i in range(1,p):
            target = c + remain[i-1]
            remain[i] = target 
            while(len(C[i]) < (1 - alpha/2)*target):
                #Find the best subtree
                tree = BF(T)
                #Delet the best subtree from the given tree
                T = T - tree 
                #Add those nodes to the cluster
                C[i-1] = C[i-1] + tree
                remain[i] = remain[i] - len(tree)
        return C 

    elif "algo" = "FF":
        for i in range(1,p):
            target = c + remain[i-1]
            remain[i] = target 
            while(len(C[i]) < (1 - alpha/2)):
                #Find the best subtree
                tree = FF(T)
                #Delet the best subtree from the given tree
                T = T - tree 
                #Add those nodes to the cluster
                C[i-1] = C[i-1] + tree
                remain[i] = remain[i] - len(tree)

    return C
    else:
        raise('No valid algorithm entered')
          
def BF(T):

    

def FF():
    pass 

def remove_tree():
clustering(5)


alist = [54,26,93,17,77,31,44,55,20]
mergeSort(alist)

#Function taken from mtg source code
def wheighted_post_order(tree, vtx_id):

    

    #Order children based on the size of subtrees they generate
    def order_children(vid):
        ''' Internal function to retrieve the children in a correct order:
            - Branch before successor.
        '''
        #Create a dictionary with the children of the nodes and their actual size
        #For each node of the tree store the size of the subtree it forms
        weight = np.zeros(len(tree))
        
        for v in post_order(tree,tree.root):
            weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])

        child_nodes = {v:wheight[v] for v in tree.children(vid)}
        value_list = list(child_nodes.values())
        key_list = list(child_nodes.keys())
        #Sort the values
        value_list = bubbleSort(values_list)
        reordered_nodes = []
        for i in range(len(node_list)):
            reordered_nodes.append(key_list[value_list.index(i)])
        
        return reordered_nodes

    visited = set([])
    
    queue = [vtx_id]
  
    while queue:

        vtx_id = queue[-1]
        for vid in order_children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            post_order_visitor(vtx_id)
            yield vtx_id
            visited.add(vtx_id)
            queue.pop()

def bubbleSort(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp

