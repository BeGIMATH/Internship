from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math

class Priority_queue:
    def __init__(self,weights):
        self.heapList = [0]
        self.currentSize = 0
        self.weights = weights
        

    def Empty(self):
        return self.currentSize == 0

    def percUp(self,i):
        while i // 2 > 0:
          if self.weights[self.heapList[i]] > self.weights[self.heapList[i // 2]]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2

    def append(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.maxChild(i)
          if self.weights[self.heapList[i]] < self.weights[self.heapList[mc]]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def maxChild(self,i):
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

def SFC_BF(T,c_omponent,p,alpha):
    
    C = [[] for i in range(p)]
    
    remain = 0
    
    weight = np.zeros(len(T))
    
    for v in post_order(T,c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    c = int(len(T)/p)
    color = set()
    def BF(remain,first_time,Q,last_cluster):
        
        sub = None
        
        if last_cluster:
            sub = c_omponent
        
        elif first_time:
        
            for vid in post_order2(T,c_omponent,pre_order_filter = lambda v: v not in color):
                if T.parent(vid) != None:
                    if weight[vid] <= remain and weight[T.parent(vid)] > remain:
                        Q.append(vid)
                        if weight[vid] + 1 > remain:
                            break
               
            if Q.size() > 0:
                sub = Q.pop()

                index = weight[sub]
           
                if remain - index > 0:
                    while weight[Q.last()] > remain - index:
                        node = Q.pop()
                        for v in pre_order(T,node):
                            if T.parent(v):
                                if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                    Q.append(v)
                               
               
                
                for w in list(ancestors(T,sub)):
                    weight[w] = weight[w] - index
            
        else:
                    
            sub = Q.pop()
            index = weight[sub]
            
            if remain - index > 0:
                while weight[Q.last()] > remain - index:
                    node = Q.pop()   
                    for v in pre_order(T,node):
                        if T.parent(v):
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q.append(v)

                     

            remove_weight = weight[sub]
        
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
       
        
        
        if sub != T.root:   
            sub_tree_found = list(post_order(T,sub))
        
            T.remove_tree(sub)
        elif sub==c_omponent:
            sub_tree_found = list(post_order2(T,c_omponent,pre_order_filter = lambda v: v not in color))        
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        Qu = Priority_queue(weight)
        
        target = c
        remain = target 
        first_time = True
        last_cluster = False
        while len(C[i]) <= (1 - alpha/2)*target:
            
            if i == p-1:
                last_cluster = True
            if remain < 1:
                break    
            
            sub = BF(remain,first_time,Qu,last_cluster)
                
            remain = remain - len(sub)
            
            C[i] += sub
            
            first_time = False
    return C





def SFC_FF(tree,c_omponent,p):
    vtx_id = c_omponent
    C = [[] for i in range(p)]
    weights = np.zeros(len(tree))
    for v in post_order(tree,c_omponent):
        weights[v] = 1 + sum([weights[vid] for vid in tree.children(v)])
   
    visited = set([])
    def order_children(vid):
        ordered = []
        p_queue = Priority_queue(weights)
        for vid in tree.children(vid):
            p_queue.append(vid)
        while p_queue.size() > 0:
            node = p_queue.pop()
            ordered.append(node)
        return ordered

    
    c = int(len(tree)/p)
    
    
    queue = [vtx_id]
    
    counter = 0
    while queue:
        vtx_id = queue[-1]
        for vid in order_children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: 
            counter += 1
            visited.add(vtx_id)
            C[math.ceil(counter/c)-1].append(vtx_id)
            queue.pop()
    return C

def weighted_postorder(tree,c_omponent,weights):
    vtx_id = c_omponent
    visited = set([])
    def order_children(vid):
        ordered = []
        p_queue = Priority_queue(weights)
        for vid in tree.children(vid):
            p_queue.append(vid)
        while p_queue.size() > 0:
            node = p_queue.pop()
            ordered.append(node)
        return ordered

 
    queue = [vtx_id]
    
    
    while queue:
        vtx_id = queue[-1]
        for vid in order_children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: 
            yield vtx_id
            visited.add(vtx_id)
            queue.pop()

    
def hybrid(T,c_omponent,p,alpha):
    
    C = [[] for i in range(p)]
    
    
    weight = np.zeros(len(T))
    
    for v in post_order(T,c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
        
    c = int(len(T)/p)
    target = c
    
    def BF(last_cluster):
        
        sub = None
        if last_cluster:
            sub = c_omponent
        sub_tree_size = 0
        
        for vid in weighted_postorder(T,c_omponent,weight):
            if weight[vid] >= target - alpha and weight[vid] <= target + alpha:
                sub = vid
                print("Found a good fit subtree of size ",weight[sub])
                break
          
        if sub != c_omponent:   
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub==c_omponent:
            sub_tree_found = list(post_order2(T,c_omponent))       
        return sub_tree_found
    last_cluster = False
    for i in range(p):
        
        if i == p-1:
            last_cluster = True
        print("Finding a subtree for cluster ",i)
        C[i] = BF(last_cluster)
    return C


def hybrid_1(T,c_omponent,p,alpha):
    
    C = [[] for i in range(p)]
    
    remain = 0
    
    weight = np.zeros(len(T))
    
    for v in post_order(T,c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    c = int(len(T)/p)
    color = set()
    
    def BF(remain,Q,last_cluster):
        
        sub = None
        
        if last_cluster:
            sub = c_omponent
        
        
        else:
            A = list(weighted_postorder(T,c_omponent,weight))
            
            for vid in A:
                if T.parent(vid) != None:
                    if weight[vid] <= remain + alpha and weight[T.parent(vid)] > remain:
                        Q.append(vid)
                        print("Found a subtree of size", weight[vid])
                        if weight[vid] + 1 > remain :
                            print("Found a perfect subtree of size",weight[vid])
                            break
               
            
            sub = Q.pop()    
            
                               
               
            index = weight[sub]
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - index 
        
        if sub != c_omponent:   
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub==c_omponent:
            sub_tree_found = list(post_order(T,c_omponent))
        return sub_tree_found
        
    remain = 0
    
    last_cluster = False
    for i in range(p):
        Qu = Priority_queue(weight)
        print("-----------------------------")
        print("Cluster ",i)
        target = c 
        remain = target
       
        
            
        if i == p-1:
            last_cluster = True
        sub = BF(remain,Qu,last_cluster)            
        C[i] += sub
        remain = remain -len(sub)
        print("Remain ",remain)
    return C