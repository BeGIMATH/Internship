
"""Implementation of a number of Tree clustering algorithms to benchmark the algorithms in terms of distributed computing performance"""

from Queue import *

def Best_Fit_Clustering_Paper(T, p, alpha):
    ''' Clustering Trees based on the paper of Hambrusch and Liu

        :Parameters:
         - `T` (Tree) The tree which we want to cluster
         - `p`  (int) - The number of clusters we want to fill
         - 'alpha' (float) - The parameter which controls the difference on size between different clusters
        :Returns:
            All the clusters as a list of lists of all the nodes of the tree
        :Returns Type:
            List
        '''
    C = [[] for i in range(p)]
    remain = 0
    weight = np.zeros(len(T))
    weight = weight.astype(int)
    c_omponent = T.component_roots(T.root)[0]
    for v in post_order(T,c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    c = int(len(T)/p)
    sub_tree = T.property('sub_tree')
    cluster = T.property('cluster')
    def Best_Fit(remain,first_time,Q,last_cluster,cluster_index):
       
        sub = None
        index = 0
        if last_cluster:
            sub = c_omponent
        
        elif first_time:
            for v in post_order2(T,c_omponent,pre_order_filter = lambda v: v not in sub_tree):
                if T.parent(v) != None:
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        if Q[weight[v]] == None:
                            Q[weight[v]] = v
                        if weight[v] <= remain and weight[v] + 1 > remain:    
                            break

            i = len(Q) - 1
            while i > 1:
                if Q[i] != None:
                    index = i
                    sub = Q[index]
                    Q[i] = None
                    break 
                i = i - 1
            
            i = index - 1
            if remain - index > 0:
                while i > remain - index:
                    for v in pre_order(T,Q[i]):
                        if T.parent(v) != None:
                            if weight[v] <= remain -index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                                
                    Q[i] = None
                    i = i-1
            
            
            remove_weight = index
        
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
           
        else:
            i = remain
            while i > 0:
                if Q[i] != None:
                    index = i
                    sub = Q[i] 
                    Q[i] = None
                    break 
                i = i - 1
            
            i = index
            if remain - index > 0:
                while i > remain - index:
                    for v in post_order2(T,Q[i],pre_order_filter = lambda v: v not in sub_tree):
                        if T.parent(v) != None:
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                    Q[i] = None
                    i = i - 1    
    
            remove_weight = index
          
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
       

        if sub != c_omponent:
            sub_tree[sub] = cluster_index
            sub_tree_found = list(post_order2(T,sub,pre_order_filter = lambda v: v not in sub_tree))
            for v in sub_tree_found:
                cluster[v] = cluster_index
            
        elif sub == c_omponent:
            sub_tree[sub] = cluster_index
            sub_tree_found = list(post_order2(T,sub,pre_order_filter = lambda v: v not in sub_tree))
            for v in sub_tree_found:
                cluster[v] = cluster_index
        return sub_tree_found
        
    remain = 0
    
    for i in reversed(range(p)):
        target = c
        remain = target
        first_time = True
        last_cluster = False
        Qu = [None for i in range(remain+1)]
        while remain > 1:
            if i == 0:
                last_cluster = True
            
            sub = Best_Fit(remain,first_time,Qu,last_cluster,i)
            if sub == None:
                break
            remain = remain - len(sub)
            
            first_time = False
    
def Best_Fit_Clustering_Queue(T,p,alpha):
    ''' Clustering Trees based on the paper of Hambrusch and Liu but modified for better performance

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
    c_omponent = T.component_roots(T.root)[0]
    weight = np.zeros(len(T))
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])

    c = int(len(T)/p)
    sub_tree = T.property('sub_tree')
    def Best_Fit(remain, first_time, Q, last_cluster, cluster_index):

        sub = None
        if last_cluster:
            sub = c_omponent

        elif first_time:
            for vid in post_order2(T, c_omponent, pre_order_filter=lambda v: v not in sub_tree):
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
                        for v in pre_order(T, node):
                            if T.parent(v):
                                if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                    Q.append(v)

                for w in list(ancestors(T, sub)):
                    weight[w] = weight[w] - index

        else:

            sub = Q.pop()
            index = weight[sub]

            if remain - index > 0:
                while weight[Q.last()] > remain - index:
                    node = Q.pop()
                    for v in pre_order(T, node):
                        if T.parent(v):
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q.append(v)

            remove_weight = weight[sub]

            for w in list(ancestors(T, sub)):
                weight[w] = weight[w] - remove_weight

        if sub != c_omponent:
            sub_tree[sub] = cluster_index
            sub_tree_found = list(post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree))
            
            for v in post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree):
                cluster[v] = cluster_index
        
        elif sub == c_omponent:
            sub_tree[sub] = cluster_index
            sub_tree_found = list(post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree))
            
            for v in post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree):
                cluster[v] = cluster_index
        return sub_tree_found

    for i in reversed(range(p)):
        Qu = Priority_queue(weight)

        target = c
        remain = target
        first_time = True
        last_cluster = False
        while remain > 1:

            if i == 0:
                last_cluster = True
            if remain < 1:
                break

            sub = Best_Fit(remain, first_time, Qu, last_cluster,i)

            remain = remain - len(sub)

            first_time = False


def First_Fit_Clustering_Paper(T,p):
    ''' Clustering Trees based on the paper of Hambrusch and Liu but modified for better performance

        :Parameters:
         - `T` (MTG) The MTG(Tree) which we want to cluster
         - `p`  (int) - The number of clusters we want to fill
        :Returns:
            All the clusters as a list of lists of all the nodes of the tree
        :Returns Type:
            List
    '''
    cluster = T.property('cluster')
    sub_tree = T.property('sub_tree')
    c_omponent = T.component_roots(T.root)[0]
    vtx_id = c_omponent
    weights = np.zeros(len(T))
    for v in post_order(T, c_omponent):
        weights[v] = 1 + sum([weights[vid] for vid in T.children(v)])

    visited = set([])

    def order_children(vid):
        ordered = []
        p_queue = Priority_queue(weights)
        for vid in T.children(vid):
            p_queue.append(vid)
        while p_queue.size() > 0:
            node = p_queue.pop()
            ordered.append(node)
        return ordered

    c = int(len(T)/p)

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
            if vtx_id != c_omponent:
                if (weights[T.parent(vtx_id)] > c) or  (math.ceil((counter+1)/c) != math.ceil(counter/c)):
                    sub_tree[vtx_id] = p - 1 - (math.ceil(counter/c)-1)
                    remove_weight = weights[vtx_id]
                    for w in list(ancestors(T, vtx_id)):
                        weights[w] = weights[w] - remove_weight
            elif vtx_id == c_omponent:
                sub_tree[vtx_id] = p - 1 -(math.ceil(counter/c)-1)
            cluster[vtx_id] = p - 1 - (math.ceil(counter/c)-1)
            queue.pop()
    
def Best_Fit_Clustering_Queue_1(T,p, alpha):
    ''' Clustering Trees based on the paper of Hambrusch and Liu but modified for better performance
        Improvemnt of the function Best_Fit_Clustering, so that it does not change the structure of the tree during processing
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
    sub_tree = T.property('sub_tree')
    C = [[] for i in range(p)]
    weight = np.zeros(len(T))
    c_omponent = T.component_roots(T.root)[0]
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])

    c = int(len(T)/p)

    def Best_Fit(remain, Q, last_cluster, cluster_index):
        sub = None
        if last_cluster:
            sub = c_omponent
        else:
            for vid in post_order2(T, c_omponent, pre_order_filter=lambda v:v not in sub_tree):
                if T.parent(vid) != None:
                    if weight[vid] <= (1+alpha)*remain and weight[T.parent(vid)] > remain*(1 + alpha):
                        Q.append(vid)
                        if weight[vid] > (1-alpha/2)*remain:
                            break

            if Q.size() > 0:
                sub = Q.pop()
                index = weight[sub]
                for w in list(ancestors(T, sub)):
                    weight[w] = weight[w] - index

        sub_tree[sub] = cluster_index
        for v in post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree):
            cluster[v] = cluster_index
        
    last_cluster = False
    for i in reversed(range(p)):
        Qu = Priority_queue(weight)
        target = c
        if i == 0:
            last_cluster = True

        Best_Fit(target, Qu, last_cluster, i)





def Best_Fit_Clustering_No_Queue(T,p, alpha):
    ''' Clustering Trees based on the paper of Hambrusch and Liu but modified for better performance
    Now, it uses level-order traversal instead of post-order to find the trees

        :Parameters:
         - `T` (MTG) The MTG(Tree) which we want to cluster
         - `p`  (int) - The number of clusters we want to fill
         - 'alpha' (float) - The parameter which controls the difference on size between different clusters
        :Returns:
            All the clusters as a list of lists of all the nodes of the tree
        :Returns Type:
            List
    '''
    weight = np.zeros(len(T))
    c_omponent = T.component_roots(T.root)[0]
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    cluster = T.property('cluster')
    sub_tree = T.property('sub_tree')
    c = int(len(T)/p)

    def Best_Fit(remain, Q, last_cluster, cluster_index):
        sub = None
        if last_cluster:
            sub = c_omponent
        else:
            for vid in level_order2(T, c_omponent, visitor_filter=lambda v: v not in sub_tree):

                if T.parent(vid) != None:
                    if weight[vid] <= (1+alpha)*remain and weight[T.parent(vid)] > remain*(1 + alpha):
                        Q.append(vid)
                        if weight[vid] > (1-alpha/2)*remain:
                            break

            if Q.size() > 0:
                sub = Q.pop()
                index = weight[sub]
                for w in list(ancestors(T, sub)):
                    weight[w] = weight[w] - index

        
        sub_tree[sub] = cluster_index
        for v in post_order2(T, sub, pre_order_filter=lambda v: v not in sub_tree):
            cluster[v] = cluster_index
        
    
    last_cluster = False
    for i in reversed(range(p)):
        Qu = Priority_queue(weight)
        target = c
        if i == 0:
            last_cluster = True

        Best_Fit(target, Qu, last_cluster, i)




"""
Experimental work
"""

def Best_Fit_Clustering_No_Queue_1(T,p, alpha):
    ''' Clustering MTG(Tree) based on the paper of Hambrusch and Liu but modified for better performance
    Find as many subtrees as possible by just one traversal using the level-order traversal

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
    sub_tree = T.property('sub_tree')
    c_omponent = T.component_roots(T.root)[0]
    queue = []
    queue.append(c_omponent)
    node = queue.pop(0)
    for vid in T.children(node):
        queue.append(vid)

    remain = 0

    weight = np.zeros(len(T))
    for v in post_order(T, c_omponent):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    c = int(len(T)/p)

    def Best_Fit(remain, Q, last_cluster,cluster_index):

        sub = None

        if last_cluster:
            sub = c_omponent

        else:
            if len(queue) > 0:
                while len(queue) > 0:
                    node = queue.pop(0)
                    if weight[node] <= (1+alpha)*remain and weight[node] > (1-alpha/2)*remain:
                        sub = node
                        break
                    if weight[node] > (1+alpha)*remain:
                        for vid in T.children(node):
                            queue.append(vid)
            else:
                queue.append(c_omponent)
                while len(queue) > 0:
                    node = queue.pop(0)
                    if weight[node] <= (1+alpha)*remain and weight[node] > (1-alpha/2)*remain:
                        sub = node
                        break
                    if weight[node] > (1+alpha)*remain:
                        for vid in T.children(node):
                            queue.append(vid)

        index = weight[sub]
        for w in list(ancestors(T, sub)):
            weight[w] = weight[w] - index

        sub_tree[sub] = cluster_index
        for v in post_order2(T,sub,pre_order_filter = lambda v: v not in sub_tree):
            cluster[v] = cluster_index
 
    remain = 0
    last_cluster = False
    for i in reversed(range(p)):
        Qu = Priority_queue(weight)

        target = c
        if i == p-1:
            last_cluster = True
        Best_Fit(target, Qu, last_cluster,i)
        
