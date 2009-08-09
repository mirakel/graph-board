"""
Graph Board Class v.1.0

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
from string import *                 # string management
from Tkinter import *                # GUI
from imp import *                    # for importing modules
from random import *                 # random number generator
from time import sleep               # timer function
# personal modules and classes
from GraphClass import *             # Graph classes

"""
GraphBoard Class
"""
class GraphBoard:
    """
    graph board class structure:
    
    master       : tkinter main Tk() object
    G            : graph
    
    node_size    : node size
    c_size       : canvas size
    source_color : color for source node
    sink_color   : color for sink node
    
    menu_bar     : menu bar
    frame        : canvas frame
    canvas       : canvas
    tool_bar     : right side tool bar
    sel_obj      : selected object
    curr_pos     : current click position
    
    set_mode     : board mode: "m" - move, "d" - delete, "a" - add
    e_view       : external flow/label view
    gui_mode     : identifies if GUI mode is True or False
    """
    def __init__(self, master, G, gui_mode, modules):
        """ 
        board initialization
        
        @type master: Tk() object
        @param master: tkinter master window object
        
        @type G: graph
        @param G: graph
        
        @type gui_mode: boolean
        @param gui_mode: use GUI or not
        
        @type modules: list
        @param modules: list of modules to load on the menu        
        """
        #************** graph parameters **************
        # define size of nodes (radius)
        self.node_size = 15
        # colors for source and sink
        self.source_color = "forest green"
        self.sink_color = "RoyalBlue1"
        # canvas size
        self.c_size = [800, 600]
        #**********************************************
        # adds the graph to the class
        self.graph = G
        # object state variable
        self.set_mode = "m"              # set to move
        # variables for moving/adding objects
        self.sel_obj = None              # selected object
        self.curr_pos = None             # current position
        self.e_view = False              # show or not external flows 
        
        # add master board to the class
        self.master = master
        self.master.title("Graph Board ..:mr rax:.. 2009 (c)")
        
        # set type of board
        self.gui_mode = gui_mode
        
        # create the menubar and build the main menu
        self.menu_bar = Menu(master)
        self.add_main_menu()
        
        # build the main frame
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)                # geometry manager: add frame to master
        
        # build toolbar frame
        self.toolbar = Frame(master, borderwidth=2, relief='raised')
        self.toolbar.pack(side=RIGHT, fill=Y)
        
        # add widgets to the board (including canvas)
        self.create_widgets()
        
        # add the modules & functions to the menu
        self.add_modules(modules)
        
        # print the first version of the graph
        self.draw_graph()
        
        return
    
    """
    Board Building Functions
    """
    def add_main_menu(self):
        """
        add the main menu to the board
        
        @param: None
        @return: None
        """
         # file menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.quit_board)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # if in GUI mode, add Graph Tools menu
        if self.gui_mode:
            tools_menu = Menu(self.menu_bar, tearoff=0)
            tools_menu.add_command(label="Export", command=self.export_draw)
            
            tools_menu.add_separator()
            
            tools_menu.add_command(label="Clean", command=self.draw_graph)
            tools_menu.add_checkbutton(label="Show External Flows",\
                                       command=self.external_flows_switch)
            # flow view tools
            flow_menu = Menu(self.menu_bar, tearoff=0)
            flow_menu.add_command(label="Flow Saturation",\
                                  command=self.draw_arc_saturation)
            flow_menu.add_command(label="Flow Volume", command=self.draw_arc_flow)
            tools_menu.add_cascade(label="Flow Views", menu=flow_menu)
            
            tools_menu.add_command(label="Re-position Nodes",\
                                   command=lambda x=True: self.electric_move(x))
            
            tools_menu.add_separator()
            # change types
            type_menu = Menu(self.menu_bar, tearoff=0)
            type_menu.add_command(label="Set to Directed",\
                                  command=lambda x="d": self.change_graph_type(x))
            type_menu.add_command(label="Set to Undirected",\
                                  command=lambda x="u": self.change_graph_type(x))
            tools_menu.add_cascade(label="Graph Types", menu=type_menu)
            
            # new graph menu
            new_menu = Menu(self.menu_bar, tearoff=0)
            new_menu.add_command(label="New Graph", command=self.new_graph)
            new_menu.add_separator()
            new_menu.add_command(label="Add Random Costs (int)",\
                                 command=lambda x="int": self.add_random_cost(x))
            new_menu.add_command(label="Add Random Costs (float)",\
                                 command=lambda x="float": self.add_random_cost(x))
            new_menu.add_separator()
            new_menu.add_command(label="Add Random Capacities (int)",\
                                 command=lambda x="int": self.add_random_capacity(x))
            new_menu.add_command(label="Add Random Capacities (float)",\
                                 command=lambda x="float": self.add_random_capacity(x))
            tools_menu.add_cascade(label="New Random Graph", menu=new_menu)
            
            # delete elements menu
            del_menu = Menu(self.menu_bar, tearoff=0)
            del_menu.add_command(label="Remove Costs",\
                                 command=lambda x="cost": self.remove_parameter(x))
            del_menu.add_command(label="Remove Capacities",\
                                 command=lambda x="capacity": self.remove_parameter(x))
            del_menu.add_command(label="Remove Flow",\
                                 command=lambda x="flow": self.remove_parameter(x))
            del_menu.add_command(label="Remove External Flow",\
                                 command=lambda x="ext_flow": self.remove_parameter(x))
            tools_menu.add_cascade(label="Remove Parameters", menu=del_menu)
            
            # add the menu
            self.menu_bar.add_cascade(label="Graph Tools", menu=tools_menu)
            
        self.master.config(menu=self.menu_bar)
        
        return
    
    def create_widgets(self):
        """ 
        add widgets to the board
        
        @param: None
        @return: None
        """
        # toolbal parameter
        buttons_width = 8
        
        # add canvas
        self.canvas = Canvas(self.frame, width=self.c_size[0],\
                             height=self.c_size[1], bg="white")
        self.canvas.grid(row=0, column=0, rowspan=3)
        
        # add buttons
        self.button = Button(self.toolbar, width=buttons_width, text="Export",\
                             command=self.export_draw)
        self.button.pack(side=TOP)
        if self.gui_mode:
            self.button = Button(self.toolbar, width=buttons_width, text="Clean",\
                                 command=self.draw_graph)
            self.button.pack(side=TOP)
            
        #self.button.grid(row=1, column=1)
        self.button = Button(self.toolbar, width=buttons_width, text="Quit",\
                             command=self.quit_board)
        self.button.pack(side=BOTTOM)
        
        # I/O activities: mouse
        self.canvas.bind('<ButtonPress-3>', self.right_click)
        self.canvas.bind('<ButtonPress-1>', self.left_click)
        self.canvas.bind('<B1-Motion>', self.move_mouse)
        self.canvas.bind('<ButtonRelease>', self.button_release)
        self.canvas.bind('<Double-Button-1>', self.double_click)
        # I/O activities: keyboard
        self.master.bind('<KeyPress-m>', self.press_m)
        self.master.bind('<KeyPress-a>', self.press_a)
        self.master.bind('<KeyPress-d>', self.press_d)
        
        return
    
    def add_modules(self, modules):
        """
        build the menu with all the modules
        
        @type modules: list
        @param modules: list of modules to add (Python program files)  
        """
        # import modules and generate menus
        if modules == None:
            return
        
        menu_list = []          # list with all the functions
        n_algs = []             # number of algorithms per module
        m_it = 0                # for m iterations
        
        # import all the modules and create menus for each
        for m in modules:
            # find the module and load it
            fp, pathname, description = find_module(m)
            module = load_module(m, fp, pathname, description)
            # get the module information
            menu_name, a_list = module.menu_items()
            
            # add each algorithm to a new menu
            a_list = array(a_list)
            n_algs = append(n_algs, shape(a_list)[0])       # number of algorithms
            
            # add function to menu array
            menu_list = append(menu_list, a_list[:,1])
            
            new_menu = Menu(self.menu_bar, tearoff=0)       # new menu to add
            # add each of the algorithms to the menu cascade
            for a in range(int(n_algs[m_it])):
                if a_list[a,0] == "separator" and a_list[a,1] == "separator":
                    new_menu.add_separator()
                else:
                    new_command = lambda r=sum(n_algs[0:m_it])+a,x=self: menu_list[r](x)
                    new_menu.add_command(label=a_list[a,0], command=new_command)
            # add the module as a menu
            self.menu_bar.add_cascade(label=menu_name, menu=new_menu)
            m_it = m_it + 1
        
        # configure the menu bar
        self.master.config(menu=self.menu_bar)
        
        return
        
    """
    Canvas I/O Activities
    """
    def right_click(self, event):
        """
        activities when right-clicking
        
        @type event: event
        @param event: mouse clicking event
        """
        # add a node
        self.add_node(event)
        
        return
    
    def left_click(self, event):
        """
        activities when left-clicking
        
        @type event: event
        @param event: mouse clicking event
        """
        # identify selected object
        self.get_object(event)
        
        return
    
    def move_mouse(self, event):
        """
        activities when moving the mouse
        
        @type event: event
        @param event: mouse moving event
        """
        # when on moving mode
        if self.set_mode == "m":
            # move the selected object
            self.move_object(event)
        # when on adding mode
        elif self.set_mode == "a":
            # add an arc
            self.new_arc(event)
        
        return
    
    def button_release(self, event):
        """
        activities when the button is released
        
        @type event: event
        @param event: mouse button release event
        """
        # only work if adding a new arc
        if self.sel_obj != None:
            # get tag of selected object
            sel_tag = self.canvas.gettags(self.sel_obj)
            if sel_tag != ():
                sel_tag = sel_tag[0]
        
        # if adding a new arc, go to the add arc event
        if self.set_mode == "a" and sel_tag[0:3] == "new":
            self.add_arc(event)
        
        return
        
    def double_click(self, event):
        """ 
        double click event
        
        @type event: event
        @param event: mouse double clicking event
        """
        # identify the object
        self.get_object(event)
        
        # in moving or adding mode, add data to the double clicked object
        if self.set_mode == "m" or self.set_mode == "a":
            # add data
            self.add_data(event)
        # in deleting mode, delete the selected object
        elif self.set_mode == "d":
            # delete an arc
            self.delete_object(event)
        
        return
    
    """
    Keyboard I/O Activities
    """
    def press_m(self, event):
        """
        routine when m is pressed - set to moving mode
        
        @type event: event
        @param event: key pressing event
        """
        print "Mode set to move"
        
        self.set_mode = "m"
        # change text label
        self.canvas.itemconfigure("mode_state", text="mode = move")
        
        return
            
    def press_a(self, event):
        """
        routine when a is pressed - set to adding mode
        
        @type event: event
        @param event: key pressing event
        """
        print "Mode set to add"
        
        self.set_mode = "a"
        # change text label
        self.canvas.itemconfigure("mode_state", text="mode = add")
        
        return
            
    def press_d(self, event):
        """
        routine when d is pressed - set to deleting mode
        
        @type event: event
        @param event: key pressing event
        """
        print "Mode set to delete"
        
        self.set_mode = "d"
        # change text label
        self.canvas.itemconfigure("mode_state", text="mode = delete")
        
        return
    
    """
    Main Menu/Toolbar Functions
    """
    def quit_board(self):
        """ 
        quitting routine
        
        @param: None
        @return: None 
        """
        # save the current graph in a tmp file
        self.graph.save_graph_to_file("draw_tmp.txt")
        
        # kill the window
        self.master.destroy()
        
        return
    
    def export_draw(self, *args):
        """ 
        export current drawing to a .ps file
        
        @note: the following parameters are optional (but if used, both are required)
        
        @type file_name: string 
        @param file_name:name of the file to store the .ps
        
        @type mode: char
        @param mode: saving mode: "w" write, "a" append
           
        @return: None 
        """
        # initialization
        file_name = "graph.ps"
        mode = "w"
        
        # if arguments are given, get the filename and mode
        if len(args) > 0:
            file_name = args[0]
            mode = args[1]
            
        # file to write the ps
        ps_file = open(file_name, mode)
        # build ps page
        page = self.canvas.postscript(colormode='color', pagex=0, pagey=0, pageanchor="sw")
        
        # write to file and close
        ps_file.write(page)
        ps_file.close()
        
        return
        
    """
    Adding Functions
    """
    def new_graph(self):
        """
        create a random new graph
        
        @param: None
        @return: None 
        """
        # get the number of nodes and arcs
        n = 0
        while n <= 0 or not isinstance(n, int):
            n = int(raw_input("Number of nodes: \n"))
        
        m = 0
        while m <= 0 or not isinstance(m, int):
            m = int(raw_input("Number of arcs: \n"))
        
        # clear the canvas
        self.canvas.delete("all")
        
        # new random graph
        self.graph = self.graph.random_graph([n, m], ["directed"])
        
        # add random coordinates
        for node in range(n):
            # randomly choose arc positions
            x_pos = uniform(self.node_size, self.c_size[0] - self.node_size)
            y_pos = uniform(self.node_size, self.c_size[1] - self.node_size)
            # add coordinates to coord vector
            self.graph.coord[node] = array([x_pos, y_pos], float)
        
        # make sure that the coord matrix is a float
        self.graph.coord = matrix(self.graph.coord, float)
        
        # move the nodes using electric force method
        self.electric_move(False)
        
        return
    
    def add_data(self, event):
        """ 
        manage adding data when double click is pressed - define what
        object to add the data on
        
        @type event: event
        @param event: mouse clicking event
        
        @return: None
        """
        # tag of selected object
        sel_tag = self.canvas.gettags(self.sel_obj)
        
        # if the tag is empty, return
        if sel_tag == ():
            return
        
        # if it is not a node or the new arc, return
        sel_tag = sel_tag[0]
        if sel_tag[0:3] != "arc" and sel_tag[0:4] != "tarc" and\
        sel_tag[0:3] != "nod" and sel_tag[0:4] != "tnod" and sel_tag[0:4] != "enod":
            return
        
        # add data depending if it is a node or an arc
        if sel_tag[0:3] == "nod" or sel_tag[0:4] == "tnod":
            self.add_node_data(sel_tag)
        elif sel_tag[0:3] == "arc" or sel_tag[0:4] == "tarc":
            self.add_arc_data(sel_tag)
        elif sel_tag[0:4] == "enod":
            self.add_external_data(sel_tag)
            
        return
    
    def add_arc_data(self, sel_tag):
        """
        adds data to a double-clicked arc
        
        @type sel_tag: string
        @param sel_tag: tag of the selected arc
        
        @return: None
        """
        # get arc parameters
        if sel_tag[0:3] == "arc":
            arc = int(sel_tag[4:])                     # arc position
        elif sel_tag[0:4] == "tarc":
            arc = int(sel_tag[5:])
        
        line = self.get_arc_text(arc)
        print "add data to arc %d: %s" %(arc, line)
        
        c, u, f = [], [], []
        # get data to input
        if size(self.graph.c) != 0:
            c = float(raw_input("data for c: \n"))
        if size(self.graph.u) != 0:
            u = float(raw_input("data for u: \n"))
        if size(self.graph.f) != 0:
            f = float(raw_input("data for f: \n"))
        # add data
        self.graph.add_data_to_arc_pos(arc, c, u , f)
        
        # correct text in board
        line = self.get_arc_text(arc)
        self.canvas.itemconfigure("tarc_%d" %(arc), text=line)
        
        return
    
    def add_arc(self, event):
        """ 
        add a new arc when the button is released, after the new_arc operation
        
        @type event: event
        @param event: mouse clicking event
        
        @return: None
        """
        #get the object
        self.get_object(self.curr_pos)
        # get tag of previously selected object (previous node)
        sel_tag = self.canvas.gettags(self.sel_obj)
        sel_tag = sel_tag[0]
        # node number
        i = int(sel_tag[6:])
        # current position of the node (tail node)
        x_1 = self.graph.coord[i-1,0]
        y_1 = self.graph.coord[i-1,1]
        
        # get objects near mouse button release position
        self.sel_obj = self.canvas.find_overlapping(event.x - 5, event.y - 5,\
                                                    event.x + 5, event.y + 5)
        
        # only add the arc if the release was near a node
        for obj in self.sel_obj:
            # check each object
            tmp_object = obj
            # get its tag
            tmp_tag = self.canvas.gettags(tmp_object)
            tmp_tag = tmp_tag[0]
            # if it is a node, keep it
            if tmp_tag[0:3] == "nod":
                # update the selected object
                self.sel_obj = tmp_object
                # get the node tag
                sel_tag = self.canvas.gettags(self.sel_obj)
                break
        
        # if the tag is empty, return
        if sel_tag == ():
            self.canvas.delete("new")
            return
        
        # if it is not a node or the new arc, return
        sel_tag = sel_tag[0]
        if sel_tag[0:3] != "nod":
            self.canvas.delete("new")
            return
        
        # node number (head node)
        j = int(sel_tag[5:])
        # get position of the node
        x_2 = self.graph.coord[j-1,0]
        y_2 = self.graph.coord[j-1,1]
        
        # if it is i again, return
        if j == i:
            # eliminate the arc
            self.canvas.delete("new")
            return
        
        # correct the arc coordinates to account for node size
        x_1, y_1, x_2, y_2 = self.get_arc_coord(x_1, y_1, x_2, y_2)
        # set the arc coordinates
        self.canvas.coords("new", x_1, y_1, x_2, y_2)
        # put arc
        self.canvas.itemconfigure("new", fill="black")
        
        # add the arc to the graph structure and add the arc text
        self.graph.add_arc(i, j)
        m = self.graph.arcs()
        
        # add text to the arc
        line = self.get_arc_text(m - 1)
        self.canvas.create_text((x_1 + x_2) / 2, (y_1 + y_2) / 2,\
                                text=line, tag="tarc_%d" %(m - 1))
                
        # add the correct tag to the arc and remove "new" tag
        self.canvas.addtag_withtag("arc_%d" %(m - 1), "new")
        self.canvas.dtag("new", "new")
        print "Added: arc from (%d, %d)" %(i, j)
        
        return
    
    def add_external_data(self, sel_tag):
        """
        add data for external flow on a node
        
        @type sel_tag: string
        @param sel_tag: tag of the selected node
        
        @return: None
        """
        # get the node number
        i = int(sel_tag[6:])
        print "add external flow to node %d" %(i)
        
        # ask for the flow
        flow = float(raw_input("external in-flow: \n"))
        # add the flow to the graph
        self.graph.B[i-1] = flow
        # update the drawing
        self.canvas.itemconfigure("enode_%d" %(i), text=flow)
        
        return
    
    def add_node_data(self, sel_tag):
        """
        manages which nodes are source or sink depending on
        double-click events
        
        @type sel_tag: string
        @param sel_tag: tag of the selected node
        
        @return: None
        """
        # get node parameters
        if sel_tag[0:3] == "nod":
            i = int(sel_tag[5:])                            # node number
        elif sel_tag[0:4] == "tnod":
            i = int(sel_tag[6:])
        
        # if there is no source, add it
        if self.graph.source == [] and self.graph.sink != i:
            self.graph.source = i
            self.canvas.itemconfigure("node_%d" %(i), fill=self.source_color)
        # if double-click is over source, delete source
        elif self.graph.source != [] and self.graph.source == i:
            self.graph.source = []
            self.canvas.itemconfigure("node_%d" %(i), fill="white")
        # if double click is over other node and no sink exists, set as sink
        elif self.graph.source != [] and self.graph.sink == []:
            self.graph.sink = i
            self.canvas.itemconfigure("node_%d" %(i), fill=self.sink_color)
        # if double click is over sink, eliminate it
        elif self.graph.source != [] and self.graph.sink == i:
            self.graph.sink = []
            self.canvas.itemconfigure("node_%d" %(i), fill="white")
        # if no source and double-click on sink shift
        elif self.graph.source == [] and self.graph.sink == i:
            self.graph.sink = []
            self.graph.source = i
            self.canvas.itemconfigure("node_%d" %(i), fill=self.source_color)
        
        return
    
    def add_node(self, event):
        """ 
        add a node by right-clicking
        
        @type event: event
        @param event: mouse clicking event
        """
        # add the node to N
        self.graph.add_node()
        # get new number of nodes
        n = self.graph.nodes()
        
        # mouse click coordinates
        x_pos, y_pos = event.x, event.y
        # add coordinates to coord vector
        self.graph.coord[n-1,:] = array([x_pos, y_pos])
        
        # circle coordinates
        x_1 = x_pos - self.node_size
        y_1 = y_pos - self.node_size
        x_2 = x_pos + self.node_size
        y_2 = y_pos + self.node_size
        # draw node
        self.canvas.create_oval(x_1, y_1, x_2, y_2, fill="white",\
                                activeoutline="gray", tag="node_%d" %(n))
        self.canvas.create_text(x_pos, y_pos, text=n, tag="tnode_%d" %(n))
        
        # add a label
        if self.e_view:
            y_label = y_pos - 1.5 * self.node_size
            self.canvas.create_text(x_pos, y_label, text=self.graph.B[n-1],\
                                    tag="enode_%d" %(n))
        
        print "Added: node (%d)" %(n)
        
        return
    
    def add_random_cost(self, type):
        """
        add a random cost to the arcs
        
        @type type: string
        @param type: cost type: "int", "float"  
        """
        # ask for the limit values
        c_min = float(raw_input("minimum cost: \n"))
        c_max = float(raw_input("maximum cost: \n"))
        
        self.graph = self.graph.add_random_cost([c_min, c_max], type)
        
        # re-draw the graph
        self.draw_graph()
        
        return
    
    def add_random_capacity(self, type):
        """
        add a random capacity to the arcs
        
        @type type: string
        @param type: cost type: "int", "float"  
        """
        # ask for the limit values
        U = float(raw_input("maximum capacity: \n"))
        
        self.graph = self.graph.add_random_capacity(U, type)
        
        # re-draw the graph
        self.draw_graph()
        
        return
        
    """
    Deleting Functions
    """
    def delete_object(self, event):
        """
        manage the deleting function in the board, choosing what object
        to delete
        
        @type event: event
        @param event: mouse clicking event
        
        @return: None
        """
        # identify what object to delete
        sel_tag = self.canvas.gettags(self.sel_obj)
        
        # if the tag is empty, return
        if sel_tag == ():
            return
        # if it is not a node or the new arc, return
        sel_tag = sel_tag[0]
        if sel_tag[0:3] != "nod" and sel_tag[0:3] != "arc" and\
        sel_tag[0:4] != "tnod" and sel_tag[0:4] != "tarc":
            return
        
        # if it is an arc, delete it
        if sel_tag[0:3] == "arc":
            arc = int(sel_tag[4:])
            self.del_arc(arc)
        elif sel_tag[0:4] == "tarc":
            arc = int(sel_tag[5:])
            self.del_arc(arc)
        
        # if it is a node, delete it
        elif sel_tag[0:3] == "nod":
            i = int(sel_tag[5:])
            self.del_node(i)
        elif sel_tag[0:4] == "tnod":
            i = int(sel_tag[6:])
            self.del_node(i)
            
        return
    
    def del_node(self, i):
        """
        deletes the selected node and its adjacent arcs
        
        @type i: number
        @param i: node number to delete
        
        @return: None  
        """
        # delete node
        self.graph.del_node(i)
        # re-draw the graph
        self.draw_graph()
        
        print "Deleted: node (%d)" %(i)
        
        return
    
    def del_arc(self, arc):
        """
        deletes the selected arc
        
        @type arc: number
        @param arc: arc position
        
        @return: None  
        """
        # get arc end-points
        i = self.graph.A[arc,0]
        j = self.graph.A[arc,1]
        
        #delete arc
        self.graph.del_arc_pos(arc)
        #re-draw graph
        self.draw_graph()
        
        print "Deleted: arc from (%d, %d)" %(i,j)
        
        return
    
    def remove_parameter(self, parameter):
        """
        removes selected parameters from the graph
        
        @type parameter: string
        @param parameter: parameter to remove "cost", "capacity", "flow", "ext_flow"
        """
        if parameter == "cost":
            self.graph = self.graph.strip_cost()
        elif parameter == "capacity":
            self.graph = self.graph.strip_capacity()
        elif parameter == "flow":
            self.graph = self.graph.strip_flow()
        elif parameter == "ext_flow":
            self.graph = self.graph.strip_external_flow()
        
        # re-draw the graph
        self.draw_graph()
        
        return
       
    """
    Get Information Functions
    """
    def get_object(self, event):
        """ 
        get object closest to the click event and store the object
        and its location
        
        @type event: event
        @param event: mouse clicking event
        
        @return: None
        @attention: this function modifies the sel_obj and curr_pos class variables
        """
        # get the object closest to the click
        x_pos, y_pos = event.x, event.y
        object = self.canvas.find_closest(x_pos, y_pos, halo=None, start=None)
        
        # store the object id
        self.sel_obj = object
        # store the event
        self.curr_pos = event
        
        return
    
    def get_arc_text(self, pos):
        """
        get data from arc in position pos in text form
        
        @type pos: number
        @param pos: position of arc to get data from
        
        @rtype: string
        @return: string with data for arc in position pos
        """
        # number of arcs
        m = self.graph.arcs()
        
        if pos >= m:
            print "ERROR: selected position does not exist in A"
            return []
        
        if size(self.graph.c) == 0 and size(self.graph.u) == 0 and size(self.graph.f) == 0:
            text = ""
            return text
        else:
            text = "["
        
        # if c exists, add it
        if size(self.graph.c) != 0:
            c = '%.2f, ' % (self.graph.c[pos])    # cost
            text += c
        
        # if u exists, add it
        if size(self.graph.u) != 0:
            u = '%.2f, ' % (self.graph.u[pos])    # capacity/residual cap
            text += u
        
        # if f exists, add it
        if size(self.graph.f) != 0 and not self.graph.is_correct_type('r'):
            f = '%.2f' % (self.graph.f[pos])    # flow
            text += f
        
        text += "]"
        
        return text
    
    def get_arc_coord(self, x_1, y_1, x_2, y_2, *args):
        """
        correct the coordinates for the arcs to account
        for the size of the node
        
        @type x_1: number
        @param x_1: x coordinate of start of the arc
        
        @type y_1: number
        @param y_1: y coordinate of start of the arc
        
        @type x_2: number
        @param x_2: x coordinate of end of the arc
        
        @type y_2: number
        @param y_2: y coordinate of end of the arc
        
        @note: optional parameter
        @type arc_t: int
        @param arc_t: indicate if it is a forward (1) or backward (-1) arc
        
        @rtype: vector
        @return: corrected coordiantes
        """
        # get the arc type
        arc_t = 0
        if size(args) > 0:
            arc_t = args[0]
        
        # projection angle
        angle = arctan2(y_2 - y_1, x_2 - x_1)
        
        # correct line end points
        if arc_t == "r":
            x_1 = x_1 + self.node_size * cos(angle + pi / 5.0)
            y_1 = y_1 + self.node_size * sin(angle + pi / 5.0)
            x_2 = x_2 - self.node_size * cos(angle - pi / 5.0)
            y_2 = y_2 - self.node_size * sin(angle - pi / 5.0)
        else:
            x_1 = x_1 + self.node_size * cos(angle)     # x_pos of i
            y_1 = y_1 + self.node_size * sin(angle)     # y_pos of i
            x_2 = x_2 - self.node_size * cos(angle)     # x_pos of j
            y_2 = y_2 - self.node_size * sin(angle)     # y_pos of j
        
        return [x_1, y_1, x_2, y_2]
    
    """
    Moving Functions
    """
    def move_object(self, event):
        """
        manage moving routine, selecting what to move
        
        @type event: event
        @param event: mouse moving event
        
        @return: None
        """
        # get the object tag
        sel_tag = self.canvas.gettags(self.sel_obj)
        
        # if the tag is empty, return
        if sel_tag == ():
            return
        
        # if it is not a node, return
        sel_tag = sel_tag[0]
        if sel_tag[0:3] != "nod" and sel_tag[0:4] != "tnod":
            return
        
        # if it was the label, correct it to get the node number
        if sel_tag[0:4] == "tnod":
            # eliminate the "t"
            sel_tag = sel_tag[1:]
            # get node number
            i = int(sel_tag[5:])
            # set as object the node
            self.sel_obj = self.canvas.find_withtag("node_%d" %(i))
            
        # node number
        i = int(sel_tag[5:])
            
        # get the mouse position
        x_pos, y_pos = event.x, event.y
        
        # position variation of node
        dx = x_pos - self.curr_pos.x
        dy = y_pos - self.curr_pos.y
        
        # move the node
        self.move_node(i, dx, dy)
        
        # update position/ store it
        self.curr_pos = event
        
        return
    
    def move_node(self, i, dx, dy):
        """
        move node i an amount dx in x and dy in y
        
        @type i: number
        @param i: node number
        
        @type dx: number
        @param dx: movement in x direction
        
        @type dy: number
        @param dy: movement in y direction
        
        @return: None    
        """
        # current position of node i
        x_1 = self.graph.coord[i-1,0] + dx
        y_1 = self.graph.coord[i-1,1] + dy
        
        # update in cord matrix
        self.graph.coord[i-1,:] = array([x_1, y_1])
        
        # move node
        self.sel_obj = self.canvas.find_withtag("node_%d" %(i)) # get the node
        self.canvas.move(self.sel_obj, dx, dy)                  # move it
        
        # move text
        t_obj = self.canvas.find_withtag("tnode_%d" %(i))       # get the related text
        self.canvas.move(t_obj, dx, dy)
        # move external flow label if it exists
        if self.e_view:
            e_obj = self.canvas.find_withtag("enode_%d" %(i))   # get the external flow text
            self.canvas.move(e_obj, dx, dy)
        
        # move adjacent arcs
        list = self.graph.get_out_arcs_pos(i)             # get out arc list
        for arc in list:
            # move the arc's tail
            j = self.graph.A[arc,1]                       # head of the arc
            # position of the head
            x_2 = self.graph.coord[j-1,0]
            y_2 = self.graph.coord[j-1,1]
            # correct coordinates
            xx_1, xy_1, x_2, y_2 = self.get_arc_coord(x_1, y_1, x_2, y_2)
            # move the arc
            self.canvas.coords("arc_%d" %(arc), xx_1, xy_1, x_2, y_2)
            self.canvas.coords("tarc_%d" %(arc), (xx_1 + x_2) / 2.0, (xy_1 + y_2) / 2.0)
            
        list = self.graph.get_in_arcs_pos(i)              # get in arc list
        for arc in list:
            # move the arc's head 
            j = self.graph.A[arc,0]                       # tail of the arc
            # position of the tail
            x_2 = self.graph.coord[j-1,0]
            y_2 = self.graph.coord[j-1,1]
            # correct coordinates
            x_2, y_2, xx_1, xy_1 = self.get_arc_coord(x_2, y_2, x_1, y_1)
            # move the arc
            self.canvas.coords("arc_%d" %(arc), x_2, y_2, xx_1, xy_1)
            self.canvas.coords("tarc_%d" %(arc), (xx_1 + x_2) / 2.0, (xy_1 + y_2) / 2.0)
        
        return
    
    def new_arc(self, event):
        """ 
        manage the movement of the new arc while the mouse moves
        
        @type event: event
        @param event: mouse moving event
        
        @return: None
        """
        # style of graph
        type = self.graph.type
        
        # define arrow type
        if type == "d":
            arrow_type = "last"
        else:
            arrow_type = "none"
        
        # get the tag of the last selected object
        sel_tag = self.canvas.gettags(self.sel_obj)
        
        # if the tag is empty, return
        if sel_tag == ():
            return
        
        # if it is not a node or the new arc, return
        sel_tag = sel_tag[0]
        if sel_tag[0:3] != "nod" and sel_tag[0:3] != "new":
            return
        
        # get the mouse position
        x_2, y_2 = event.x, event.y                    # current mouse position
        x_1, y_1 = self.curr_pos.x, self.curr_pos.y    # tail position
        
        # if we are in the node, set initial conditions
        if sel_tag[0:3] == "nod":
            # node number
            i = int(sel_tag[5:])
            # current position of node i
            x_1 = self.graph.coord[i-1,0]
            y_1 = self.graph.coord[i-1,1]
            # store it for future use
            self.curr_pos.x = x_1
            self.curr_pos.y = y_1
            # add arc line and set it as selected object
            x_1, y_1, dum, dum = self.get_arc_coord(x_1, y_1, x_2, y_2)
            self.sel_obj = self.canvas.create_line(x_1, y_1, x_2, y_2,\
                                                    fill="blue", arrow=arrow_type, tag="new")
        # if we are moving the arc already refresh
        elif sel_tag[0:3] == "new":
            # correct the arc coordinates
            x_1, y_1, dum, dum = self.get_arc_coord(x_1, y_1, x_2, y_2)
            # move the head of the arc
            self.canvas.coords("new", x_1, y_1, x_2, y_2)
            
        return
    
    def electric_move(self, draw_mode):
        """
        move the nodes to accommodate them in the canvas using
        electro-dynamic and spring PDE
        
        @type draw_mode: boolean 
        @param draw_mode: if true, draws all node movements
        
        @return: None 
        """
        # simulation parameters
        M = 80.0        # particle mass (Kg) (80)
        q = 5e2         # particle charge * sqrt(k) (5e2)
        L = 0.5         # border charge density * 2k (0.5)
        dt = 0.6        # time interval (0.6)
        sk = .02        # spring constant (0.02)
        T = 2000        # number of samples (2k)
        st = 0.00001    # sleep interval (0.00001)
        vc = 0.6        # viscous coefficient (0.6)
        
        # in not draw mode, increase vc for faster performance
        if not draw_mode:
            vc = 6.0
        
        # number of nodes
        n = self.graph.nodes()
        # number of arcs
        m = self.graph.arcs()
        
        # velocity vector, start with a random initial velocity
        v = 2.0 * rand(n,2) - 1.0
        
        # force matrices
        Fv = zeros((n,2), float)    # viscous force
        Fb = zeros((n,2), float)    # border electric force
        Fs = zeros((n,2), float)    # spring force
        Fe = zeros((n,2), float)    # electric particle force
        
        # run the simulation for T time samples
        for t in range(T):
            # get maximum speed
            max_speed = max(max(v[:,0]), max(v[:,1]))
            # if it is too small, stop
            if max_speed < 0.1:
                break
            
            # position of all nodes at time t
            pos = self.graph.coord.copy()
            
            # calculate viscous force for all nodes
            Fv = -vc * v * 1.0
            
            # calculate border force
            t_x = self.c_size[0] * ones((n,1), float)
            t_y = self.c_size[1] * ones((n,1), float)
            Fb = q * L * (1.0 / pos - 1.0 / (bmat('t_x t_y') - pos))
            
            # calculate spring force
            Fs = zeros((n,2), float)    # spring force
            for arc in range(m):
                # get nodes of arc
                i = self.graph.A[arc,0]
                j = self.graph.A[arc,1]
                # get node positions
                x_i = pos[i - 1,0]
                y_i = pos[i - 1,1]
                x_j = pos[j - 1,0]
                y_j = pos[j - 1,1]
                # calculate parameters
                r = sqrt((x_i - x_j)**2 + (y_i - y_j)**2)   # distance
                theta = arctan2(y_i - y_j, x_i - x_j)       # angle
                # calculate force
                F_tmp = 1.0 * sk * r
                # add force projections for i
                Fs[i - 1,0] -= F_tmp * cos(theta)
                Fs[i - 1,1] -= F_tmp * sin(theta)
                # add force projections for j
                Fs[j - 1,0] += F_tmp * cos(theta)
                Fs[j - 1,1] += F_tmp * sin(theta)
            
            # calculate electric force, add total force and move each node
            Fe = zeros((n,2), float)
            for i_node in range(n):
                i = i_node + 1
                # get node position
                x_i = pos[i_node,0]
                y_i = pos[i_node,1]
                
                # check all "next" nodes
                for j_node in range(i_node + 1, n):
                    j = j_node + 1
                    # node position
                    x_j = pos[j_node,0]
                    y_j = pos[j_node,1]
                    
                    # calculate parameters
                    r = sqrt((x_i - x_j)**2 + (y_i - y_j)**2)   # distance
                    theta = arctan2(y_i - y_j, x_i - x_j)       # angle
                    
                    # calculate electric force value
                    F_tmp = 1.0 * (q**2) / (r**2)
                    # add force projections for node i
                    Fe[i_node,0] += F_tmp * cos(theta)
                    Fe[i_node,1] += F_tmp * sin(theta)
                    # add force projections for node j
                    Fe[j_node,0] -= F_tmp * cos(theta)
                    Fe[j_node,1] -= F_tmp * sin(theta)
                
                # total force and acceleration on each direction
                F_x = Fs[i_node,0] + Fe[i_node,0] + Fb[i_node,0] + Fv[i_node,0]
                F_y = Fs[i_node,1] + Fe[i_node,1] + Fb[i_node,1] + Fv[i_node,1]
                # calculate accelerations
                a_x = F_x / M
                a_y = F_y / M
                
                # update position: x = x_ + v_ * dt, but limit if gets to the border
                dx = v[i_node,0] * dt + 0.5 * a_x * dt * dt
                if x_i + dx <= self.node_size or x_i + dx >= self.c_size[0] - self.node_size:
                    dx = 0
                
                dy = v[i_node,1] * dt + 0.5 * a_y * dt * dt
                if y_i + dy <= self.node_size or y_i + dy >= self.c_size[1] - self.node_size:
                    dy = 0
                
                # update velocity due to force
                v[i_node,0] += dt * a_x
                v[i_node,1] += dt * a_y
                
                # move node
                if draw_mode:
                    # in drawing mode move the node visually
                    self.move_node(i_node + 1, dx, dy)
                else:
                    # in calculation mode only update the matrix
                    x = self.graph.coord[i_node,0] + dx
                    y = self.graph.coord[i_node,1] + dy
                    self.graph.coord[i_node,:] = array([x, y])
                
            self.master.update_idletasks()
            
        if draw_mode:
            # in drawing mode, indicate
            print "Done!"
        else:
            # in calculation mode re-draw the graph 
            self.draw_graph()
        
        return
    
    """
    Main Drawing Functions
    """
    def draw_graph(self):
        """ 
        draw the graph on the board (self.graph)
        
        @param: None 
        @return: None
        """
        # number of nodes
        n = self.graph.nodes()
        # number of arcs
        m = self.graph.arcs()
        # graph type
        type = self.graph.type
        
        # define arrow type
        if self.graph.is_correct_type('dr'):
            arrow_type = "last"
        else:
            arrow_type = "none"
        
        # clear canvas just in case
        self.canvas.delete("all")
        
        # draw nodes
        for node in range(n):
            x_pos = self.graph.coord[node,0]  # x coordinate for node
            y_pos = self.graph.coord[node,1]  # y coordinate for node
            # circle coordinates
            x_1 = x_pos - self.node_size
            y_1 = y_pos - self.node_size
            x_2 = x_pos + self.node_size
            y_2 = y_pos + self.node_size
            # draw nodes
            self.canvas.create_oval(x_1, y_1, x_2, y_2, fill="white", activeoutline="gray",\
                                    tag="node_%d" %(node+1))
            #label nodes
            self.canvas.create_text(x_pos, y_pos, text=node+1, tag="tnode_%d" %(node+1))
        
        # if source and sink exist, change their color
        if self.graph.source != []:
            self.canvas.itemconfigure("node_%d" %(self.graph.source), fill=self.source_color)
        if self.graph.sink != []:
            self.canvas.itemconfigure("node_%d" %(self.graph.sink), fill=self.sink_color)
            
        # add legend over it
        text_label = "arc = ["
        if size(self.graph.c) != 0:
            text_label += "c, "
        if size(self.graph.u) != 0 and type != "r":
            text_label += "u, "
        elif size(self.graph.u) != 0 and type == "r":
            text_label += "r, "
        if size(self.graph.f) != 0 and type != "r":
            text_label += "f, "
        text_label += "]"
        self.canvas.create_text(40, 10, text=text_label)
        
        # add mode label
        if self.set_mode == "m":
            mode_text = "move"
        elif self.set_mode == "a":
            mode_text = "add"
        elif self.set_mode == "d":
            mode_text = "delete"
        self.canvas.create_text(750, 10, text="mode = %s" %(mode_text), tag="mode_state")
        # add external flow labels
        self.draw_external_labels()
        
        if m == 0:
            # skip the arc part if no arc exists
            return
        # draw arcs
        for arc in range(m):
            i = self.graph.A[arc,0]           # tail of arc
            j = self.graph.A[arc,1]           # head of arc
            x_1 = self.graph.coord[i-1,0]     # x_pos of i
            y_1 = self.graph.coord[i-1,1]     # y_pos of i
            x_2 = self.graph.coord[j-1,0]     # x_pos of j
            y_2 = self.graph.coord[j-1,1]     # y_pos of j
            # correct coordinates
            x_1, y_1, x_2, y_2 = self.get_arc_coord(x_1, y_1, x_2, y_2, type)
            
            # add arc line
            self.canvas.create_line(x_1, y_1, x_2, y_2, fill="black", arrow=arrow_type,\
                                    tag="arc_%d" %(arc))
            # add arc text
            line = self.get_arc_text(arc)
            self.canvas.create_text((x_1 + x_2) / 2, (y_1 + y_2) / 2, text=line,\
                                    tag="tarc_%d" %(arc))
        
        return
    
    def draw_tree(self, T):
        """ 
        highlight a tree T on the graph
        
        @type T: number vector
        @param T: tree
        
        @return: None  
        """
        # number of nodes
        n = self.graph.nodes()
        
        root = []
        # draw arcs
        for node in range(n):
            i = T[node]              # tail of arc
            if i == 0:
                root = node + 1
            elif i == inf:           # non connected nodes
                pass
            else:
                i = i                # tail of the arc
                j = node + 1         # head of arc
                pos = self.graph.get_arc_pos(i, j)
                # change arc line color
                self.canvas.itemconfigure("arc_%d" %(pos), fill="red")
        # change root color
        if root != []:
            self.canvas.itemconfigure("node_%d" %(root), outline="red")
            
        return
            
    def draw_path(self, P):
        """ 
        highlight a path P over the graph
        
        @type P: number vector
        @param P: path
        
        @return: None  
        """
        # get path
        p = size(P)
        
        # draw arcs
        i = P[0]                     # initialize tail
        for k in range(1, p):
            j = P[k]                 # head of arc
            pos = self.graph.get_arc_pos(i, j)
            # change arc line color
            self.canvas.itemconfigure("arc_%d" %(pos), fill="red")
            i = j
        
        # change start/end color
        self.canvas.itemconfigure("node_%d" %(P[0]), outline="red")
        self.canvas.itemconfigure("node_%d" %(P[p - 1]), outline="red")
        
        return
            
    def draw_coloring(self, C):
        """ 
        paint a coloring C over the graph
        
        @type C: number vector
        @param C: coloring
        
        @return: None  
        """
        # list of possible colors        
        color_list = ["white", "blue", "red", "green", "yellow", "gray75",\
                      "DarkMagenta", "Gold4", "navy", "cyan", "green4", "darkred", "black"]
        nc = size(color_list)
        
        # get coloring and graph data
        c = size(C)
        n = self.graph.nodes()
        
        # draw arcs
        for node in range(n):
            # calculate the rest of the division to wrap up the use of colors
            o_color = color_list[C[node]%nc]
            # change color
            self.canvas.itemconfigure("node_%d" %(node+1), fill=o_color)
            
        return
            
    def draw_arc_saturation(self):
        """ 
        paint the arcs according to the saturation of each arc
        
        @param: None
        @return: None
        """
        # number of arcs
        m = self.graph.arcs()
        
        # list of colors and arcs from empty to full + over
        color_list = ["gray", "green", "green", "blue", "blue", "red", "DarkMagenta"]
        width_list = [1, 1, 2, 1, 2, 2, 3]
        nl = size(color_list)
        
        if size(self.graph.f) == 0 or size(self.graph.u) == 0:
            print "could not draw arc saturations as no f or u vectors exist"
            return
        
        # set the color and width of each arc
        for arc in range(m):
            if self.graph.u[arc] == 0:
                sat_range = 1.0 * (nl - 2) * self.graph.f[arc]
            else:
                sat_range = 1.0 * (nl - 2) * self.graph.f[arc] / self.graph.u[arc]
            if sat_range > (nl - 2):
                sat_range = nl - 1
            sat_range = int(round(sat_range))
            self.canvas.itemconfigure("arc_%d" %(arc), fill=color_list[sat_range],\
                                      width=width_list[sat_range])
            
        return
    
    def draw_arc_flow(self):
        """ 
        paint the arcs according to the flow volume
        
        @param: None
        @return: None  
        """
        # number of arcs
        m = self.graph.arcs()
        
        # list of colors and arcs from empty to full + over
        color_list = ["gray", "green", "green", "blue", "blue", "red", "DarkMagenta"]
        width_list = [1, 1, 2, 1, 2, 2, 3]
        nl = size(color_list)
        
        if size(self.graph.f) == 0:
            print "could not draw arc flow as no f vector exists"
            return
        
        # set the color and width of each arc
        for arc in range(m):
            # maximum flow in the graph
            max_flow = max(self.graph.f)
            
            # if capacities exist also check them (to show overflow)
            if size(self.graph.u) != 0:
                max_cap = max(self.graph.u)
                max_flow = min(max_flow, max_cap)
                
            if max_flow == 0:
                flow_range = 1.0 * (nl - 2) * self.graph.f[arc]
            else:
                flow_range = 1.0 * (nl - 2) * self.graph.f[arc] / max_flow
                
            if flow_range > (nl - 2):
                flow_range = nl - 1
            
            flow_range = int(round(flow_range))
            self.canvas.itemconfigure("arc_%d" %(arc), fill=color_list[flow_range],\
                                      width=width_list[flow_range])
            
        return
    
    def draw_cut(self, S):
        """ 
        paint an s-t cut in the graph
        
        @type S: number vector
        @param S: vector with nodes in the S part of the s-t cut
        
        @return: None
        """
        # number of nodes
        n = self.graph.nodes()
        
        # set color of all nodes to S'
        for node in range(n):
            # change color
            self.canvas.itemconfigure("node_%d" %(node+1), fill="blue")
            
        # set color of nodes in S cut
        for i in S:
            # change color
            self.canvas.itemconfigure("node_%d" %(i), fill="red")
        
        return
                
    def draw_arc_set(self, set):
        """ 
        highlight a set of arcs in a graph
        
        @type set: number vector
        @param set: positions in A of arcs in the set
        
        @return: None
        """
        for arc in set:
            self.canvas.itemconfigure("arc_%d" %(arc), fill="red")
        
        return
    
    """
    Additional Drawing Functions
    """
    def draw_external_labels(self):
        """
        draw the external flows as labels over the nodes
        
        @param: None
        @return: None 
        """
        # number of nodes
        n = self.graph.nodes()
        
        if self.e_view:
            # draw labels
            for node in range(n):
                # x coordinate for node
                x_pos = self.graph.coord[node,0]
                # y coordinate for node
                y_pos = self.graph.coord[node,1]
                y_pos -= 1.5 * self.node_size
                #label nodes
                self.canvas.create_text(x_pos, y_pos, text=self.graph.B[node],\
                                        tag="enode_%d" %(node+1))
        else:
            # delete labels
            for node in range(n):
                #label nodes
                self.canvas.delete("enode_%d" %(node+1))
        
        return
    
    """
    Board/Graph Modification Functions
    """
    def change_graph_type(self, type):
        """
        change the graph type and re-draw
        
        @type type: char
        @param type: type of graph to set (check Graph Class)
        
        @return: None  
        """
        # change type
        self.graph.set_type(type)
        # draw the graph again
        self.draw_graph()
        
        return
    
    def external_flows_switch(self):
        """
        switch on and off the data of external flows
        
        @param: None
        @return: None 
        """
        self.e_view = bool(1 - self.e_view)
        self.draw_external_labels()
        
        return

"""
General Printing / Drawing Functions
"""
def graph_gui(G, modules):
    """
    Run Board GUI
    
    @type G: graph
    @param G: graph to start the board
    
    @type modules: list
    @param modules: list of modules to load on the GUI    
    """
    # create the master object
    master = Tk()
    
    # build the board basics on the master
    gui_mode = True                    # just draw once
    board = GraphBoard(master, G, gui_mode, modules)
    
    # user loop
    mainloop()
    
    return

def print_graph(G):
    """
    print the graph in text form (list of arcs and data)
    
    @type G: graph
    @param G: graph  
    """
    # check if it a valid Graph
    if not G.is_correct_type('dur'):
        return
    
    # print headers
    print 'Graph Information'
    if G.is_correct_type('du'):
        print '     arcs          c,    u'
    elif G.is_correct_type('r'):
        print '     arcs          c,    r'
    
    # scan each node and print all its adjacent arcs
    n = G.nodes()               # number of nodes
    for node in range(n):
        pos = G.N[node,0]       # initial position of data for N(node)
        
        # allow for iterations only if node information exists
        if pos == -1:
            link = 0
        else:
            link = 1                 # initialization of link variable
        # check all the adjacent arcs of 'node'
        while link != 0:
            i = G.A[pos,0]           # tail of the arc
            j = G.A[pos,1]           # head of the arc
            # if c exists, add it
            if size(G.c) != 0:
                c = '%.2f' % (G.c[pos])     # cost
            else:
                c = '  x  '
            
            # if u exists, add it
            if size(G.u) != 0:
                u = '%.2f' % (G.u[pos])     # capacity/residual cap
            else:
                u = '  x  '
            
            # print the arc if it has capacity or no capacity is defined
            if u == '  x  ' or u > 0:
                print 'arc ',int(i),'->',int(j),': (%s, %s)' % (c,u)
                
            link = G.A[pos,2]
            pos = link           # get the next position
    
    print(" ")
    return
    
def draw_graph(*args):
    """
    draw the graph in a simple board and add over it a structure
    (like tree, path, cycle, etc.) if needed
    
    @type G: graph
    @param G: graph
    
    @note: the following parameters are optional and should be set
           in pairs ["type", structure]
    
    @type type: string
    @param type: type of structure: "tree", "path", "coloring", "cut"
                                    "saturation"
    
    @type structure: vector
    @param structure: structure to add over the graph
    
    @type style: string
    @param style: drawing style: "one-shot", "permanent", "append", "write"
    """
    #default style
    style = "one-shot"
    # initialize structures
    structure = []
    type = []
    
    # get the graph
    G = args[0]
    
    # create the master object
    master = Tk()

    # build the board basics on the master
    gui_mode = False                    # just draw once
    board = GraphBoard(master, G, gui_mode, None)
    
    # add all other structures
    st = size(args)
    for k in range(1, st):
        layer = args[k]
        type = layer[0]
        structure = layer[1]
    
        # add tree, path, coloring, etc.
        if type == "tree":
            # if a tree was added, draw it too
            board.draw_tree(structure)
        elif type == "path":
            board.draw_path(structure)
        elif type == "coloring":
            board.draw_coloring(structure)
        elif type == "cut":
            board.draw_cut(structure)
        elif type == "saturation":
            board.draw_arc_saturation()
        elif type == "arc_set":
            board.draw_arc_set(structure)
        elif type == "style":
            # indicate drawing style
            style = layer[1]
            if style == "append" or style == "write":
                # if it is append, add the file name
                file_name = layer[2]
    
    # user loop
    if style == "permanent":
        mainloop()
    # in append mode, add the graph to the step file
    elif style == "append" or style == "write":
        # make sure the graph is printed
        board.master.update_idletasks()
        # append it to a file and close the board
        board.export_draw(file_name, style[0])
        master.destroy()
    # otherwise kill the window
    else:
        master.destroy()
    
    return