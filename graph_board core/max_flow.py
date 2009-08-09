"""
Max Flow Algorithms for Graphs v.1.0

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
from shortest_path import *          # shortest path algorithms

"""
Main Algorithms
"""
def generic_augmenting_path(*args):
    """
    max flow calculation using a generic augmenting path algorithm
    
    @type G: graph
    @param G: graph
    
    @note: optional parameters
    @type s: int
    @param s: source node
    
    @type t: int
    @param t: sink node
    
    @rtype: graph
    @return: graph with the optimal flow
    """
    # get arguments
    G = args[0]                     # graph
    
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
        G.f = empty(0)
        return G
    
    if size(G.u) == 0 or s == [] or t == []:
        print 'ERROR: the graph has no capacities or no source/sink is set'
        G.f = empty(0)
        return G
    
    n = G.nodes()
    m = G.arcs()
    # check if t is reachable from s
    if G.reach_from(s)[t-1] != 1:
        print 'ERROR: the sink %d, is not reachable from the source %d' %(t, s)
        G.f = empty(0)
        return G
    
    # set flow to zero
    G = G.add_flow(zeros(m))
    # obtain residual graph
    R = G.residual_graph()
    
    # augment while an augmenting path exists
    order, p = breath_first(R, s)   # do a search from s to all nodes
    t_reach = p[t-1]
    while t_reach != inf:
        # get an augmenting path
        path = get_rooted_path(p, t)
        # get maximum capacity
        delta = path_max_capacity(R, path)
        print "path: ", path
        print "delta: ", delta
        # augment the flow
        R = augment_path(R, path, delta)
        # do a new search on the modified graph
        order, p = breath_first(R, s)
        t_reach = p[t-1]
    
    # get the flow from the residual graph
    Gf = R.graph_from_residual()
    
    return Gf

def labeling_max_flow(*args):
    """
    max flow calculation using a labeling algorithm
    
    @type G: graph
    @param G: graph
    
    @note: optional parameters
    @type s: int
    @param s: source node
    
    @type t: int
    @param t: sink node
    
    @rtype: graph
    @return: graph with the optimal flow
    """
    # get arguments
    G = args[0]                     # graph
    
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
        G.f = empty(0)
        return G
    
    if size(G.u) == 0 or s == [] or t == []:
        print 'ERROR: the graph has no capacities or no source/sink is set'
        G.f = empty(0)
        return G
    
    n = G.nodes()
    m = G.arcs()
    # check if t is reachable from s
    if G.reach_from(s)[t-1] != 1:
        print 'ERROR: the sink %d, is not reachable from the source %d' %(t, s)
        G.f = empty(0)
        return G
    
    # set flow to zero
    G = G.add_flow(zeros(m))
    # obtain residual graph
    R = G.residual_graph()
    
    label = zeros(n)            # label vector
    label[t-1] = 1              # label t
    
    # augment while t is labeled
    while label[t-1] == 1:
        # un-label all nodes
        label = zeros(n)            # label vector
        pred = zeros(n)             # predecessor list
        
        # label s and add to list
        label[s-1] = 1
        list = array([s])
        # start augmenting
        while size(list) != 0 and label[t-1] == 0:
            i = list[0]             # get a node from the list
            list = delete(list, 0)  # eliminate the node
            
            # add all arcs from i to the list
            pos = R.N[i-1,0]        # initial position of data for node i
            # allow for iterations only if node information exists
            if pos == -1:
                link = 0
            else:
                link = 1
            # label adjacent nodes to i
            while link != 0:
                # add the nodes that have not been used
                j = R.A[pos,1]      # head of the arc
                # check if the arc is admissible and has capacity
                if label[j-1] == 0 and R.u[pos] > 0:
                    list = append(list, j)  # add j to the list
                    label[j-1] = 1          # and label it
                    pred[j-1] = i           # predecessor
                pos = int(R.A[pos,2])       # check next node
                link = pos
            
        # if t was labeled, augment
        if label[t-1] == 1:
            # get the path from the predecessor list
            path = get_rooted_path(pred, t)
            # get maximum capacity
            delta = path_max_capacity(R, path)
            print "path: ", path
            print "delta: ", delta
            # augment the flow
            R = augment_path(R, path, delta)
    
    # get the flow from the residual graph
    Gf = R.graph_from_residual()
    
    return Gf

def cheapest_bottleneck(*args):
    """
    algorithm for detecting the cheapest bottleneck
    
    @type G: graph
    @param G: graph
    
    @note: optional parameters
    @type s: int
    @param s: source node
    
    @type t: int
    @param t: sink node
    
    @rtype: int vector
    @return: path of the cheapest bottleneck
    """
    # get arguments
    G = args[0]                     # graph
    
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
        print 'ERROR: the graph is not in one of the valid formats for cheapest_bottleneck()'
        return []
    
    if size(G.u) == 0 or s == [] or t == []:
        print 'ERROR: the graph has no capacities or no source/sink is set'
        return []
    
    if size(G.c) == 0:
        print 'ERROR: the arcs have no associated costs, no calculation can be made'
        return []
    
    # optimize & and add the flow
    print "Solving Max Flow Problem"
    G = labeling_max_flow(G)
    flow = G.f
    
    if size(flow) == 0:
        print "Max Flow problem was not solvable"
        return []
    
    # copy the graph and change costs
    H = G.copy()
    m = H.arcs()
    
    for arc in range(m):
        # if the arc is not saturated, set cost as 0
        if H.f[arc] < H.u[arc]:
            H.c[arc] = 0
    
    print "Solving Cheapest Path Problem"
    # solve the shortest path over this new graph
    p, d, nc_flag, nc_path = shortest_path_fifo(H, s)
    
    # get the path from the predecessor list
    path = get_rooted_path(p, t)
    
    return path
    
"""
Auxiliary Functions
"""
def get_rooted_path(p, t):
    """
    get the path from the root to a node t, using the predecessor vector
    
    @type p: int vector
    @param p: predecessor array
    
    @type t: int
    @param t: destination node to build path root -> t
    
    @rtype: int vector
    @return: path to go from root to t
    """
    # initialize path array
    path = array([t], int)
    node = t                        # last node
    
    # built the path to the root
    while p[node-1] != 0:
        node = p[node-1]
        path = insert(path, 0, node)
    
    return path

def path_max_capacity(R, path):
    """
    get the maximum capacity of a path in the graph
    
    @type R: graph
    @param R: residual graph
    
    @type path: int vector
    @param path: path to test
    
    @rtype: float/int
    @return: maximum flow that can be pushed in the path
    """
    # initialize delta
    delta = inf
    steps = size(path) - 1          # number of arcs in the path
    
    for node in range(steps):
        # path arc
        i = path[node]
        j = path[node + 1]
        # get arc information
        data = R.get_arc_data(i,j)
        # @todo: add protection if arc does not exist
        u = data[4]
        # update max cap
        if u < delta:
            delta = u
            
    return delta

def augment_path(R, path, flow):
    """
    augment an amount flow through a path in R
    
    @type R: graph
    @param R: residual graph
    
    @type path: int vector
    @param path: path where to push the flow
    
    @type flow: number
    @param flow: flow to push
    
    @rtype: graph
    @return: graph with flow pushed
    """
    # check if it a valid Graph
    if not R.is_correct_type('dr'):
        print 'ERROR: the graph is not in one of the valid formats for augment_path()'
        return R
    
    steps = size(path) - 1          # number of arcs in the path
    for node in range(steps):
        # path arc
        i = path[node]
        j = path[node + 1]
        arc = R.get_arc_pos(i, j)
        
        # augment the flow in the arc
        if R.type == "d":
            # if it is a directed graph, just increase f
            R.f[arc] = R.f[arc] + flow
            
        elif R.type == "r":
            # if it is a residual graph, reduce capacity of arc, and increase of reverse
            R.u[arc] = R.u[arc] - flow
            link = R.mirror[arc]    # back arc
            R.u[link] = R.u[link] + flow
            #print "pushed ", flow, "through arc (%d,%d)" %(R.A[arc,0], R.A[arc,1])
            #print "and pushed back through arc (%d,%d)" %(R.A[link,0], R.A[link,1])
    
    return R

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
    menu_name = "Max Flow"
    algorithm_list = [["Generic Augmenting Path", board_generic_augmenting_path],
                      ["Generic Labeling", board_labeling_max_flow],
                      ["separator", "separator"],
                      ["Cheapest Bottleneck", board_cheapest_bottleneck]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_cheapest_bottleneck(board):
    print "\nMax Flow: Cheapest Bottleneck Calculation"
    path = cheapest_bottleneck(board.graph)
    
    print "\nResults:"
    print "path: ", path
    
    if path != []:
        board.draw_graph()
        board.draw_path(path)
        #print "Total Cost: ", board.graph.total_tree_cost(p)
    print "-----------------------------------------------------------------"
    
def board_labeling_max_flow(board):
    print "\nMax Flow: Generic Labeling Algorithm"
    # optimize & and add the flow
    ini_time = clock()
    board.graph = labeling_max_flow(board.graph)
    end_time = clock()
    flow = board.graph.f
    
    print "\nResults:"
    print "flow per arc: ", flow
    print "time taken: ", end_time - ini_time
    
    if size(flow) != 0:
        print "total flow from s: ", board.graph.total_flow_from(board.graph.source)
        board.draw_graph()
        board.draw_arc_saturation()
    else:
        print "total flow from s: 0"
        board.draw_graph()
    print "-----------------------------------------------------------------"

def board_generic_augmenting_path(board):
    print "\nMax Flow: Generic Augmenting Path Algorithm"
    # optimize & and add the flow
    ini_time = clock()
    board.graph = generic_augmenting_path(board.graph)
    end_time = clock()
    flow = board.graph.f
    
    print "\nResults:"
    print "flow per arc: ", flow
    print "time taken: ", end_time - ini_time
    
    if size(flow) != 0:
        print "total flow from s: ", board.graph.total_flow_from(board.graph.source)
        board.draw_graph()
        board.draw_arc_saturation()
    else:
        print "total flow from s: 0"
        board.draw_graph()
    print "-----------------------------------------------------------------"