"""
Shortest Path Algorithms for Graphs v.1.0

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
from GraphClass import *             # Graph classes
    
"""
Main Algorithms
"""
def shortest_path_dag(*args):
    """
    shortest path algorithm for Directed Acyclic Graphs
    
    @type G: graph
    @param G: graph
    
    @type k: int
    @param k: root node for the shortest path tree
    
    @rtype p: tree
    @return p: shortest path tree rooted at k
    
    @rtype d: int vector
    @return d: distance labels
    """
    # get arguments
    G = args[0]                     # graph
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr'):
        print 'Warning: the graph is not in one of the valid formats for shortest_path_generic()'
        return [[], 0]
    
    if size(G.c) == 0 or k == []:
        print 'ERROR: the graph has no cost/distance values or no source set'
        return [[], 0]
    
    # check if the graph is in topological order
    if not G.is_top_sort():
        print 'ERROR: the graph must be in topological order'
        return [[], 0]
    
    # node number
    n = G.nodes()
    
    # check if all nodes are reachable from k
    if sum(G.reach_from(k)) < n:
        print 'Warning: not all nodes are reachable from node', k
    
    # initialize distance labels
    d = inf * ones(n)                # set all to infinity
    d[k-1] = 0                       # set node k as source
    # initialize predecessor list
    p = inf * ones(n)                # all set as infinity...
    p[k-1] = 0                       # ...except k which is set as source
    
    # update node labels and predecessors in topological order
    for node in range(int(k-1), n):
        pos = G.N[node,0]           # initial position of data for node
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1                 # initialization of link variable
        # search all adjacent arcs of node i (until link=0)
        while link != 0:
            # search for an arc without the opt. condition and u>0
            i = G.A[pos,0]           # tail of arc
            j = G.A[pos,1]           # head of arc
            c = G.c[pos]             # cost/distance of arc
            if size(G.u) != 0:
                u = G.u[pos]         # capacity cap of arc
            else:
                u = []
            # check if the arc breaks the optimality condition
            if d[j-1] > d[i-1] + c and (u > 0 or u == []):
                # if it finds one, corrects the labels
                d[j-1] = d[i-1] + c  # update label
                p[j-1] = i           # update predecessor
                
            # look for the next arc in the adjacency list
            link = G.A[pos,2]
            pos = link               # get next position
    
    return [p, d]

def shortest_path_dijkstra(*args):
    """
    shortest path using Dijkstra's algorithm
    
    @type G: graph
    @param G: graph
    
    @type k: int
    @param k: root node for the shortest path tree
    
    @rtype p: tree
    @return p: shortest path tree rooted at k
    
    @rtype d: int vector
    @return d: distance labels
    """
    # get arguments
    G = args[0]
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr'):
        print 'Warning: the graph is not in one of the valid formats for shortest_path_dijkstra()'
        return [[], 0]
        
    if size(G.c) == 0 or k == []:
        print 'ERROR: the graph has no cost/distance values or no source set'
        return [[], 0]
    
    # check if all costs are positive
    if min(G.c[:]) < 0:
        print("ERROR: for using Dijkstra's Algorithm all weights must be positive")
        return [[], 0]
    
    # number of nodes
    n = G.nodes()
       
    # check if all nodes are reachable from k
    if sum(G.reach_from(k)) < n:
        print 'Warning: not all nodes are reachable from node', k
    
    # initialize set S
    S = zeros(n)                     # indicates which labels have been set (1=set, 0=not)
    # initialize distance labels
    d = inf * ones(n)                # set all to infinity
    d[k-1] = 0                       # set node k as source
    # initialize predecessor list
    p = inf * ones(n)                # all set as infinity...
    p[k-1] = 0                       # ...except k which is set as source
    
    # iterate while at least one node is not in S
    while min(S) == 0:
        # get i, the node in S.complement with the smallest label
        d_min = inf                  # initialize distance
        i = 0                        # initialize argmin
        for node in range(n):
            # if the distance is smaller or equal (to catch inf), and node not set correct
            if d[node] <= d_min and S[node] == 0:
                d_min = d[node]
                i = node
        i = i + 1                    # node with smallest distance
        S[i-1] = 1                   # adds node i to S
        
        pos = G.N[i-1,0]             # initial position of data for N(i)
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1                 # initialization of link variable
        # search all adjacent arcs of node i (until link=0)
        while link != 0:
            # search for an arc without the opt. condition and u>0
            j = G.A[pos,1]           # link node
            c = G.c[pos]             # cost/distance of arc
            if size(G.u) != 0:
                u = G.u[pos]         # capacity cap of arc
            else:
                u = []
            # check if the arc breaks the optimality condition
            if d[j-1] > d[i-1] + c and (u > 0 or u == []):
                # if it finds one, corrects the labels
                d[j-1] = d[i-1] + c  # update label
                p[j-1] = i           # update predecessor
                
            # look for the next arc in the adjacency list
            link = int(G.A[pos,2])
            pos = link               # get next position
    
    return [p, d]

def shortest_path_generic(*args):
    """
    shortest path using the generic labeling algorithm
    
    @type G: graph
    @param G: graph
    
    @type k: int
    @param k: root node for the shortest path tree
    
    @rtype p: tree
    @return p: shortest path tree rooted at k
    
    @rtype d: int vector
    @return d: distance labels
    
    @rtype nc_flag: boolean
    @return nc_flag: true if a negative cycle is detected
    
    @rtype nc_path: path
    @return nc_path: negative cycle path
    """
    # get arguments
    G = args[0]
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr'):
        print 'Warning: the graph is not in one of the valid formats for shortest_path_generic()'
        return [[], 0, 0, 0]
            
    if size(G.c) == 0 or k == []:
        print 'ERROR: the graph has no cost/distance values or no source set'
        return [[], 0, 0, 0]
    
    # get graph parameters
    n = G.nodes()
    C = max([max(G.c), max(-G.c)])   # maximum cost of arcs (abs)
    
    # check if all nodes are reachable from k
    if sum(G.reach_from(k)) < n:
        print 'Warning: not all nodes are reachable from node', k
    
    # initialize flags
    nc_flag = False                  # indicates if a negative cycle is found
    nc_path = matrix([[]])           # path of the negative cycle
    # initialize distance labels vector
    d = inf * ones(n)                # all set as infinity...
    d[k-1] = 0                       # ...except k which is set as source
    # initialize predecessor list
    p = inf * ones(n)                # all set as infinity...
    p[k-1] = 0                       # ...except k which is set as source    
    
    # check if the shortest path condition is satisfied
    cond, i, j, pos = short_path_cond(G, d)    # pos indicates arc that does not comply
    while cond:
        d[j-1] = d[i-1] + G.c[pos]             # update label
        p[j-1] = i                   # update predecessor
        # check if a negative cycle exists
        D = min(d)                   # smallest distance label
        if D < -n*C:                 # if it is smaller than -nC we have a n.cycle
            nc_flag = True
            break
        
        # otherwise keep on looking for the optimality condition
        cond, i, j, pos = short_path_cond(G,d)
    
    # if a negative cycle was detected, give the nodes that belong to it
    if nc_flag:
        nc_path = get_sp_cyle(p, d)  # get cycle
    
    return [p, d, nc_flag, nc_path]
    
def shortest_path_fifo(*args):
    """
    shortest path using the FIFO implementation of the
    label correcting algorithm
    
    @type G: graph
    @param G: graph
    
    @type k: int
    @param k: root node for the shortest path tree
    
    @rtype p: tree
    @return p: shortest path tree rooted at k
    
    @rtype d: int vector
    @return d: distance labels
    
    @rtype nc_flag: boolean
    @return nc_flag: true if a negative cycle is detected
    
    @rtype nc_path: path
    @return nc_path: negative cycle path
    """
    # get arguments
    G = args[0]
    # if a second argument exists set as source
    if len(args) > 1:
        k = args[1]
    else:
        k = G.source
        
    # check if it a valid Graph
    if not G.is_correct_type('dr'):
        print 'Warning: the graph is not in one of the valid formats for shortest_path_fifo()'
        return [[], 0, 0, 0]
    if size(G.c) == 0 or k == []:
        print 'ERROR: the graph has no cost/distance values or no source set'
        return [[], 0, 0, 0]
    
    # get graph parameters
    n = G.nodes()
    C = max([max(G.c), max(-G.c)])   # maximum cost of arcs (abs)
    # check if all nodes are reachable from k
    if sum(G.reach_from(k)) < n:
        print 'Warning: not all nodes are reachable from node', k
    
    # initialize flags
    nc_flag = False                  # indicates if a negative cycle is found
    nc_path = matrix([[]])           # path of the negative cycle
    # initialize distance labels vector
    d = inf * ones(n)                # all set as infinity...
    d[k-1] = 0                       # ...except k which is set as source
    # initialize predecessor list
    p = inf * ones(n)                # all set as infinity...
    p[k-1] = 0                       # ...except k which is set as source
    # initialize list of violating nodes
    list = inf * ones(n)             # inf means it is not in the list
    step = 1
    list[k-1] = step                 # puts node k on the list
    
    # iterate while some node belongs to list
    while min(list) != inf:
        i = argmin(list) + 1         # get the first node of the list (FIFO)
        list[i-1] = inf              # ...and eliminate it
        
        pos = G.N[i-1,0]             # initial position of data for node i
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1                 # initialization of link variable
        # search all adjacent arcs of node i (until link=0)
        while link != 0:
            # search for an arc without the opt. condition and u>0
            j = G.A[pos,1]           # link node
            c = G.c[pos]             # cost/distance of arc
            if size(G.u) != 0:
                u = G.u[pos]         # capacity cap of arc
            else:
                u = []
            # check if the arc breaks the optimality condition
            if d[j-1] > d[i-1] + c and (u > 0 or u == []):
                # if it does not, correct the labels
                d[j-1] = d[i-1] + c  # update label
                p[j-1] = i           # update predecessor
                # if node j is not in the list, add it
                if list[j-1] == inf:
                    step = step + 1
                    list[j-1] = step
                
            # look for the next arc in the adjacency list
            link = G.A[pos,2]
            pos = link               # get next position
            
        # check if a negative cycle exists
        D = min(d)                   # smallest distance label
        if D < -n*C:                 # if it is smaller than -nC we have a n.cycle
            nc_flag = True
            break
    
    # if a negative cycle was detected, give the nodes that belong to it
    if nc_flag:
        nc_path = get_sp_cyle(p, d)  # get cycle
    
    return [p, d, nc_flag, nc_path]

"""
Auxiliary Functions
"""
def short_path_cond(G, d):
    """
    check the shortest path optimality condition using distance labels d
    returning the node pair that brakes it
    
    @type G: graph
    @param G: graph
    
    @type d: int vector
    @param d: distance labels
    
    @rtype cond: boolean
    @return cond: true if optimality break is detected
    
    @rtype i: int
    @return i: tail of arc that breaks the condition
    
    @rtype j: int
    @return j: head of arc that breaks the condition
    
    @rtype pos: int
    @return pos: position of the arc 
    """
    # number of nodes
    n = G.nodes()
    
    # initialize condition
    cond = False
    
    # scan each node and check all its adjacent arcs
    for node in range(n):            # search all arcs along all nodes
        # initial position of data for N(node)
        pos = G.N[node,0]
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1                 # initialization of link variable
        # search all arcs of this node (until link=0)
        while link != 0:
            # search for an arc without the opt. condition and u>0
            i = G.A[pos,0]           # start node
            j = G.A[pos,1]           # link node
            c = G.c[pos]             # cost/distance of arc
            if size(G.u) != 0:
                u = G.u[pos]         # capacity cap of arc
            else:
                u = []
            # check if the arc breaks the optimality condition
            if d[j-1] > d[i-1] + c and (u > 0 or u == []):
                # if it does, set non-opt condition and return
                cond = True
                return [cond, i, j, pos]
            
            # otherwise, look for the next arc from this node
            link = G.A[pos,2]
            # get next position
            pos = link
            
    return [cond, i, j, pos]

def get_sp_cyle(p, d):
    """
    get a cycle form a predecessor list p, using distance labels d
    
    @type p: int vector
    @param p: predecessor list
    
    @type d: int vector
    @param d: distance labels for each node
    
    @rtype: path
    @return: cycle path    
    """
    # amount of nodes in G
    n = size(d)
    
    # list of amount of times a node is visited
    visits = zeros(n)
    # position of node that lifted the nc_flag
    k = argmin(d)
    # first node of the path
    t_path = array([k+1])
    # temp var for following the path
    pos = k
    # increase number of visits for initial node
    visits[pos] = visits[pos] + 1
    while max(visits) < 2:
        # follow predecessor
        pos = p[pos] - 1
        # add the new node
        t_path = append(t_path, pos + 1)
        # increase number of visits
        visits[pos] = visits[pos] + 1
        
    # clean the initial "tail" if there was one
    k = 0
    last_node = t_path[size(t_path) - 1]
    while t_path[k] != last_node:
        k = k + 1
        
    # get the clean path
    cycle_path = t_path[k:size(t_path)]
    # reverse it to have it in the correct order
    cycle_path = cycle_path[range(size(cycle_path)-1,-1,-1)]
    
    return cycle_path

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
    menu_name = "Shortest Path"
    algorithm_list = [["DAG", board_shortest_path_dag],
                      ["Dijkstra's", board_shortest_path_dijkstra],
                      ["separator", "separator"],
                      ["Generic Label Correcting", board_shortest_path_generic],
                      ["Label Correcting FIFO", board_shortest_path_fifo]]
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_shortest_path_dag(board):
    print "\nShortest Path: DAG Algorithm"
    ini_time = clock()
    p, d = shortest_path_dag(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "p: ", p
    print "d: ", d
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if p != []:
        print "Total Cost: ", board.graph.total_tree_cost(p)
        board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_shortest_path_dijkstra(board):
    print "\nShortest Path: Dijkstra's Algorithm"
    ini_time = clock()
    p, d = shortest_path_dijkstra(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "p: ", p
    print "d: ", d
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if p != []:
        print "Total Cost: ", board.graph.total_tree_cost(p)
        board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_shortest_path_generic(board):
    print "\nShortest Path: Generic Label Correcting Algorithm"
    ini_time = clock()
    p, d, nc_flag, nc_path = shortest_path_generic(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "p: ", p
    print "d: ", d
    print 'nc_flag: ', nc_flag
    print 'nc_path: ', nc_path
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if p != []:
        if nc_flag:
            print "Negative Cycle Detected"
            board.draw_path(nc_path)
        else:
            print "Total Cost: ", board.graph.total_tree_cost(p)
            board.draw_tree(p)
    print "-----------------------------------------------------------------"
    
def board_shortest_path_fifo(board):
    print "\nShortest Path: Label Correcting Algorithm - FIFO Implementation"
    ini_time = clock()
    p, d, nc_flag, nc_path = shortest_path_fifo(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "p: ", p
    print "d: ", d
    print 'nc_flag: ', nc_flag
    print 'nc_path: ', nc_path
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if p != []:
        if nc_flag:
            print "Negative Cycle Detected"
            board.draw_path(nc_path)
        else:
            print "Total Cost: ", board.graph.total_tree_cost(p)
            board.draw_tree(p)
    print "-----------------------------------------------------------------"