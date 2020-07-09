def SFC_BF_PAPER(T,p,alpha):
    
    C = [[] for i in range(p)]
    
    remain = 0
    
    weight = np.zeros(len(T))
    weight = weight.astype(int)
    
    
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
        
    
    c = int(len(T)/p)
    
    def BF(remain,first_time,Q,last_cluster):
       
        sub = None
        index = 0
        if last_cluster:
            sub = T.root
        
        elif first_time:
            for v in post_order(T,T.root):
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
                    for v in pre_order(T,Q[i]):
                        if T.parent(v) != None:
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                    Q[i] = None
                    i = i - 1    
    
            remove_weight = index
          
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
       

        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            #T.remove_tree(sub)
        elif sub == T.root:
            sub_tree_found = list(post_order(T,sub))
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        target = c
        remain = target
        first_time = True
        last_cluster = False
        Qu = [None for i in range(remain+1)]
        while len(C[i]) < (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
            
            sub = BF(remain,first_time,Qu,last_cluster)
            if sub == None:
                break
            remain = remain - len(sub)
            C[i] += sub
            first_time = False
    return C