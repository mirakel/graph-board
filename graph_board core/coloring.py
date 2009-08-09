"""
Coloring Algorithms for Graphs v.1.0

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
from numpy.random import *           # random number generation
from time import *                   # timers
# personal modules and classes
from GraphClass import *             # Graph classes

"""
Main Algorithms
"""
def brute_force_coloring(*args):
    """
    exact coloring by using brute force search
    
    @type G: graph
    @param G: graph
    
    @rtype min_coloring: int vector
    @return min_coloring: smallest stable coloring
    
    @rtype chrom_n: int
    @return chrom_n: chromatic number
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    m = G.arcs()
    
    # check if it a valid Graph
    if not G.is_correct_type('u'):
        print "ERROR: the graph is not in one of the valid formats for brute_force_coloring()"
        return [], []
    
    coloring = ones(n, int)         # initialize with just one color
    chrom_n = inf                   # initialize chromatic number
    min_coloring = []               # initialize minimum coloring
    
    # iterate till you get a coloring (really stupid way)
    terminal = array(range(n), int) + 1
    while sum(coloring != terminal) > 0:
        #print coloring
        coloring[n-1] += 1
        # correct if some achieve n
        for node in range(n-1):
            # if one get above n
            if coloring[n-1-node] > max(coloring[0:n-1-node]) + 1:
                coloring[n-1-node] = 1          # take one and...
                coloring[n-2-node] += 1         # ... add it to the previous one
                
        # if it is a coloring check it
        if G.is_coloring(coloring):
            col_number = max(coloring)          # number of colors
            # if it is better, update
            if col_number < chrom_n:
                chrom_n = col_number
                min_coloring = coloring.copy()
                print "current minimum: ", min_coloring, "with %d colors" %(chrom_n)
    
    return min_coloring, chrom_n

def greedy_coloring(*args):
    """
    approximate coloring by using greedy algorithm
    
    @type G: graph
    @param G: graph
    
    @rtype coloring: int vector
    @return coloring: approximate smallest stable coloring
    
    @rtype col_number: int
    @return col_number: approximate chromatic number
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    m = G.arcs()
    
    # check if it a valid Graph
    if not G.is_correct_type('u'):
        print "ERROR: the graph is not in one of the valid formats for greedy_coloring()"
        return [], []
        
    # calculate degrees of each node (set as rows per node)
    a_nodes = zeros((n,n), int)
    for arc in range(m):
        i = G.A[arc,0]              # tail of the arc
        j = G.A[arc,1]              # head of the arc
        a_nodes[i-1,j-1] = 1
        a_nodes[j-1,i-1] = 1
    # get degree and add the node number
    degree = sum(a_nodes,0)
    degree = vstack((degree, array(range(n), int) + 1))
    
    # initialize coloring vector
    coloring = zeros(n, int)
    color_step = 1
    
    # if there are any nodes of degree 0 color them first
    while min(degree[0,:]) == 0:
        n_i = argmin(degree[0,:])   # get node with zero
        i = degree[1,n_i]
        # eliminate the node column from the list and matrix
        degree = delete(degree, s_[n_i], axis=1)
        a_nodes = delete(a_nodes, s_[n_i], axis=1)
        # color it
        coloring[i-1] = color_step
        
    # iterate till all nodes have a color
    while size(degree) > 0:
        n_i = argmax(degree[0,:])   # get node with largest degree
        i = degree[1,n_i]
        # eliminate the node column from the list and matrix
        degree = delete(degree, s_[n_i], axis=1)
        a_nodes = delete(a_nodes, s_[n_i], axis=1)
        
        # color it
        coloring[i-1] = color_step
        
        # color the rest of the possible nodes
        possible = 1 - array(a_nodes[i-1,:])    # transforms 0 in 1, and 1 in 0
        # iterate while there are possible nodes available
        while sum(possible) > 0:
            # get the node with largest degree among possible ones
            n_j = argmax(degree[0,:] * possible)
            j = degree[1,n_j]
            # eliminate the node column from the list and matrix
            degree = delete(degree, s_[n_j], axis=1)
            a_nodes = delete(a_nodes, s_[n_j], axis=1)
            possible = delete(possible, n_j)
            
            # color it
            coloring[j-1] = color_step
            # eliminate adjacent nodes of j from possible nodes
            possible = possible * (1 - a_nodes[j-1,:])
        
        # update color
        color_step += 1
        
    col_number = max(coloring)      # approx chromatic number
    
    return coloring, col_number

def tabu_coloring(*args):
    """
    approximate coloring using tabu search
    
    @type G: graph
    @param G: graph
    
    @rtype best_coloring: int vector
    @return best_coloring: approximate smallest stable coloring
    
    @rtype col_number: int
    @return col_number: approximate chromatic number
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    m = G.arcs()
    
    # check if it a valid Graph
    if not G.is_correct_type('u'):
        print "ERROR: the graph is not in one of the valid formats for tabu_coloring()"
        return [], []
    
    # get a starting point by using the greedy algorithm
    print "First Approximation through Greedy Algorithm"
    best_coloring, best_chrom_number = greedy_coloring(G)
    
    # tabu parameters
    tabu_step_limit = 100
    tabu_b = 9.0
    tabu_alpha = 0.6
    params = [tabu_step_limit, tabu_b, tabu_alpha]  # pack
    
    # apply tabu search lowering the number of colors
    run_condition = 1
    C, k = best_coloring.copy(), best_chrom_number
    while run_condition:
        # look for a solution with a lower chromatic number
        k = k - 1
        # transform the coloring to initial solution
        for node in range(n):
            if C[node] > k:
                C[node] = k
        print "Looking for coloring with %d colors" %(k)
        
        # search for a coloring with k colors
        C = tabu_coloring_search(G, params, C)
        
        # check the resulting coloring
        if G.is_coloring(C):
            # if a coloring was found, save as best solution
            best_coloring = C.copy()
            print "current best is", best_coloring, "with %d colors" %(max(best_coloring))
            #draw_graph(G, best_coloring, "coloring")
        else:
            # otherwise leave
            print "could not find a coloring with %d colors" %(k)
            run_condition = 0
    
    return best_coloring, max(best_coloring)

def tabu_precoloring(*args):
    """
    approximate coloring using tabu search
    
    @type G: graph
    @param G: graph
    
    @rtype best_coloring: int vector
    @return best_coloring: approximate smallest stable coloring
    
    @rtype col_number: int
    @return col_number: approximate chromatic number
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    m = G.arcs()
    
    # check if it a valid Graph
    if not G.is_correct_type('u'):
        print "ERROR: the graph is not in one of the valid formats for tabu_coloring()"
        return [], []
        
    # get a starting point by using the greedy algorithm
    print "First Approximation through Greedy Algorithm"
    best_coloring, best_chrom_number = greedy_coloring(G)
    
    # tabu parameters
    tabu_step_limit = 100
    tabu_b = 9.0
    tabu_alpha = 0.6
    params = [tabu_step_limit, tabu_b, tabu_alpha]  # pack
    
    # apply tabu search lowering the number of colors
    run_condition = 1
    C, k = best_coloring.copy(), best_chrom_number
    while run_condition:
        # look for a solution with a lower chromatic number
        k = k - 1
        # transform the coloring to initial pre-coloring
        for node in range(n):
            if C[node] > k:
                C[node] = 0
        print "Looking for coloring with %d colors" %(k)
        
        # search for a coloring with k colors
        C = tabu_precoloring_search(G, params, C)
        
        # check the resulting coloring
        if G.is_coloring(C) and min(C) != 0:
            # if a coloring was found, save as best solution
            best_coloring = C.copy()
            print "current best is", best_coloring, "with %d colors" %(max(best_coloring))
            #draw_graph(G, best_coloring, "coloring")
        else:
            # otherwise leave
            print "could not find a coloring with %d colors" %(k)
            run_condition = 0
    
    return best_coloring, max(best_coloring)

"""
Auxiliary Functions
"""
def tabu_coloring_search(*args):
    """
    tabu search algorithm to find a coloring
    
    @type G: graph
    @param G: graph
    
    @type params: vector
    @param params: tabu search parameters [tabu_step_limit, tabu_b, tabu_alpha]
    
    @type C or k: int vector or int
    @param C or k: coloring starting point or number of colors to search
    
    @rtype: int vector
    @return: coloring
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    
    # load tabu parameters
    params = args[1]                # tabu parameters
    tabu_step_limit = params[0]
    tabu_b = params[1]
    tabu_alpha = params[2]
    
    # get coloring or required number of colors
    C = args[2]                     # initial coloring vector
    if size(C) == 1:
        # if it was k, create a dummy coloring
        C = C * ones(n)
    k = max(C)                      # number of colors to look for
    # list of all possible colors
    possible_colors = array(range(k)) + 1
    
    # tabu search for getting the coloring
    v_list = get_violating_nodes(G, C)
    tabu_tenure = zeros((k,n), float)   # k colors and n nodes
    step = 0                            # iteration indicator
    # try to reduce the number of violating nodes
    tabu_search = 1
    while tabu_search:
        curr_best = sum(v_list)         # current number of violating nodes
        best_color = 0
        num_equal_solutions = 1         # to break ties among equal solutions
        
        # look for the best neighbor
        for node in range(n):
            node_color = C[node]          # color of the node
            # check all other colors
            for color in possible_colors:
                # check the new color if it is different
                if color != node_color:
                    # apply color
                    C[node] = color
                    # list of nodes
                    tmp_list = get_violating_nodes(G, C)
                    
                    # if it is a non-tabu solution with equal number of nodes update
                    if sum(tmp_list) == curr_best and tabu_tenure[color-1,node] <= 0:
                        # break ties using a uniform distribution
                        prob = uniform(0,1)
                        if prob > num_equal_solutions / (num_equal_solutions + 1):
                            # update current best
                            curr_best = sum(tmp_list)
                            best_node = node
                            best_color = color
                        
                        # indicate that a new equal solution was found
                        num_equal_solutions += 1
                    # if it is better (tabu or not)
                    elif sum(tmp_list) < curr_best:
                        # update current best
                        curr_best = sum(tmp_list)
                        best_node = node
                        best_color = color
                        # start counting again
                        step = 0
                        # restart the equality counter
                        num_equal_solutions = 1
                    
            # return original color before testing next node
            C[node] = node_color
        
        # update tabu_tenure matrix
        tabu_tenure -= 1
        # update the current solution and tenure if a better/equal one was found
        if best_color != 0:
            C[best_node] = best_color
            tabu_tenure[best_color - 1, best_node] = uniform(0,tabu_b) + tabu_alpha * sum(v_list)
               
        # check if it has to stop
        v_list = get_violating_nodes(G, C)
        step += 1
        if sum(v_list) == 0 or step > tabu_step_limit or best_color == 0:
            tabu_search = 0
    
    return C

def tabu_precoloring_search(*args):
    """
    tabu search algorithm to find a coloring
    
    @type G: graph
    @param G: graph
    
    @type params: vector
    @param params: tabu search parameters [tabu_step_limit, tabu_b, tabu_alpha]
    
    @type C: int vector
    @param C: coloring starting point
    
    @rtype: int vector
    @return: coloring
    """
    # get arguments
    G = args[0]
    n = G.nodes()
    
    # get full adjacency matrix for speeding the process
    adj_matrix = G.build_adjacency_lists()
    
    # load tabu parameters
    params = args[1]                # tabu parameters
    tabu_step_limit = params[0]
    tabu_b = params[1]
    tabu_alpha = params[2]
    
    # get coloring or required number of colors
    C = args[2]                     # initial pre-coloring vector
    k = max(C)                      # number of colors to look for
    # list of all possible colors
    possible_colors = array(range(k)) + 1
    
    # tabu search for getting the coloring
    tabu_tenure = zeros((k,n), float)   # k colors and n nodes
    step = 0                            # iteration indicator
    # try to reduce the number of violating nodes
    tabu_search = 1
    while tabu_search:
        curr_best = sum(C == 0)         # current number of nodes without color
        best_color = 0
        num_equal_solutions = 1         # to break ties among equal solutions
        #print "colors: ", C
        # look for the best neighbor by testing all colors on non-colored nodes
        for node in range(n):
            # if belongs to O, check all colors
            if C[node] == 0:
                # get list of adjacent nodes
                adjacent_list = adj_matrix[node]
                # get respective colors
                color_list = C[adjacent_list - 1]
                #print "node: ", node + 1
                #print "list: ", adjacent_list, "colors: ", color_list
                # check with color has less nodes 
                for color in possible_colors:
                    # get the size of O given this possible change
                    size_O = sum(C == 0) - 1 + sum(color_list == color)
                    #print "color: ", color, "size of O:", size_O
                    # if the current color generates and equal solution update
                    if size_O == curr_best and tabu_tenure[color-1,node] <= 0:
                        # break ties using a uniform distribution
                        prob = uniform(0,1)
                        if prob > num_equal_solutions / (num_equal_solutions + 1):
                            # update current best
                            curr_best = size_O
                            best_node = node
                            best_color = color
                            
                        # indicate that a new equal solution was found
                        num_equal_solutions += 1
                    # if it is better (tabu or not)
                    elif size_O < curr_best:
                        # update current best
                        curr_best = size_O
                        best_node = node
                        best_color = color
                        # start counting again
                        step = 0
                        # restart the equality counter
                        num_equal_solutions = 1
        
        #print "best node: ", best_node + 1, "best color: ", best_color
        # update tabu_tenure matrix
        tabu_tenure -= 1
        # update the current solution and tenure if a better/equal one was found
        if best_color != 0:
            # add color to best node
            C[best_node] = best_color
            # get adjacent nodes
            adjacent_list = adjacent_list = adj_matrix[best_node]
            # put in O all nodes in the list with best_color, and tabu them
            for j in adjacent_list:
                if C[j-1] == best_color:
                    C[j-1] = 0
                    tabu_tenure[best_color - 1, j - 1] = uniform(0,tabu_b) + tabu_alpha * sum(C == 0)
               
        # check if it has to stop
        step += 1
        if sum(C == 0) == 0 or step > tabu_step_limit or best_color == 0:
            tabu_search = 0
    
    return C

def get_violating_nodes(G, C):
    """
    get a list of nodes that are not stable in the coloring
    
    @type G: graph
    @param G: graph
    
    @type C: int vector
    @param C: coloring to test
    
    @rtype: list
    @return: list of nodes that are not stable
    """
    C = array(C, int)
    # get graph parameters
    n = G.nodes()
    m = G.arcs()
    
    v_list = zeros(n)
    
    for arc in range(m):
        i = G.A[arc,0]        # arc end-points
        j = G.A[arc,1]
        
        # if head and tail have the same color, add vertex
        if C[i-1] == C[j-1] and C[i-1] != 0 and C[j-1] != 0:
            v_list[i-1] = 1
            v_list[j-1] = 1
        
    return v_list

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
    menu_name = "Coloring"
    algorithm_list = [["Brute Force", board_brute_force_coloring],
                      ["separator", "separator"],
                      ["Greedy Coloring", board_greedy_coloring],
                      ["Tabu Coloring Search", board_tabu_coloring],
                      ["Tabu Pre-Coloring Search", board_tabu_precoloring]]
    
    return [menu_name, algorithm_list]

"""
Functions Mapping Algorithms for the Board
"""
def board_tabu_precoloring(board):
    print "\nColoring: Tabu Search Algorithm (approximate)\n"
    # get the coloring
    ini_time = clock()
    coloring, col_number = tabu_precoloring(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "coloring: ", coloring
    print "number of colors required: ", col_number
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if coloring != []:
        board.draw_coloring(coloring)
    print "-----------------------------------------------------------------"
    
def board_tabu_coloring(board):
    print "\nColoring: Tabu Search Algorithm (approximate)\n"
    # get the coloring
    ini_time = clock()
    coloring, col_number = tabu_coloring(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "coloring: ", coloring
    print "number of colors required: ", col_number
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if coloring != []:
        board.draw_coloring(coloring)
    print "-----------------------------------------------------------------"
    
def board_brute_force_coloring(board):
    print "\nColoring: Brute Force Algorithm\n"
    # get the coloring
    ini_time = clock()
    min_coloring, chrom_n = brute_force_coloring(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "coloring: ", min_coloring
    print "number of colors required: ", chrom_n
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if min_coloring != []:
        board.draw_coloring(min_coloring)
    print "-----------------------------------------------------------------"
    
def board_greedy_coloring(board):
    print "\nColoring: Greedy Algorithm (approximate)\n"
    # get the coloring
    ini_time = clock()
    coloring, col_number = greedy_coloring(board.graph)
    end_time = clock()
    
    print "\nResults:"
    print "coloring: ", coloring
    print "number of colors required: ", col_number
    print "time taken: ", end_time - ini_time
    
    board.draw_graph()
    if coloring != []:
        board.draw_coloring(coloring)
    print "-----------------------------------------------------------------"