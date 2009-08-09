"""
Searching Algorithms for Graphs v.1.0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

@copyright: Copyright (c) 2009, Rodrigo Carrasco <rodrigo.carrasco at gmail.com>
@author: mr_rax
"""
# general modules
from numpy import *                  # matrix manipulation
from time import *                   # timers
# personal modules and classes
from GraphClass import *             # graph class

"""
Main Algorithms
"""
def breath_first(*args):
    """
    breath first search of nodes from k (k-reachable nodes)
    
    @type G: graph
    @param G: graph
    
    @note: optional parameter
    @type k: int
    @param k: source node
    
    @rtype order: int vector
    @return order: bfs order of each node
    
    @rtype p: tree
    @return p: predecessor tree
    """
    # get arguments
    G = args[0]
    G = G.copy()
    
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr') or k == []:
        print 'ERROR: the graph is not directed or has no source set'
        return [[], []]
    
    # correct the position of the arcs to have them in ascending order
    G = sort_arcs(G, "ascending")
    
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
    
    # initialize predecessor list
    p = inf * ones(n, int)      # all set as infinity...
    p[k-1] = 0                  # ...except k which is set as source
    
    # ordering variables
    order = inf * ones(n, int)  # gives the order of each node
    order[k-1] = 0
    position = 1                # variable for assigning order
    
    # list of nodes
    list = [k]                  # 1 -> node will be tested
        
    # keep on searching while there are nodes in the list
    while size(list) != 0:
        i = list[0]             # get the first node in the list
        list = delete(list, 0)  # eliminate it from the list
        
        # add all arcs from i to the list
        pos = G.N[i-1,0]        # initial position of data for node i
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1
        while link != 0:
            # add the nodes that have not been used
            j = G.A[pos,1]      # head of the arc
            
            # check if the arc is admissible and has capacity
            if p[j-1] == inf and cap_ok(G.u, pos):
                list = append(list, j)  # add j to the list
                p[j-1] = i      # predecessor
                order[j-1] = position   # position of the node
                position = position + 1
            pos = G.A[pos,2]    # check next node
            link = pos
            
    return order, p

def depth_first(*args):
    """
    depth first search of nodes from k (k-reachable nodes)
    
    @type G: graph
    @param G: graph
    
    @note: optional parameter
    @type k: int
    @param k: source node
    
    @rtype order: int vector
    @return order: bfs order of each node
    
    @rtype p: tree
    @return p: predecessor tree
    """
    # get arguments
    G = args[0]                     # graph
    G = G.copy()
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr') or k == []:
        print 'ERROR: the graph is not directed or has no source set'
        return [[], []]
    
    # correct the position of the arcs to have them in ascending order
    G = sort_arcs(G, "ascending")
    
    A = G.A.copy()              # duplicate A for doing the search
    N = G.N.copy()              # duplicate N for doing the search
    u = G.u.copy()              # duplicate u for doing the search
    
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
    
    # initialize predecessor list
    p = inf * ones(n)           # all set as infinity...
    p[k-1] = 0                  # ...except k which is set as source
    
    # ordering variables
    order = inf * ones(n, int)  # gives the order of each node
    order[k-1] = 0
    position = 1                # variable for assigning order
    
    # list of nodes
    list = [k]                  # 1 -> node will be tested
    # keep on searching while there are nodes in the list
    while size(list) != 0:
        last_pos = size(list) - 1
        i = int(list[last_pos]) # get the first node in the list
        pos = N[i-1,0]          # first data point for node i
        if pos < 0:             # if no arcs are left
            list = delete(list, last_pos)   # eliminate the node from the list
        else:
            # add the nodes that have not been used
            j = A[pos,1]        # head of the arc
            
            # check if the arc is admissible and has capacity
            if p[j-1] == inf and cap_ok(u, pos):
                list = append(list, j)  # add j to the list
                p[j-1] = i      # predecessor
                order[j-1] = position   # position of the node
                position = position + 1
            
            # eliminate the arc from the list
            A = delete(A, s_[pos], axis=0)
            if size(u) != 0:
                u = delete(u, pos)
            # correct the N matrix
            if N[i-1,0] == N[i-1,1]:
                N[i-1,0], N[i-1,1] = -1, -1
            else:
                N[i-1,1] = N[i-1,1] -1
            # reduce N for all other nodes j < i
            for k in range(i, n):
                N[k,0] = N[k,0] - 1
                N[k,1] = N[k,1] - 1
    
    return order, p

def topological(*args):
    """
    topological search of nodes - looks for a root
    
    @type G: graph
    @param G: graph
    
    @rtype order: int vector
    @return order: bfs order of each node
    
    @rtype p: tree
    @return p: predecessor tree
    """
    # get arguments
    G = args[0]                     # graph
    G = G.copy()
    
    # check if it a valid Graph
    if not G.is_correct_type('d'):
        print 'ERROR: the graph is not directed'
        return [[], []]
    
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
    
    # initialize predecessor list
    p = inf * ones(n)           # all set as infinity...
    t_p = zeros(n, int)
    
    # initialize variables
    indegree = zeros(n)         # in-degree of each node
    order = zeros(n)            # topological order of each node
    
    # set the in-degree of each node
    for arc in range(m):
        j = G.A[arc,1]          # head of the arc
        indegree[j-1] = indegree[j-1] + 1
    
    # set the list of nodes with in-degree 0
    list = zeros(n)             # 0=does not belong to list, 1=does
    for node in range(n):
        # if it has in-degree 0, add it to list
        if indegree[node] == 0:
            list[node] = 1
        
    # iterate till the list is empty
    position = 0                # variable for assigning topological order
    while max(list) == 1:
        i = argmax(list) + 1    # get the smallest node in the list
        list[i-1] = 0           # eliminate it from the list
        order[i-1] = position   # assign order
        # set predecessor
        p[i-1] = t_p[i-1]
        position = position + 1
        
        # go through adjacency list of node i and reduce it's in-degree
        pos = G.N[i-1,0]        # starting point of data for node i
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1            # initialization of link variable
        while link != 0:
            j = G.A[pos,1]      # head of the arc
            t_p[j-1] = i        # temporal predecessor
            indegree[j-1] = indegree[j-1] - 1   # reduce the in-degree of the arc
            # check if it is 0 to add it to the list
            if indegree[j-1] == 0:
                list[j-1] = 1
            # get next arc position
            link = int(G.A[pos,2])
            pos = link
    
    # if not all nodes were ordered, a cycle exists
    if max(order) < n - 1:
        print 'CYCLE: The graph has a directed cycle, no topological order exists'
        return [[], []]
    else:
        return order, p

"""
Auxiliary Functions
"""
def cap_ok(u, pos):
    """
    checks the capacity of the arc in pos, returning true if it is
    > 0 or no capacity vector exists
    
    @type u: float vector
    @param u: capacity of each arc
    
    @type pos: number
    @param pos: position of the arc
    
    @rtype: boolean
    @return: indicate if the capacity of the arc is OK    
    """
    if size(u) == 0:
        return True
    elif u[pos] > 0:
        return True
    else:
        return False

def sort_arcs(*args):
    """ 
    sorts the adjacency matrix to make sure that it is in
    ascending/descending order (also sorts c, u and f)
    
    @type G: graph
    @param G: graph
    
    @note: optional argument
    @type type: string
    @param type: sorting order (ascending or descending)
    
    @rtype: graph
    @return: sorted graph
    """
    # get arguments
    G = args[0]                     # graph
    
    # if a second argument exists -> type
    if len(args) > 1:
        type = args[1]
    else:
        type = "ascending"
    
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
    
    # initialize matrices
    N = -1 * ones((n,2), int)
        
    # stick c, u and f to A for sorting
    M = array(G.A.copy()).T
    if size(G.c) != 0:
        M = vstack([M, G.c])
    if size(G.u) != 0:
        M = vstack([M, G.u])
    if size(G.f) != 0:
        M = vstack([M, G.f])
    if size(G.mirror) != 0:
        M = vstack([M, G.mirror])           # link for residual graphs
        M = vstack([M, array(range(m))])    # index to correct the order
    M = M.T
    
    # trick to sort by first col and then second col
    Ms = 10 * M[:,0] + M[:,1]
    # sort the matrix
    sort_order = Ms.argsort()
    if type == "ascending":
        M = M[sort_order]
    else:
        M = M[sort_order[range(size(sort_order) - 1, -1, -1)]]
    
    # get the arc data back
    c, u, f, mirror = empty(0), empty(0), empty(0), empty((0,2), float)
    if size(G.c) != 0:
        c = M[:,3]
        M = delete(M, s_[3], axis=1)
    if size(G.u) != 0:
        u = M[:,3]
        M = delete(M, s_[3], axis=1)
    if size(G.f) != 0:
        f = M[:,3]
        M = delete(M, s_[3], axis=1)
    if size(G.mirror) != 0:
        mirror = M[:,3]
        M = delete(M, s_[3], axis=1)
        # get the mixed indices
        s_mirr = M[:,3]
        M = delete(M, s_[3], axis=1)
        # order them and apply it to mirror
        index_order = s_mirr.argsort()
        mirror = index_order[array(mirror, int)]
    
    # correct the link of A and build N
    for arc in range(m):
        i = M[arc,0]            # head of the arc
        
        # if it is the first arc, set N[i-1,0]
        if N[i-1,0] == -1:
            N[i-1,0] = arc      # initial data point
        N[i-1,1] = arc          # update last data point
        # correct the link
        if arc < m - 1:
            # check if next arc is also from i
            if M[arc+1,0] == i:
                M[arc,2] = arc + 1
            else:
                M[arc,2] = 0
        else:
            # the last line has only a 0
            M[arc,2] = 0
    
    # correct the variables
    G.A = M
    G.N = N
    G.c = c
    G.u = u
    G.f = f
    G.mirror = mirror
    
    return G

def sort_nodes(G, order):
    """ 
    sorts the node numbers according to an ordering vector
    
    @type G: graph
    @param G: graph
    
    @type order: number vector
    @param order: ordering vector
    
    @rtype: graph
    @return: sorted graph
    """
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
        
    # correct arc names according to their new order
    for arc in range(m):
        # correct the node names of each arc
        G.A[arc,0] = order[G.A[arc,0] - 1] + 1
        G.A[arc,1] = order[G.A[arc,1] - 1] + 1
        
    # correct external flow positions
    B = array(G.B).copy()
    B = B[array(order).argsort(),:]
    
    # correct coordinates
    coord = empty((0,2), float)
    if size(G.coord) != 0:
        coord = G.coord.copy()
        coord = coord[array(order).argsort(),:]
    
    # re-build the rest of the graph by ordering the arcs
    G = sort_arcs(G, "ascending")
    G.coord = coord
    G.B = B
    
    return G
        
"""
GUI Menu Function
"""
def menu_items():
    """ 
    returns the list of algorithms available for populating the GUI menu
    
    @param: None
    
    @rtype: list
    @return: list of algorithms and menu to add to the GUI 
    """
    menu_name = "Search & Order"
    algorithm_list = [["Breath First Search", board_breath_first],
                      ["Depth First Search", board_depth_first],
                      ["Topological Search", board_topological],
                      ["separator", "separator"],
                      ["Breath First Sort", board_breath_first_sort],
                      ["Depth First Sort", board_depth_first_sort],
                      ["Topological Sort", board_topological_sort]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_breath_first(board):
    print "\nBreath First Search Algorithm"
    ini_time = clock()
    order, p = breath_first(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "order of nodes: ", order
    print "BFS Tree: ", p
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if order != []:
        board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_depth_first(board):
    print "\nDepth First Search Algorithm"
    ini_time = clock()
    order, p = depth_first(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "order of nodes: ", order
    print "DFS Tree: ", p
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if order != []:
        board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_topological(board):
    print "\nTopological Search Algorithm"
    ini_time = clock()
    order, p = topological(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "order of nodes: ", order
    print "Topological Tree: ", p
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if order != []:
        board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_breath_first_sort(board):
    print "\nBreath First Search Algorithm with Sorting"
    # sort the nodes
    order, p = breath_first(board.graph)
    
    print "\nResults:"
    print "order of nodes: ", order
    print "BFS Tree: ", p
    
    if order != []:
        # sort only if all nodes have an order
        if max(p) != inf:
            # apply sorting
            board.graph = sort_nodes(board.graph, order)
            print "Graph Sorted"
            # correct the predecessor list
            for node in range(size(p)):
                if p[node] != 0:
                    p[node] = order[int(p[node])-1] + 1
            p = p[array(order).argsort()]
        else:
            print "Not all nodes are reachable - no sorting was done"
        board.draw_graph()
        board.draw_tree(p)
    else:
        print "No result from the search method - no sorting was done"
        board.draw_graph()
    print "-----------------------------------------------------------------"
    
def board_depth_first_sort(board):
    print "\nDepth First Search Algorithm with Sorting"
    # sort the nodes
    order, p = depth_first(board.graph)
    
    print "\nResults:"
    print "order of nodes: ", order
    print "DFS Tree: ", p
    
    if order != []:
        # sort only if all nodes have an order
        if max(p) != inf:
            # apply sorting
            board.graph = sort_nodes(board.graph, order)
            # correct the predecessor list
            for node in range(size(p)):
                if p[node] != 0:
                    p[node] = order[int(p[node])-1] + 1
            p = p[array(order).argsort()]
        else:
            print "Not all nodes are reachable - no sorting was done"
        board.draw_graph()
        board.draw_tree(p)
    else:
        print "No result from the search method - no sorting was done"
        board.draw_graph()
    print "-----------------------------------------------------------------"
    
def board_topological_sort(board):
    print "\nTopological Search Algorithm with Sorting"
    order, p = topological(board.graph)
    
    print "\nResults:"
    print "order of nodes: ", order
    print "Topological Tree: ", p
    
    if order != []:
        # sort only if all nodes have an order
        if max(p) != inf:
            # apply sorting
            board.graph = sort_nodes(board.graph, order)
            print "Graph Sorted"
            # correct the predecessor list
            for node in range(size(p)):
                if p[node] != 0:
                    p[node] = order[int(p[node])-1] + 1
            p = p[array(order).argsort()]
        else:
            print "Not all nodes are reachable - no sorting was done"
        board.draw_graph()
        board.draw_tree(p)
    else:
        print "No result from the search method - no sorting was done"
        board.draw_graph()
    print "-----------------------------------------------------------------"