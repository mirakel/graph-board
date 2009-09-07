"""
Graph Class v.1.01

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
# general modules used
from numpy import *                 # matrix manipulation
from numpy.random import *          # matrix manipulation
from string import *                # string management
from random import *                # random number generator
# personal modules
from search_order import *          # searching algorithms

"""
graph class
"""
class Graph(object):
    """
    graph class structure:
    
    type         : graph type check ".set_type()" for graph types
    
    N[i-1,:]     : start & end positions in A[] for information of node i
    A[arc,:]     : adjacency matrix [i j link]
    B[i-1]       : external flow/node label of node i
    names[i-1]   : name of node i
    
    c[pos]       : cost of arc in pos
    u[pos]       : capacity/residual capacity of arc in pos
    f[pos]       : flow in arc pos
    
    coord[i-1,:] : coordinates (x,y) of node i for drawing
    
    source       : source node
    sink         : sink node
    mirror[arc]  : used for residual graphs, link to the mirror arc
    """
    
    def __init__(self):
        """
        graph initialization
        """
        self.type = 'x'             # set as none
        
        self.N = empty((0,2), int)  # initial and end points of node data
        self.A = empty((0,3), int)  # adjacency matrix
        self.B = empty(0)           # external flow for each node
        self.names = []             # names of nodes
        
        self.c = empty(0)           # costs of arcs
        self.u = empty(0)           # capacity of arcs
        self.f = empty(0)           # flow for each arc
        
        self.coord = empty((0,2), float)    # coordinate system
        
        self.source = []            # source node(s)
        self.sink = []              # sink node(s)
        self.mirror = empty(0, int) # mirror of arc, used for residual graphs
        
    def __str__(self):
        """
        str for Graph() object
        
        @rtype: string
        @return: graph information
        """
        # graph information
        
        n = len(self)
        m = shape(self.A)[0]
        if m == 1 and size(self.A) == 0:
            # correct if no columns exist
            m = 0
            
        c = size(self.c) > 0
        u = size(self.u) > 0
        f = size(self.f) > 0
        
        return "<graph object - %d nodes, %d arcs - c: %s, u: %s, f: %s>" %(n,m,c,u,f)
    
    def __len__(self):
        """
        len for Graph() object
        
        @rtype: numbers
        @return: number of nodes
        """ 
        return self.nodes()
        
    """
    Basic Graph Parameters
    """
    def nodes(self):
        """
        number of nodes in the graph
        
        @rtype: number (int)
        @return: number of nodes
        """
        # get graph parameters
        n = shape(self.N)[0]
        
        if n == 1 and size(self.N) == 0:
            # correct if no columns exist
            n = 0
            
        return n
    
    def arcs(self):
        """
        number of arcs in the graph
        
        @rtype: number (int)
        @return: number of nodes
        """
        # get graph parameters
        m = shape(self.A)[0]
        
        if m == 1 and size(self.A) == 0:
            # correct if no columns exist
            m = 0
            
        return m
    
    """
    Forming Functions
    """
    def random_graph(self, g_size, g_type):
        """
        build a random graph (without costs, capacities, etc.)
        
        @type g_size: vector with 2 numbers 
        @param g_size: size of the graph [n = nodes, m = edges]
        
        @type g_type: list []
        @param g_type: type of graph - "directed", "undirected"
        
        @rtype: graph
        @return: random generated graph
        """
        self.__init__()             # clean the graph
        
        # get graph size
        n = g_size[0]
        m = g_size[1]
        
        # graph type
        if g_type[0] == "directed":
            self.type = "d"
        elif g_type[0] == "undirected":
            self.type = "u"
        
        # add the required number of nodes
        for node in range(n):
            self.add_node()
        
        # generate all the arc combinations
        list = zeros((n * (n - 1), 2), int)
        pos = 0
        for i in range(n):
            for j in range(n):
                if i != j:
                     list[pos, :] = array([i + 1, j + 1])
                     pos += 1
                     
        # randomly select m positions and add them as arcs
        for arc in range(m):
            pos = random_integers(0, shape(list)[0] - 1)
            i, j = list[pos, 0], list[pos, 1]
            self.add_arc(i, j)
            
            # delete arc and back arc
            list = delete(list, s_[pos], axis=0)        # eliminate arc
            pos = 0
            while list[pos,0] != j or list[pos,1] != i:
                pos += 1
            list = delete(list, s_[pos], axis=0)        # eliminate back arc
        
        return self
    
    def random_graph_full(self, g_size, g_type, g_param):
        """
        build a random graph
        
        @type g_size: vector with 2 numbers 
        @param g_size: size of the graph [n = nodes, m = edges]
        
        @type g_type: list []
        @param g_type: type of graph - "directed", "undirected"
                       parameter type: "int", "float"
        
        @type g_param: vector with 2 numbers
        @param g_param: arc parameters [C = maximum cost, U = maximum capacity]
        
        @rtype: graph
        @return: random generated graph
        """
        self.__init__()             # clean the graph
        
        # build a random graph
        self = self.random_graph(g_size, g_type)
        
        param_type = g_type[1]
        
        # parameter values
        C = g_param[0]
        U = g_param[1]
        
        # add costs and capacities if they exist
        if C > 0:
            self = self.add_random_cost([-C, C], param_type)
            
        if U > 0:
            self = self.add_random_capacity(U, param_type)
        
        return self
    
    def form_graph(self, N, A, type):
        """
        build a graph using the N (position) and A (adjacency) matrices
        and its type
        
        @type N: int matrix
        @param N: node out-arcs position matrix
        
        @type A: int matrix
        @param A: adjacency matrix
        
        @type type: character
        @param type: graph type
        
        @rtype: graph
        @return: graph formed with N, A, and type      
        """
        self.__init__()                                 # clean the graph
        
        # check that nodes in A and in N match
        n = shape(N)[0]                                 # largest node number in N
        n_A = max([max(A[:,0]), max(A[:,1])])           # largest node number in A
        
        # if there is an arc with head/tail out of the range of N stop
        if n_A > n:
            print 'ERROR: nodes in A are outside the range of N'
            return self
        # check if A and N have the correct size
        if N.shape[1] != 2 or A.shape[1] != 3:
            print 'ERROR: the size of A or N is incorrect'
            return self
        
        # add N, A, and type to G
        self.N = matrix(N, int)
        self.A = matrix(A, int)
        self.type = type
        
        return self
       
    """
    Adding Functions
    """
    def add_random_cost(self, C, type):
        """
        add a set of random costs to each arc
        
        @type C: list
        @param C: [c_min c_max] vector with cost limits
        
        @type type: string
        @param type: type of variable: "int", "float"
        
        @rtype: graph
        @return: graph with random costs
        """
        m = self.arcs()             # number of arcs
        
        # add random costs
        self = self.add_cost(array( (C[1] - C[0]) * random_sample(m) + C[0], type))
        
        return self
        
    def add_random_capacity(self, U, type):
        """
        add a set of random capacities to each arc
        
        @type U: number
        @param U: maximum capacity
        
        @type type: string
        @param type: type of variable: "int", "float"
        
        @rtype: graph
        @return: graph with random capacities
        """
        m = self.arcs()             # number of arcs
        
        # add random capacities
        self = self.add_capacity(array(U * random_sample(m), type))
        
        return self
    
    def add_cost(self, c):
        """
        add a cost to each arc
        
        @type c: number vector
        @param c: cost of each arc
        
        @rtype: graph
        @return: graph with costs
        """
        m = self.arcs()             # number of arcs
        
        # check if the size of the cost vector is equal to m
        if size(c) != m:
            print 'ERROR: size of A and c do not match'
            return self
        
        # add the cost vector 
        self.c = c
        
        return self
        
    def add_capacity(self, u):
        """
        add a capacity to each arc
        
        @type u: number vector
        @param u: capacity of each arc
        
        @rtype: graph
        @return: graph with capacities
        """
        m = self.arcs()             # number of arcs
        
        # check if the size of the capacity vector is equal to m
        if size(u) != m:
            print 'ERROR: size of A and u do not match'
            return self
        
        # add the capacity vector 
        self.u = u
        
        return self
    
    def add_external_flow(self, B):
        """
        add an external flow value to each node
        
        @type B: number vector
        @param B: external flow for each node (<0 for sink nodes)
        
        @rtype: graph
        @return: graph with external flow
        """
        n = self.nodes()            # number of nodes
        
        # check if the size of the flow vector is equal to n
        if size(B) != n:
            print 'ERROR: size of N and B do not match'
            return self
        
        # add the flow vector 
        self.B = B
        
        return self
    
    def add_flow(self, f):
        """
        add a flow value to each arc
        
        @type f: number vector
        @param f: flow for each arc
        
        @rtype: graph
        @return: graph with flow
        """
        m = self.arcs()             # number of arcs
        
        # check if the size of the flow vector is equal to m
        if size(f) != m:
            print 'ERROR: size of A and f do not match'
            return self
        
        # add the capacity vector 
        self.f = f
        
        return self
    
    def add_coordinates(self, coord):
        """
        add a pair of coordinates to each node
        
        @type coord: number matrix
        @param coord: [x, y] position for each node
        
        @rtype: graph
        @return: graph with coordinates
        """
        n = self.nodes()            # number of nodes
        
        # check if the size of the coord vector is equal to n
        if coord.shape[0] != n:
            print 'ERROR: size of N and coordinates do not match'
            return self
        
        # add the coordinate vector 
        self.coord = coord
        
        return self
    
    def add_node(self):
        """
        add an unconnected node to the graph
        
        @rtype: graph
        @return: graph with new node
        """
        # append new lines to each relevant matrix
        self.N = vstack([self.N, [-1, -1]])
        self.B = append(self.B, 0)
        self.coord = vstack([self.coord, [0, 0]])
        
        return self
        
    def add_arc(self, i, j):
        """ 
        add an arc from node i to node j
        
        @type i: number
        @param i: node at the tail of the arc
        
        @type j: number
        @param j: node at the head of the arc
        
        @rtype: graph
        @return: graph with new arc
        """
        n = self.nodes()            # number of nodes
        
        # check if it is possible
        if max(i, j) > n:
            print 'ERROR: trying to add an arc to a non existing node'
            return self
        
        # add the arc
        self.A = vstack([self.A, [i, j, 0]])
        
        m = self.arcs()             # new number of arcs
        
        # correct the links
        pos = self.N[i-1,1]         # previous to last arc of i
        # if the node had no arcs, correct it in N
        if pos == -1:
            pos = m
            self.N[i-1,0] = m - 1
        else:
            self.A[pos,2] = m - 1   # point to the last arc
        self.N[i-1,1] = m - 1       # correct end_data point
        
        # pad with zeros in data where needed
        if size(self.c) != 0:
            self.c = append(self.c, 0)
        if size(self.u) != 0:
            self.u = append(self.u, 0)
        if size(self.f) != 0:
            self.f = append(self.f, 0)
        if size(self.mirror) != 0:
            self.mirror = append(self.mirror, 0)
        
        return self
    
    def add_data_to_arc_pos(self, pos, c, u, f):
        """
        adds data to a specified arc position
        
        @type pos: number (int)
        @param pos: arc position in the Adjacency matrix
        
        @type c: number
        @param c: arc cost
        
        @type u: number
        @param u: arc capacity
        
        @type f: number
        @param f: arc flow
        
        @rtype: graph
        @return: graph with new arc values
        """
        m = self.arcs()             # number of arcs
        
        # check if pos is viable
        if pos >= m:
            print "ERROR: selected position does not exist in A"
            return self
        
        # add data
        if size(self.c) != 0:
            self.c[pos] = c
        else:
            print "Warning: c was not added as no c vector exists in G"
        
        if size(self.u) != 0:
            self.u[pos] = u
        else:
            print "Warning: u was not added as no u vector exists in G"
        
        if size(self.f) != 0:
            self.f[pos] = f
        else:
            print "Warning: f was not added as no f vector exists in G"
            
        return self
    
    def set_type(self, type):
        """
        sets the type of the graph
        
        @type type: char
        @param type: type of graph    d: directed
                                      u: undirected
                                      r: residual
        
        @rtype: graph
        @return: graph with new type
        """
        # check if it is one of the allowed types
        if find("dur", type) == -1:
            print "ERROR: invalid type selected"
        else:
            self.type = type
        
        return self
        
    """
    Deleting Functions
    """
    def del_arc_pos(self, pos):
        """
        delete arc in position pos
        
        @type pos: number
        @param pos: position of arc to delete
        
        @rtype: graph
        @return: graph without the arc
        """
        m = self.arcs()
        n = self.nodes()
        
        # check if it is a valid position
        if pos >= m:
            print "ERROR: the position is not valid"
            return self
        
        # initialize temporal graph
        tG = Graph()
        tG.N = -1 * ones((n, 2), int)       # add all nodes without arcs
        
        # add arcs one by one, skipping pos
        for arc in range(m):
            # get arc information
            if arc != pos:
                i = self.A[arc, 0]
                j = self.A[arc, 1]
                tG.add_arc(i, j)
        
        # put N and A back into the graph
        self.A = tG.A
        self.N = tG.N
        
        # delete cost
        if size(self.c) != 0:
            self.c = delete(self.c, [pos])
        # delete capacity
        if size(self.u) != 0:
            self.u = delete(self.u, [pos])
        # delete flow
        if size(self.f) != 0:
            self.f = delete(self.f, [pos])
        # delete mirror
        if size(self.mirror) != 0:
            self.mirror = delete(self.mirror, [pos])
        
        return self
    
    def del_arc(self, i, j):
        """
        delete arc (i, j)
        
        @type i: number
        @param i: node at the tail of the arc
        
        @type j: number
        @param j: node at the head of the arc
        
        @rtype: graph
        @return: graph without the arc (i, j)
        """
        # get the position of the arc
        pos = self.get_arc_pos(i, j)
        
        # if the arc doesn't exist, return
        if pos == []:
            return self
        
        # otherwise delete the arc
        self.del_arc_pos(pos)
        
        return self
    
    def del_node(self, i):
        """
        delete node i and all its adjacent arcs
        
        @type i: number
        @param i: arc to delete
        
        @rtype: graph
        @return: graph without the node and adjacent arcs
        """
        # delete all out-arcs
        list = self.get_out_arcs_pos(i)
        while size(list) != 0:
            self.del_arc_pos(list[0])
            list = self.get_out_arcs_pos(i)
        
        # delete all in-arcs
        list = self.get_in_arcs_pos(i)
        while size(list) != 0:
            self.del_arc_pos(list[0])
            list = self.get_in_arcs_pos(i)
        
        # eliminate the node
        self.N = delete(self.N, [i-1], axis=0)
        self.coord = delete(self.coord, [i-1], axis=0)
        self.B = delete(self.B, i-1)
        
        # correct node names in A
        m = self.arcs()
        for arc in range(m):
            if self.A[arc,0] > i:
                self.A[arc,0] = self.A[arc,0] - 1
            if self.A[arc,1] > i:
                self.A[arc,1] = self.A[arc,1] - 1
        
        return self
    
    def strip_cost(self):
        """
        eliminate the cost vector
        
        @rtype: graph
        @return: graph without costs
        """
        # clean the vector
        self.c = empty(0)
        
        return self
    
    def strip_capacity(self):
        """
        eliminate the capacity vector
        
        @rtype: graph
        @return: graph without capacity
        """
        # clean the vector
        self.u = empty(0)
        
        return self
    
    def strip_flow(self):
        """
        eliminate the flow vector
        
        @rtype: graph
        @return: graph without flows
        """
        # clean the vector
        self.f = empty(0)
        
        return self
    
    def strip_external_flow(self):
        """
        eliminate the external flow vector
        
        @rtype: graph
        @return: graph without external flows
        """
        # number of nodes
        n = self.nodes()
        
        # clean the vector
        self.B = zeros(n)
        
        return self
    
    """
    File I/O Functions
    """
    def form_graph_from_file(self, file_name):
        """
        load graph information from data file
        
        @type file_name: string
        @param file_name: name of the file with the graph data
        
        @rtype: graph
        @return: graph
        """
        # initialize temporal variables
        N = []
        A = []
        B = []
        c = []
        u = []
        f = []
        coord = []
        
        file = open(file_name)           # open data file
        mode = 0                         # initialize mode
        
        # read each line of text file and put values in corresponding variables
        for line in file.xreadlines():
            # identify the area of the text file
            if line[0] == "#" or line[0] == "\r\n":
                mode = 0
            elif line[0] == "N":
                mode = 1
            elif line[0] == "A":
                mode = 2
            elif line[0] == "c":
                mode = 3
            elif line[0] == "u":
                mode = 4
            elif line[0] == "f":
                mode = 5
            elif line[0] == "x":
                mode = 6
            elif line[0] == "B":
                mode = 7
            elif line[0] == "t":
                mode = 0
                type = line[2]           # get the type
            
            # depending on the area, append data to the corresponding variable
            if line[0] == "[":
                if mode == 1:            # N       
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    N_line = [int(x) for x in line.split(',')]
                    N.append(N_line)
                elif mode == 2:          # A
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    A_line = [int(x) for x in line.split(',')]
                    A.append(A_line)
                elif mode == 3:          # c
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    c = [float(x) for x in line.split(',')]
                elif mode == 4:          # u
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    u = [float(x) for x in line.split(',')]
                elif mode == 5:          # f
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    f = [float(x) for x in line.split(',')]
                elif mode == 6:          # x
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    x_line = [float(x) for x in line.split(',')]
                    coord.append(x_line)
                elif mode == 7:          # B
                    # clean both sides
                    line = line.lstrip('[')
                    line = line.rstrip(']\r\n')
                    # get the numbers
                    B = [float(x) for x in line.split(',')]
        
        # transform arrays to matrices and transpose
        N = matrix(N)
        N = N.T
        A = matrix(A)
        A = A.T
        
        # build graph
        self.form_graph(N, A, type)
        
        # add data if it exists
        if c != []:
            self.add_cost(array(c))
        if u != []:
            self.add_capacity(array(u))
        if f != []:
            self.add_flow(array(f))
        if coord != []:
            coord = matrix(coord)
            coord = coord.T
            self.add_coordinates(coord)
        if B != []:
            self.add_external_flow(array(B))
        
        return self
    
    def save_graph_to_file(self, file_name):
        """
        save graph information to data file
        
        @type file_name: string
        @param file_name: name of the file with the graph data
        
        @rtype: graph
        @return: saved graph
        """
        n = self.nodes()
        
        if n == 0:
            # if there is no graph to store, skip
            return self
            
        # open the file for saving
        text_file = open(file_name, "w")
        
        # graph type
        text_file.write("# graph type\n")
        text_file.write("t %s\n" % (self.type))
        
        # graph nodes
        text_file.write("\n# Node data points\nN\n")
        N = array(self.N.T, int)
        line = list(N[0,:])
        text_file.write("%s\n" %(line))
        line = list(N[1,:])
        text_file.write("%s\n" %(line))
        
        # external flow on nodes
        text_file.write("\n# External Flows\nB\n")
        line = list(self.B)
        text_file.write("%s\n" %(line))
        
        # graph adjacency matrix
        text_file.write("\n# Adjacency matrix\n")
        if size(self.A) != 0:
            text_file.write("A\n")
            A = array(self.A.T, int)
            line = list(A[0,:])
            text_file.write("%s\n" %(line))
            line = list(A[1,:])
            text_file.write("%s\n" %(line))
            line = list(A[2,:])
            text_file.write("%s\n" %(line))
        
        # other information
        text_file.write("\n# graph elements: cost, capacity, flow\n")
        # costs
        if size(self.c) != 0:
            text_file.write("c\n")
            line = list(self.c)
            text_file.write("%s\n" %(line))
        # capacity
        if size(self.u) != 0:
            text_file.write("u\n")
            line = list(self.u)
            text_file.write("%s\n" %(line))
        # flow
        if size(self.f) != 0:
            text_file.write("f\n")
            line = list(self.f)
            text_file.write("%s\n" %(line))
        # coordinates
        text_file.write("\n# coordinates for draw\n")
        if size(self.coord) != 0:
            text_file.write("x\n")
            coord = array(self.coord.T)
            line = list(coord[0,:])
            text_file.write("%s\n" %(line))
            line = list(coord[1,:])
            text_file.write("%s\n" %(line))
        
        # close the file
        text_file.close()
        
        return self
        
    """
    Information Functions
    """
    def get_arc_pos(self, i, j):
        """
        get the position of arc (i, j) in the Adjacency matrix
        
        @type i: number
        @param i: node at the tail of the arc
        
        @type j: number
        @param j: node at the head of the arc
        
        @rtype: number
        @return: position of (i, j)
        """
        
        # check if node i has outgoing arcs
        if self.N[i-1,0] >= 0:
            pos = self.N[i-1,0]     # initial position of data for node i
        else:
            print 'Arc (%d, %d) does not exist' % (i, j)
            return []
        
        # check if arc (i,j) exists
        while self.A[pos,1] != j:
            pos = self.A[pos,2]     # search next arc in the list of node i
            # if no arcs are left, indicate it
            if pos == 0:
                print 'Arc (%d, %d) does not exist' % (i, j)
                return []
        
        return pos
    
    def get_out_arcs_pos(self, i):
        """
        get the positions of all outward arcs of node i
        
        @type i: number
        @param i: node
        
        @rtype: list
        @return: positions of outward arcs
        """
        # initialize the list
        list = empty(0, int)
        
        # starting point of data
        pos = self.N[i-1,0]
        
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1
        
        # iterate through all arcs in adjacency matrix
        while link != 0:
            list = append(list, pos) # add position to the list
            link = int(self.A[pos,2])
            pos = link               # next position to check
        
        return list
        
    def get_in_arcs_pos(self, i):
        """
        get the positions of all inward arcs of node i
        
        @type i: number
        @param i: node
        
        @rtype: list
        @return: positions of inward arcs
        """
        # number of arcs
        m = self.arcs()
        
        # initialize the list
        list = empty(0, int)
        
        # check all arcs
        for arc in range(m):
            # if the head of the arc is i, add it
            if self.A[arc,1] == i:
                list = append(list, arc)
        
        return list
    
    def get_adjacent_arcs_pos(self, i):
        """
        get the positions of all adjacent arcs of node i
        
        @type i: number
        @param i: node
        
        @rtype: list
        @return: positions of adjacent arcs
        """
        # number of arcs
        m = self.arcs()
        
        # initialize the list
        list = empty(0, int)
        
        # check all arcs and add the positions if they contain i
        for arc in range(m):
            if self.A[arc,0] == i or self.A[arc,1] == i:
                list = append(list, arc)    # add position to the list
                
        return list
    
    def get_cut_arcs_pos(self, S):
        """
        get the position of the arcs in a cut S
        
        @type S: vector
        @param S: cut (set of nodes in one side of the cut)
        
        @rtype: list
        @return: position of arcs in the cut S
        """
        positions = empty(0, int)
        
        # check each node in S
        for i in S:
            # get all out arcs from node i
            out_arcs = self.get_out_arcs_pos(i)
            # clean those connected to nodes in S
            index = 0
            for k in range(size(out_arcs)):
                arc = out_arcs[index]
                j = self.A[arc,1]       # head of the arc
                # if the head is in S, delete it
                if sum(S == j) > 0:
                    out_arcs = delete(out_arcs, index)
                else:
                    index += 1
            
            # get all in arcs to node i
            in_arcs = self.get_in_arcs_pos(i)
            # clean those connected to nodes in S
            index = 0
            for k in range(size(in_arcs)):
                arc = in_arcs[index]
                j = self.A[arc,0]       # tail of the arc
                # if the tail is in S, delete it
                if sum(S==j) > 0:
                    in_arcs = delete(in_arcs, index)
                else:
                    index += 1
            
            # paste both lists together
            positions = append(positions, out_arcs)
            positions = append(positions, in_arcs)
            
        return positions
    
    def get_adjacent_nodes(self, i):
        """
        get all the adjacent nodes of node i
        
        @type i: number
        @param i: node
        
        @rtype: list
        @return: list of adjacent nodes
        """
        # number of arcs
        m = self.arcs()
        
        # initialize the list
        list = empty(0, int)
        
        # check all arcs and add the positions if they contain i
        for arc in range(m):
            # when the tail is in i
            if self.A[arc,0] == i:
                j = self.A[arc,1]                   # adjacent node
                # if j is not on the list, add it
                if sum(list == j) == 0:
                    list = append(list, j)  # add node to the list
            # if the head is in i
            elif self.A[arc,1] == i:
                j = self.A[arc,0]                   # adjacent node
                # if j is not on the list, add it
                if sum(list == j) == 0:
                    list = append(list, j)  # add node to the list
                
        return list
    
    def get_arc_data(self, i, j):
        """
        get data from arc (i, j)
        
        @type i: number
        @param i: node at the tail of the arc
        
        @type j: number
        @param j: node at the head of the arc
        
        @rtype: number vector
        @return: vector with arc data [i, j, link, c, u, f]
        """
        # get the position of the arc
        pos = self.get_arc_pos(i, j)
        
        # check if arc exists
        if pos == []:
            return 0
        
        # get (i,j) link data
        arc_data = array(self.A[pos,:])
        # if it has a cost, add it
        if size(self.c) != 0:
            arc_data = append(arc_data, self.c[pos])
        else:
            arc_data = append(arc_data, [nan])
        
        # if it has a capacity, add it
        if size(self.u) != 0:
            arc_data = append(arc_data, self.u[pos])
        else:
            arc_data = append(arc_data, [nan])
        
        # if it has a flow, add it
        if size(self.f) != 0:
            arc_data = append(arc_data, self.f[pos])
        else:
            arc_data = append(arc_data, [nan])
        
        return arc_data
    
    def build_adjacency_lists(self):
        """
        build a list of adjacency nodes for each node
        
        @rtype: list of lists
        @return: list of adjacency nodes for each node
        """
        # number of arcs
        m = self.arcs()
        # number of nodes
        n = self.nodes()
        
        # initialize the matrix
        adj_matrix = zeros((n,n), int)
        
        # check all arcs and add the positions if they contain i
        for arc in range(m):
            i = self.A[arc,0]       # get edge elements
            j = self.A[arc,1]
            # indicate adjacency
            adj_matrix[i-1,j-1] = 1
            adj_matrix[j-1,i-1] = 1
            
        # build lists
        list = []
        for n_i in range(n):
            # build adjacency vector for node n_i+1
            list_i = empty(0, int)
            for n_j in range(n):
                if adj_matrix[n_i,n_j] == 1:
                    list_i = append(list_i, n_j+1)
            # add this list to the master list
            list.append(list_i)
        
        return list
    
    """
    Functions for Checking Properties
    """
    def is_correct_type(self, types):
        """
        checks if the graph belongs to one of the selected types
        
        @type types: string
        @param types: collection of all types to check
        
        @rtype: boolean
        @return: true if graph type belongs
        """
        # check the type
        if find(types, self.type) == -1:
            return False
        else:
            return True
    
    def is_top_sort(self):
        """
        checks if the graph is in topological order
        
        @rtype: boolean
        @return: true if graph is in topological order
        """
        # check if it a valid Graph
        if not self.is_correct_type('d'):
            return False
        
        # number of arcs
        m = self.arcs()
        
        # initialize condition
        cond = True
        
        for arc in range(m):
            # if the tail is larger than the head, it is not in order
            if self.A[arc,0] > self.A[arc,1]:
                cond = False
                return cond
            
        return cond
        
    def is_coloring(self, C):
        """
        checks if C is a stable coloring for the graph
        
        @type C: number vector
        @param C: coloring (color of each node)
        
        @rtype: boolean
        @return: true if C is coloring
        """
        C = array(C, int)
        
        # number of arcs
        m = self.arcs()
        
        # initialize condition
        cond = True
        
        for arc in range(m):
            i = self.A[arc,0]        # arc end-points
            j = self.A[arc,1]
            
            # if head and tail have the same color, stop
            if C[i-1] == C[j-1]:
                cond = False
                return cond
        
        return cond
    
    def reach_from(self, k):
        """
        checks which nodes are reachable from k using BFS,
        considering that all arcs are directed
        
        @type k: number
        @param k: node from which to check
        
        @rtype: binary vector
        @return: vector with 1 for those nodes that are reachable
        """
        # work over H so self is not arc-sorted
        H = self.copy()
        # do BFS
        reach, dummy = breath_first(H, k)
        
        # number of nodes
        n = self.nodes()
        
        for i in range(n):          # set as 1 all those that have an order
            if reach[i] != inf:
                reach[i] = 1
            else:
                reach[i] = 0
        
        return reach
    
    def u_reach_from(self, k):
        """
        checks which nodes are reachable from k using BFS,
        considering that all arcs are undirected
        
        @type k: number
        @param k: node from which to check
        
        @rtype: binary vector
        @return: vector with 1 for those nodes that are reachable
        """
        # number of nodes
        n = self.nodes()
        
        # reachable vector
        reach = zeros(n)
        # testing list
        list = array([k])
        
        while size(list) > 0:
            i = list[0]             # get first node
            list = delete(list, 0)  # eliminate it from the list
            
            # check all the out-arcs to add the adjacent nodes
            out_list = self.get_out_arcs_pos(i)
            for arc in out_list:
                j = self.A[arc,1]   # head of the arc
                # if it was not labeled, label it and add it to the testing list
                if reach[j-1] == 0:
                    reach[j-1] = 1
                    list = append(list, j)
            
            # check all the in-arcs to add the adjacent nodes
            in_list = self.get_in_arcs_pos(i)
            for arc in in_list:
                j = self.A[arc,0]   # tail of the arc
                # if it was not labeled, label it and add it to the testing list
                if reach[j-1] == 0:
                    reach[j-1] = 1
                    list = append(list, j)
                
        return reach
    
    """
    Graph Value Calculations
    """
    def total_tree_cost(self, T):
        """
        calculate the total cost of arcs in a tree
        
        @type T: number vector
        @param T: tree
        
        @rtype: number
        @return: cost of the tree
        """
        # check if the graph has a cost vector
        if size(self.c) == 0:
            print "ERROR: the graph has no cost vector"
            return 0
        
        n = self.nodes()        # number of nodes in the tree
        total_cost = 0          # initialization
        
        # sum up all the arcs in the tree
        for node in range(n):
            j = node + 1        # head of the arc
            i = T[node]         # tail of the arc
            # if a predecessor exist, add the arc
            if i != 0 and i != inf:
                arc = self.get_arc_data(i, j)
                total_cost += arc[3]
        
        return total_cost
    
    def total_path_cost(self, P):
        """
        calculate the total cost of arcs in a path
        
        @type P: number vector
        @param P: path
        
        @rtype: number
        @return: cost of the path
        """
        # check if the graph has a cost vector
        if size(self.c) == 0:
            print "ERROR: the graph has no cost vector"
            return 0
        
        n = size(P)             # number of nodes in the tree
        total_cost = 0          # initialization
        
        # sum up all the arcs in the tree
        for node in range(n - 1):
            i = P[node]         # head of the arc
            j = P[node + 1]     # tail of the arc
            # get the arc and sum it's cost
            arc = self.get_arc_data(i, j)
            total_cost += arc[3]
                
        return total_cost
    
    def total_arc_set_cost(self, set):
        """
        calculate the total cost of a set of arcs
        
        @type set: number vector
        @param set: position of arcs in the set
        
        @rtype: number
        @return: cost of the arc set
        """
        # check if the graph has a cost vector
        if size(self.c) == 0:
            print "ERROR: the graph has no cost vector"
            return 0
        
        # initialization
        total_cost = 0
        set = array(set, int)
        
        # sum up all the arcs in the set
        for arc in set:
            total_cost += self.c[arc]
        
        return total_cost
    
    def total_flow_cost(self):
        """
        calculate the total cost of a flow
        
        @rtype: number
        @return: cost of the flow
        """
        if size(self.c) == 0 or size(self.f) == 0:
            print "ERROR: the graph has no cost or flow vectors"
            return 0
        
        # number of arcs
        m = self.arcs()
        # initialization
        total_cost = 0
        
        # sum up the flow costs
        for arc in range(m):
            total_cost += self.c[arc] * self.f[arc]
        
        return total_cost
    
    def total_flow_from(self, s):
        """
        calculate the total flow from node s
        
        @type s: number
        @param s: node
        
        @rtype: number
        @return: total flow from node s
        """
        if size(self.f) == 0:
            print "ERROR: no flow vector in this graph"
            return 0
        
        # initialization
        flow = 0
        
        # get all out arcs from s
        out_arcs = self.get_out_arcs_pos(s)
        # sum up their flows
        for arc in out_arcs:
            flow += self.f[arc]
        
        in_arcs = self.get_in_arcs_pos(s)
        # subtract up their flows
        for arc in in_arcs:
            flow -= self.f[arc]
            
        return flow
    
    def get_cut_capacity(self, S):
        """
        calculate the total capacity of a cut S
        
        @type S: vector
        @param S: cut (set of nodes in one side of the cut)
        
        @rtype: number
        @return: total capacity of the cut S
        """
        if size(self.u) == 0:
            print "ERROR: no capacity vector in this graph"
            return 0
        
        # initialization
        capacity = 0
        
        # check the capacity of each node in S
        for i in S:
            # get all out arcs from node
            out_arcs = self.get_out_arcs_pos(i)
            # sum up their flows if the head is not in S
            for arc in out_arcs:
                j = self.A[arc,1]       # head of the arc
                # if the head is not in S, add the capacity
                if sum(S == j) == 0:
                    capacity += self.u[arc]
        
        return capacity
            
    """ Residual Graphs """
    def residual_graph(self):
        """
        build a residual graph from the current information
        
        @rtype: graph
        @return: residual graph
        """
        # check if it a valid Graph
        if not self.is_correct_type('d'):
            print "ERROR: the graph is not in one of the valid formats for residual_graph()"
            return self
        if size(self.u) == 0:
            print "ERROR: the graph has no capacities set"
            return self
        
        # residual graph definition and initialization
        R = Graph()
        R.type = "r"
        R.A = self.A.copy()
        R.N = self.N.copy()
        R.B = self.B.copy()
        R.source = self.source
        R.sink = self.sink
        if size(self.coord) != 0:
            R.coord = self.coord.copy()
         
        # number of arcs
        m = self.arcs()
        # add capacities
        R.u = zeros(m)
        R.u[0:m] = self.u.copy()
        # add flow
        R.f = zeros(m)
        # check if a flow exists
        if size(self.f) == 0:
            print 'Warning: the graph does not contain a flow vector, a zero vector was added'
        else:
            R.f = self.f
        
        # add costs
        if size(self.c) != 0:
            R.c = zeros(m)
            R.c[0:m] = self.c.copy()
        
        # mirror vector
        R.mirror = zeros(m, int)
        
        # add the reverse arc
        for arc in range(m):
            # get arc nodes
            i = self.A[arc,0]
            j = self.A[arc,1]
            
            # build reverse arc
            R = R.add_arc(j, i)
            # mirror links
            R.mirror[arc] = m + arc
            R.mirror[m + arc] = arc
            # set capacities
            R.u[m + arc] = R.f[arc]         # cap of residual arc = flow
            R.u[arc] = R.u[arc] - R.f[arc]  # cap of arc = cap - flow
            R.f[arc] = 1                    # indicate forward arc
            R.f[m + arc] = -1               # indicate backward arc
            # set costs if they exist
            if size(R.c) != 0:
                R.c[m + arc] = -R.c[arc]
        
        return R
    
    def graph_from_residual(self):
        """
        build a graph from the current residual graph
        
        @rtype: graph
        @return: graph
        """
        # check if it a valid Graph
        if not self.is_correct_type('r'):
            print "ERROR: the graph is not in one of the valid formats for graph_from_residual()"
            return self
        if size(self.u) == 0:
            print "ERROR: the residual graph has no capacities set"
            return self
        
        # graph definition and initialization
        G = Graph()
        G.type = "d"
        G.A = self.A.copy()
        G.N = self.N.copy()
        G.source = self.source
        G.sink = self.sink
        if size(self.coord) != 0:
            G.coord = self.coord.copy()
        
        m = self.arcs()                     # number of arcs for G
        # add capacities
        G.u = self.u.copy()
        # add flow
        G.f = self.f.copy()
        # add costs
        G.c = self.c.copy()
        # add external flow
        G.B = self.B.copy()
        
        # go over the arcs and correct the capacity and flow
        for arc in range(m):
            if self.f[arc] == -1:
                link = self.mirror[arc]     # link to forward arc
                G.f[link] = G.u[arc]
                G.u[link] = G.u[link] + G.u[arc]
                
        # eliminate the backwards arcs
        pos = 0
        for arc in range(m):
            # if it is a residual arc, eliminate it
            if self.f[arc] == -1:
                G = G.del_arc_pos(pos)
            else:
                pos += 1
        
        return G
    
    """
    Other Utilities
    """
    def copy(self):
        """
        make a copy of the graph
        
        @rtype: graph
        @return: graph
        """
        # new graph
        H = Graph()
        
        # copy structures
        H.A = self.A.copy()
        H.N = self.N.copy()
        H.B = self.B.copy()
        H.coord = self.coord.copy()
        
        H.c = self.c.copy()
        H.u = self.u.copy()
        H.f = self.f.copy()
        H.mirror = self.mirror.copy()
        
        H.type = self.type
        H.source = self.source
        H.sink = self.sink
        H.names = self.names
        
        return H
    
    def swap_arc(self, pos):
        """
        swap arc in position pos from (i, j) to (j, i)
        
        @type pos: number
        @param pos: position of arc to swap
        
        @rtype: graph
        @return: graph with swapped arc
        """
        # number of arcs
        m = self.arcs()
        
        # get arc information
        i = self.A[pos,0]
        j = self.A[pos,1]
        
        if size(self.c) != 0:
            c = self.c[pos]
        if size(self.u) != 0:
            u = self.u[pos]
        if size(self.f) != 0:
            f = self.f[pos]
        if size(self.mirror) != 0:
            mirror = self.mirror[pos]
        
        # delete the arc
        self = self.del_arc_pos(pos)
        # add reverse arc
        self = self.add_arc(j, i)
        
        # add data to it
        if size(self.c) != 0:
            self.c[m-1] = c
        if size(self.u) != 0:
            self.u[m-1] = u
        if size(self.f) != 0:
            self.f[m-1] = f
        if size(self.mirror) != 0:
            self.mirror[m-1] = mirror
            
        return self