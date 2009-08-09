"""
Min Cost FLow Algorithms for Graphs v.1.0

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
from shortest_path import *          # shortest path algorithms
from max_flow import *               # max flow algorithms (for the auxiliary functions)
from graph_board import *

"""
Main Algorithms
"""
def cycle_cancel_mcf(*args):
    """
    calculate the minimum cost flow using a negative cycle canceling algorithm
    
    @type G: graph
    @param G: graph
    
    @rtype: graph
    @return: graph with optimal flow
    """
    # get arguments
    G = args[0]                     # graph
        
    # check if it a valid Graph
    if not G.is_correct_type('d'):
        print "ERROR: the graph is not in one of the valid formats for labeling_max_flow()"
        G.f = empty(0)
        return G
    
    if size(G.u) == 0 or size(G.c) == 0:
        print "ERROR: the graph has no capacities or costs set"
        G.f = empty(0)
        return G
    
    if sum(G.B) != 0:
        print "ERROR: The problem is infeasible, sum of external flows is not 0"
        G.f = empty(0)
        return G
    
    n = G.nodes()
    m = G.arcs()
    
    print "Finding feasible flow"
    # put a feasible flow if sources exist
    if max(G.B) > 0:
        # find a feasible flow
        G = feasible_flow(G)
        # delete extra nodes added
        G.del_node(n+2)
        G.del_node(n+1)
        G.source = []
        G.sink = []
    else:
        G = G.add_flow(zeros(m))
        
    if size(G.f) == 0:
        print "ERROR: the problem is not feasible"
        return G
    
    print "\nSolving Min Cost Flow"
    # obtain residual graph
    R = G.residual_graph()
    
    R.source = argmax(R.B) + 1
    
    # detect a negative cost cycle
    p, d, nc_flag, nc_path = shortest_path_fifo(R, R.source)
    
    # create a file to store the steps
    draw_graph(G, ["style", "write", "cycle_cancel.ps"])
    
    draw_graph(R, ["style", "append", "cycle_cancel.ps"])
    
    # keep on augmenting while a negative cost cycle exists
    while nc_flag:
        # get maximum capacity of the negative cost cycle
        delta = path_max_capacity(R, nc_path)
        print "negative cycle: ", nc_path
        print "delta: ", delta
        print "cost improvement: ", R.total_path_cost(nc_path)
        
        # augment the flow
        R = augment_path(R, nc_path, delta)
        
        # create a file to store the steps
        draw_graph(R, ["style", "append", "cycle_cancel.ps"], ["path", nc_path])
    
        # detect a negative cost cycle
        p, d, nc_flag, nc_path = shortest_path_fifo(R, R.source)
    
    # get the flow from the residual graph
    R.source = []
    R.sink = []
    Gf = R.graph_from_residual()
    
    draw_graph(Gf, ["style", "append", "cycle_cancel.ps"], ["saturation", []])
    
    return Gf

def shortest_path_mcf(*args):
    """
    calculate the minimum cost flow using a successive shortest path algorithm
    
    @type G: graph
    @param G: graph
    
    @rtype: graph
    @return: graph with optimal flow
    """
    # get arguments
    G = args[0]                     # graph
        
    # check if it a valid Graph
    if not G.is_correct_type('d'):
        print "ERROR: the graph is not in one of the valid formats for labeling_max_flow()"
        G.f = empty(0)
        return G
    
    if size(G.u) == 0 or size(G.c) == 0:
        print "ERROR: the graph has no capacities or costs set"
        G.f = empty(0)
        return G
    
    if sum(G.B) != 0:
        print "ERROR: The problem is infeasible, sum of external flows is not 0"
        G.f = empty(0)
        return G
    
    n = G.nodes()
    m = G.arcs()
    
    # set flow to zero
    G = G.add_flow(zeros(m))
    
    # create a file to store the steps
    draw_graph(G, ["style", "write", "shortest_path.ps"])
    
    print "\nSolving Min Cost Flow"
    # obtain residual graph
    R = G.residual_graph()
    m = 2 * m                       # R has double the arcs
    orig_cost = R.c.copy()          # store original costs
    draw_graph(R, ["style", "append", "shortest_path.ps"])
    
    # initialize variables and sets
    excess = R.B.copy()             # excess vector (not to use B)
    potential = zeros(n)            # potential labels for each node
    red_cost = zeros(m)             # reduced cost for each arc
    
    E = array(excess > 0, int)      # excess node set
    D = array(excess < 0, int)      # deficit node set
    
    while sum(E) > 0:
        # get the largest excess / deficit
        k = argmax(E * excess) + 1
        l = argmin(D * excess) + 1
        print "\nsending flow from %d to %d" %(k, l)
        
        R = R.add_cost(red_cost)
        # get the shortest path from k using reduced costs
        p, d, nc_flag, nc_path = shortest_path_fifo(R, k)
        if nc_flag:
            print "negative cycle: ", nc_path
            path = nc_path
            print "cost change in path: ", R.total_path_cost(path)
        else:
            # get an augmenting path
            path = get_rooted_path(p, l)
            print "path: ", path
            #print "distances: ", d
        
        # update potential vector and reduced costs
        R = R.add_cost(orig_cost)
        potential -= array(d, int)  # potential update
        for arc in range(m):        # reduced costs update
            i = R.A[arc,0]          # arc end-points
            j = R.A[arc,1]
            red_cost[arc] = R.c[arc] - potential[i-1] + potential[j-1]
        
        # get maximum flow to push
        delta = path_max_capacity(R, path)
        delta = min(delta, excess[k-1], -excess[l-1])
        print "delta: ", delta
        # augment the flow
        R = augment_path(R, path, delta)
        
        # create a file to store the steps
        draw_graph(R, ["style", "append", "shortest_path.ps"], ["path", path])
        
        # update excess on each node if it was not a negative cycle
        if not nc_flag:
            excess[k-1] -= delta
            excess[l-1] += delta
        
        # update sets
        E = array(excess > 0, int)      # excess node set
        D = array(excess < 0, int)      # deficit node set
    
    # get the flow from the residual graph
    Gf = R.graph_from_residual()
    
    draw_graph(Gf, ["style", "append", "shortest_path.ps"], ["saturation", []])
    
    return Gf

"""
Auxiliary Functions
"""
def feasible_flow(G):
    """
    find a feasible flow for G using a max flow algorithm
    
    @attention: this function adds two nodes n+1 and n+2 to the graph
                as global source and sink
                
    @type G: graph
    @param G: graph
    
    @rtype: graph
    @return: graph with a feasible flow
    """
    n = G.nodes()
    m = G.arcs()
    
    # duplicate G to avoid changes in G
    H = G.copy()
    
    # create a virtual source and sink
    H.add_node()                    # add a source node in n+1
    s = n + 1
    H.coord[s-1,:] = array([40, 560])
    H.add_node()                    # add a sink node in n+2
    t = n + 2
    H.source = s
    H.sink = t
    H.coord[t-1,:] = array([40, 40])
    
    # add arcs: from s (n+1) to each B>0 and from B<0 to t (n+2)
    for node in range(n):
        b = H.B[node]               # external flow
        # if it is a source node
        if b > 0:
            H.add_arc(s, node+1)
            arc = H.get_arc_pos(s, node+1)
            H.u[arc] = b
        # if it is a sink node
        elif b < 0:
            H.add_arc(node+1, t)
            arc = H.get_arc_pos(node+1, t)
            H.u[arc] = -b
            
    # solve a max flow problem from s to t
    H = labeling_max_flow(H, s, t)
    flow = H.f
    
    # check if a flow exists
    if size(flow) == 0:
        print "ERROR: there is no feasible flow"
        H.f = flow
        return H
    
    # check if s - graph and graph - t arcs are saturated
    for node in range(n):
        b = H.B[node]               # external flow
        # if it is a source/sink node
        # if it is a source node
        if b > 0:
            arc = H.get_arc_pos(s, node + 1)
            if H.f[arc] != H.u[arc]:
                H.f = empty(0)
                return H
        
        # if it is a sink node
        elif b < 0:
            arc = H.get_arc_pos(node + 1, t)
            if H.f[arc] != H.u[arc]:
                H.f = empty(0)
                return H
    
    return H

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
    menu_name = "Min Cost Flow"
    algorithm_list = [["Negative Cycle Canceling", board_cycle_cancel_mcf],
                      ["Successive Shortest Paths", board_shortest_path_mcf]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_shortest_path_mcf(board):
    print "\nMin Cost Flow: Negative Cycle Canceling Algorithm"
    ini_time = clock()
    board.graph = shortest_path_mcf(board.graph)
    end_time = clock()
    flow = board.graph.f
    
    print "\nResults:"
    print "flow per arc: ", flow
    print "time taken: ", end_time - ini_time
    
    if size(flow) != 0:
        print "total flow cost: ", board.graph.total_flow_cost()
        board.draw_graph()
        board.draw_arc_saturation()
    else:
        print "total flow from s: 0"
        board.draw_graph()
    print "-----------------------------------------------------------------"
    
def board_cycle_cancel_mcf(board):
    print "\nMin Cost Flow: Negative Cycle Canceling Algorithm"
    ini_time = clock()
    board.graph = cycle_cancel_mcf(board.graph)
    end_time = clock()
    flow = board.graph.f
    
    print "\nResults:"
    print "flow per arc: ", flow
    print "time taken: ", end_time - ini_time
    
    if size(flow) != 0:
        print "total flow cost: ", board.graph.total_flow_cost()
        board.draw_graph()
        board.draw_arc_saturation()
    else:
        print "total flow from s: 0"
        board.draw_graph()
    print "-----------------------------------------------------------------"