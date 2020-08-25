"""Implementation of a number of MTG clustering algorithms"""

from tools import *

def Best_Fit_Clustering_MTG(T, p, alpha):
    ''' Clustering MTG(Tree) based on the paper of Hambrusch and Liu but modified for better performance

        :Parameters:
         - `T` (MTG) The MTG(Tree) which we want to cluster
         - `p`  (int) - The number of clusters we want to fill
         - 'alpha' (float) - The parameter which controls the difference on size between different clusters
        :Returns:
            All the clusters as a list of lists of all the nodes of the tree
        :Returns Type:
            List
    '''
    cluster = T.property('cluster')

    remain = 0

    weight = np.zeros(len(T))
    internode_root = T.roots(T.max_scale())

    a = T.roots(T.max_scale())
    c_omponent = a[0]
    
    weight = np.zeros(len(T))
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])

    c = int(len(T)/p)
    color = set()
    
    def Best_Fit(remain, Q, last_cluster, cluster_index):

        sub = None
        if last_cluster:
            sub = c_omponent

        else:
            for vid in post_order2(T, c_omponent, pre_order_filter=lambda v: v not in color):
                if T.parent(vid) != None:
                    if weight[vid] <= (1+alpha)*remain and weight[T.parent(vid)] > remain + alpha:
                        Q.append(vid)
                        if weight[vid] > (1-alpha/2)*remain:
                            break

            if Q.size() > 0:
                sub = Q.pop()
                index = weight[sub]
                for w in list(ancestors(T, sub)):
                    weight[w] = weight[w] - index
       
        color.add(sub)
        for v in post_order2(T, sub, pre_order_filter=lambda v: v not in color):
            cluster[v] = cluster_index
        
        

    remain = 0
    last_cluster = False
    for i in range(p):
        Qu = Priority_queue(weight)
        target = c
        if i == p-1:
            last_cluster = True
        Best_Fit(target, Qu, last_cluster, i)
        

def Best_Fit_Clustering_MTG_1(T, p, alpha):
    ''' Clustering MTG(Tree) based on the paper of Hambrusch and Liu but modified for better performance
    Now it uses level order instead of post order for finding the good subtrees

        :Parameters:
         - `T` (MTG) The MTG(Tree) which we want to cluster
         - `p`  (int) - The number of clusters we want to fill
         - 'alpha' (float) - The parameter which controls the difference on size between different clusters
        :Returns:
            All the clusters as a list of lists of all the nodes of the tree
        :Returns Type:
            List
    '''
    cluster = T.property('cluster')
    color = T.property('color')

    a = T.roots(T.max_scale())
    c_omponent = a[0]

    weight = np.zeros(len(T))
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])

    c = int(len(T)/p)
    

    def BF(remain, Q, last_cluster):

        sub = None

        if last_cluster:
            sub = c_omponent

        else:

            for vid in level_order(T, c_omponent, pre_visitor_filter=lambda v: v not in color):
                if T.parent(vid) != None:
                    if weight[vid] <= (1+alpha)*remain and weight[T.parent(vid)] > remain + alpha:
                        Q.append(vid)
                        if weight[vid] > (1-alpha/2)*remain:
                            break

            if Q.size() > 0:
                sub = Q.pop()
                index = weight[sub]
                for w in list(ancestors(T, sub)):
                    weight[w] = weight[w] - index

        color[sub] = sub
        
        for v in post_order2(T, sub, pre_order_filter=lambda v: v not in color):
            cluster[v] = cluster_index
        
    last_cluster = False
    for i in range(p):
        Qu = Priority_queue(weight)

        target = c
        if i == p-1:
            last_cluster = True

        BF(target, Qu, last_cluster)
