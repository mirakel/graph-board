"""
Min Cut Algorithms for Graphs v.1.0

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
from search_order import *           # search algorithms
from max_flow import *               # max flow algorithms

"""
Main Algorithms
"""
def min_cut_from_mf(*args):
    """
    algorithm to get the minimum cut given s and t using a max flow solution
    
    @type G: graph
    @param G: graph
    
    @note: optional parameters
    @type s: int
    @param s: source node
    
    @type t: int
    @param t: sink node
    
    @rtype: int vector
    @return: cut (nodes in the S part of the cut)
    """
    # get arguments
    G = args[0]
    
    # if a second argument exists set as source
    if len(args) > 1:
        s = args[1]
    else:
        s = G.source
    
    if len(args) > 2:
        t = args[2]
    else:
        t = G.sink
        
    # check if it a valid Graph
    if not G.is_correct_type('d'):
        print 'ERROR: the graph is not in one of the valid formats for labeling_max_flow()'
        return []
    
    if size(G.u) == 0 or s == [] or t == []:
        print 'ERROR: the graph has no capacities or no source/sink is set'
        return []
    
    print "Solving Max Flow Problem"
    # obtain the maximum flow
    G = labeling_max_flow(G)
    flow = G.f
    # add it if no error occurs
    if size(flow) == 0:
        return []
    
    print "Finding Minimum Cut"
    # get the residual graph
    R = G.residual_graph()
    # find the set of reachable nodes in R
    order, p = breath_first(R, s)   # do a search from s to all nodes
    n = size(p)                     # number of nodes
    cut = empty(0, int)
    
    # add connected nodes to the cut
    for node in range(n):
        # add the node if it is connected
        if p[node] != inf:
            cut = append(cut, node + 1)
    
    return cut

def global_min_cut(*args):
    """
    algorithm to get the minimum s-t cut
    
    @type G: graph
    @param G: graph
    
    @note: optional parameters
    @type s: int
    @param s: source node
    
    @type t: int
    @param t: sink node
    
    @rtype: int vector
    @return: cut (nodes in the S part of the cut)
    """
    # get arguments
    G = args[0]
    
    # if a second argument exists set as source
    if len(args) > 1:
        s = args[1]
    elif G.source != []:
        s = G.source
    else:
        s = 1
        
    # check if it a valid Graph
    if not G.is_correct_type('d'):
        print 'ERROR: the graph is not in one of the valid formats for labeling_max_flow()'
        return []
    
    if size(G.u) == 0:
        print 'ERROR: the graph has no capacities or no source/sink is set'
        return []
    
    n = G.nodes()
    
    # check if the source is useful
    list = G.get_out_arcs_pos(s)
    
    # if there are no outgoing arcs, choose one that has
    if size(list) == 0:
        s = 0
        while size(list) == 0 and s < n:
            s += 1
            list = G.get_out_arcs_pos(s)
    
    # if no outgoing arcs where found stop
    if s == n:
        print 'ERROR: the graph has no arcs'
        return []
    
    min_cut_cap = inf           # initialize cut value
    min_flow = empty(0)         # initialize minimum flow
    
    # do the n, max flow problems
    for node in range(n):
        t = node + 1
        # solve a max flow problem for each of the other nodes
        if t != s:
            print "Solving Max Flow Problem from %d to %d" % (s,t)
            # obtain the maximum flow
            G = labeling_max_flow(G, s, t)
            flow = G.f
            # if no error occurs
            if size(flow) != 0:
                # get the flow value
                flow_out = G.total_flow_from(s)
                # if it is smaller, update
                if flow_out < min_cut_cap:
                    min_cut_cap = flow_out
                    min_flow = flow
    
    if size(min_flow) == 0:
        print "ERROR: no cuts were found in the graph"
        return []
    
    # if we had a valid result, get the cut from it
    G.add_flow(min_flow)
    # get the residual graph
    R = G.residual_graph()
    # find the set of reachable nodes in R
    order, p = breath_first(R, s)   # do a search from s to all nodes
    cut = empty(0, int)
    
    # add connected nodes to the cut
    for node in range(n):
        # add the node if it is connected
        if p[node] != inf:
            cut = append(cut, node + 1)
    
    return cut

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
    menu_name = "Min Cut"
    algorithm_list = [["Min Cut from Max Flow", board_min_cut_from_mf],
                      ["separator", "separator"],
                      ["Global Min Cut by n Max Flow", board_global_min_cut]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_global_min_cut(board):
    print "\nMinimum Cut: Global Min Cut from n Maximum Flow Problems"
    # optimize & and add the flow
    ini_time = clock()
    S = global_min_cut(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "nodes in the S part of the cut: ", S
    print "total capacity of cut: ", board.graph.get_cut_capacity(S)
    print "time taken: ", end_time - ini_time
    
    if size(S) != 0:
        board.draw_graph()
        board.draw_cut(S)
    else:
        board.draw_graph()
    print "-----------------------------------------------------------------"

def board_min_cut_from_mf(board):
    print "\nMinimum Cut: Min Cut from Maximum Flow Algorithm"
    # optimize & and add the flow
    ini_time = clock()
    S = min_cut_from_mf(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "nodes in the S part of the cut: ", S
    print "total capacity of cut: ", board.graph.get_cut_capacity(S)
    print "time taken: ", end_time - ini_time
    
    if size(S) != 0:
        board.draw_graph()
        board.draw_cut(S)
    else:
        board.draw_graph()
    print "-----------------------------------------------------------------"