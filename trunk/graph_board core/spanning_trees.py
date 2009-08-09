"""
Spanning Tree Algorithms for Graphs v.1.0

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
# personal modules and classes
from GraphClass import *             # graph class
from graph_board import *            # drawing board class

"""
Main Algorithms
"""
def kruskal(*args):
    """
    obtain the minimum spanning tree using Kruskal's algorithm
    
    @type G: graph
    @param G: graph
    
    @note: optional parameter
    @type k: int
    @param k: node of start of the algorithm
    
    @rtype: list
    @return: list of arcs in the tree 
    """
    # get arguments
    G = args[0]                     # graph
    
    # if a second argument exists set as starting point
    if len(args) > 1:
        k = args[1]
    elif G.source != []:
        k = G.source
    else:
        k = 1
        
    # check if it is a valid Graph
    if not G.is_correct_type('u'):
        print 'ERROR: the graph is not in one of the valid formats for kruskal()'
        return []
    if size(G.c) == 0:
        print 'ERROR: the graph has no cost/distance values'
        return []
    
    # get graph parameters
    n = G.nodes()
    # check if all nodes are reachable from k
    if sum(G.u_reach_from(k)) < n:
        print 'ERROR: the graph is not connected: not all nodes are reachable'
        return []
    
    # set of nodes
    S = zeros(n, int)               # stores the set level of each node
    max_level = 0                   # store highest level (to speed the algorithm)
    arc_set = empty(0, int)         # arcs in the minimum spanning tree
    
    # add arcs in an ordered way
    arc_order = argsort(G.c)
    print "nodes    : ", array(range(n)) + 1
    print "node sets: ", S
    
    # create a file to store the steps
    draw_graph(G, ["style", "write", "kruskal.ps"], ["coloring", S], ["arc_set", arc_set])
    
    # add arcs in order
    for arc in arc_order:
        # arc end points
        i = G.A[arc,0]
        j = G.A[arc,1]
        
        # if a change occurs, iindicate it to add a page on the output file
        re_draw = False
        if S[i-1] == 0 or S[j-1] == 0 or S[i-1] != S[j-1]:
            re_draw = True
        
        # if both nodes are not connected, add a level and the arc
        if S[i-1] == 0 and S[j-1] == 0:
            max_level += 1
            S[i-1] = max_level
            S[j-1] = max_level
            arc_set = append(arc_set, arc)
            
        # if one is without level add the level of the other and the arc
        elif S[i-1] == 0 and S[j-1] != 0:
            S[i-1] = S[j-1]
            arc_set = append(arc_set, arc)
        elif S[i-1] != 0 and S[j-1] == 0:
            S[j-1] = S[i-1]
            arc_set = append(arc_set, arc)
        
        # if both are set but different, merge levels and add arc
        elif S[i-1] != S[j-1]:
            # merge with the smallest set
            min_merge = min(S[i-1], S[j-1])
            max_merge = S[i-1] + S[j-1] - min_merge
            
            # correct the maximum set
            max_level = 0
            # correct the set levels
            for node in range(n):
                # correct maximum set
                if S[node] > max_level:
                    max_level = S[node]
                # merge levels
                if S[node] == max_merge:
                    S[node] = min_merge
            arc_set = append(arc_set, arc)
            # if the max_level reached 0 break the loop
            if max_level == 0:
                break
        
        # if it was the case, add a step to the output file
        if re_draw:
            draw_graph(G, ["style", "append", "kruskal.ps"],\
                       ["coloring", S], ["arc_set", arc_set])
        
        # if both are set but equal, skip this arc
        print "node sets: ", S
    
    return arc_set

def prim(*args):
    """
    obtain the minimum spanning tree using Kruskal's algorithm
    
    @type G: graph
    @param G: graph
    
    @note: optional parameter
    @type k: int
    @param k: node of start of the algorithm
    
    @rtype: tree
    @return: minimum spanning tree 
    """
    # get arguments
    G = args[0]                     # graph
    
    # if a second argument exists set as starting point
    if len(args) > 1:
        k = args[1]
    elif G.source != []:
        k = G.source
    else:
        k = 1
        
    # check if it a valid Graph
    if not G.is_correct_type('u'):
        print 'ERROR: the graph is not in one of the valid formats for prim()'
        return []
    if size(G.c) == 0:
        print 'ERROR: the graph has no cost/distance values'
        return []
    
    # get graph parameters
    n = G.nodes()
    
    # check if all nodes are reachable from k
    if sum(G.u_reach_from(k)) < n:
        print 'ERROR: the graph is not connected: not all nodes are reachable'
        return []
    
    # initialize predecessor vector
    p = inf * ones(n)
    p[k-1] = 0                      # start at k
    
    # set of nodes
    S = array([k])                  # nodes already set
    
    # create a file to store the steps
    draw_graph(G, ["style", "write", "prim.ps"], ["tree", p])
    
    # add arcs till we have a tree
    while size(S) < n:
        print "nodes in set: ", S
        
        # get arcs in the cut
        arc_list = array(G.get_cut_arcs_pos(S), int)
        
        # look for the one with the minimum cost
        cost = inf
        for arc in arc_list:
            # if the cost is smaller, update
            if G.c[arc] < cost:
                min_arc = arc
                cost = G.c[arc]
        
        # get arc data
        i = int(G.A[min_arc,0])
        j = int(G.A[min_arc,1])
        
        # if it is forward add j to S and update
        if sum(S == i) > 0:
            S = append(S,j)
            p[j-1] = i
        # if it is backwards, swap the arc and add it
        else:
            G.swap_arc(min_arc)
            S = append(S,i)
            p[i-1] = j
          
        # add a step to the output file
        draw_graph(G, ["style", "append", "prim.ps"], ["tree", p])
    
    print "nodes in set: ", S
    
    return p

"""
Auxiliary Functions
"""

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
    menu_name = "Spanning Trees"
    algorithm_list = [["Kruskal's Algorithm", board_kruskal],
                      ["Prim's Algorithm", board_prim]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_kruskal(board):
    print "\nMinimum Spanning Tree, Kruskal's Algorithm"
    # optimize & and add the flow
    ini_time = clock()
    arc_set = kruskal(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "set of arcs: ", arc_set
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if arc_set != []:
        print "Total Cost: ", board.graph.total_arc_set_cost(arc_set)
        board.draw_arc_set(arc_set)
    print "-----------------------------------------------------------------"
    
def board_prim(board):
    print "\nMinimum Spanning Tree, Prim's Algorithm"
    # optimize & and add the flow
    ini_time = clock()
    p = prim(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "predecessor vector: ", p
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if p != []:
        print "Total Cost: ", board.graph.total_tree_cost(p)
        board.draw_tree(p)
    print "-----------------------------------------------------------------"