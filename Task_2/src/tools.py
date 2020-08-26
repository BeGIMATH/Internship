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


def level_order(T, vtx_id):
    queue = []
    
    queue.append(vtx_id)
    while len(queue) > 0:
        node = queue.pop(0)
        for vid in T.children(node):
            queue.append(vid)
        yield node


def level_order2(T, vtx_id, visitor_filter=None):
    queue = []
    
    if visitor_filter is None:
        visitor_filter = lambda x: True
    
    queue.append(vtx_id)
    while len(queue) > 0:
        node = queue.pop(0)
        for vid in T.children(node):
            if visitor_filter(vid):
                queue.append(vid)
        yield node

def dfs(node, adj, dp, vis): 
    vis[node] = True

    for i in range(0, len(adj[node])): 
        if not vis[adj[node][i]]: 
            dfs(adj[node][i], adj, dp, vis) 

        dp[node] = max(dp[node], 1 + dp[adj[node][i]]) 
	


def longest_path(T,p):
    sub_tree  = T.property('sub_tree')
    
    c_luster = T.property('cluster')
    vids = [i for i in range(p)]
    
    adj = [set() for i in range(p)]
    T.insert_scale(T.max_scale(), lambda vid:T.property('sub_tree').get(vid,None) != None)	

    for vid in T.vertices(scale=T.max_scale()-1):
        if T.parent(vid) is not None:
            adj[c_luster[T.parent(T.component_roots(vid)[0])]].add(c_luster[T.component_roots(vid)[0]])

    
    adj = [list(adj[i]) for i in range(p)]
    
    T.remove_scale(T.max_scale()-1)
    
    dp = [0] * p 
    
    visited = [False] * p 

    for i in range(p): 
        if not visited[i]: 
            dfs(i, adj, dp, visited) 
	
    length = 0
	
    for i in range(p): 
        length = max(length, dp[i]) 

    return length

def f_unc():
    for x in range(10000):
       x+=1
