# Introduction #

The graph board class allows the visualization and modification of the loaded graph. The [Getting Started](http://code.google.com/p/graph-board/wiki/GettingStarted) section has a summary of the main functions of the menu.

Here we give a small overview of the functions and modifiers available in the board and in the `graph_board.py` file that can be used afterwords for visualizing algorithms.


# Loading and Playing on the GUI #

In order to run the GUI you need two things before calling the GUI function. The first one is to create a graph and load it with data (at least one node is required). This is done by defining a graph variable and using the `form_graph_from_file` modifier to load data from a text file. Check the Graph Class page and the text examples in the zip file to see how these files are made. It is fairly straight forward.
```
    # graph definition
    G = Graph()
    
    # build graph from data file
    G.form_graph_from_file("example1.txt")
```

The second thing you need is the module selection. As you can see on the New Algorithms section of this wiki, you need to define a variable `modules` with all the modules you want to load to the GUI, or at least set it as an empty array if you don't want to load any libraries:
```
    modules = ["search_order", "spanning_trees", "shortest_path",\
               "coloring", "max_flow", "min_cut", "min_cost_flow"]
```

Finally, once you have this you run the GUI by just calling the command `graph_gui`:
```
    graph_gui(G, modules)
```

Once you do this you will see a window similar to the following one:
![http://sites.google.com/site/rodrigocarrasco/config/app/images/example_output.jpg](http://sites.google.com/site/rodrigocarrasco/config/app/images/example_output.jpg)

In the Getting Started page we already went through the available menus, so here we will focus on what you can do on the board. There are three main modes on the board, which are selected with the keyboard: `m` for move, `a` for add, and `d` for delete. Once you press any of these three keys you will see a message on the command window and the text indicator on the top right side of the board will also change.

  * **Moving Nodes**: you can move the nodes around using the right mouse button. First press the `m` key to make sure we are in "movement mode" and then just click a node and drag it to any position you want. The arcs are attached to the node so they will update by themselves.

  * **Adding Nodes**: nodes can me added in any of the three modes. Just press the left mouse button and a new unconnected node will appear.

  * **Adding Arcs**: press `a` to go to "add mode" and you will be able to add arcs. Right click and drag, just like you did when you wanted to mode the node and a new arc will appear. The new arc will be blue and it will change to black once you release the right button over the other node you want to connect. Arcs will always be created from tail to head.

  * **Deleting Nodes and Arcs**: press `d` to change to "delete mode" and then double click either a node or an arc. Immediately it will be deleted. Currently no undo option is available so be careful. If you delete an arc, all the associated information like cost and capacity will also be eliminated. In the case of deleting a node, the node will disappear together with all the adjacent arcs to that node.

  * **Setting Sources and Sinks**: while in add or move modes, a double click on a node will set that node as a source, and change its colour to green. A double click over it again will eliminate the source. Once a source is selected, a double click on another node will define the sink and change the node to green. If you want to eliminate the sink you need to double click it again.

  * **Setting Arc Parameters**: while in "move mode" double click an arc and you will see a message on the command window, asking you to input data. Depending on what data you can enter, it will sequentially ask you to add cost, capacity, and flow.

  * **Setting External Flows**: while in "move mode" and with the "Show External Flows" option selected (you can find it in the "Graph Tools" menu), you will see a number above each node. That is the external flow. Double click it and the command window will ask you to enter the value of the external flow for that node.

# Main Modifiers and Functions #

As with the GraphClass, the BoardClass has several modifiers. In general, unless you want for some reason to overhaul the board itself you will not need to use or change any of them. In any case, they are all commented and explained in the `graph_board.py` file, or you can use the `help(GraphBoard())` command to get a summary of them.

The really important functions in this file are the ones that allow you to visualize algorithm results over the graph in the board. The next section explains these functions and how to use them.

# Visualization Options #

On top of the graph you draw in the canvas, the Graph Board allows to highlight or represent several structures in the graph, making it easier to show them. Once you run the GUI command, a `board` variable will be created which will contain the board and the graph. Now from your algorithm you can call some of the modifiers of `board` in order to draw or highlight certain structures. If you need any detail on the available structures check the list of structures at the end of the GraphClass page.

The following is the list of the current implemented modifiers:

  * `board.draw_graph()`: will clean a re-draw the graph on the board.
  * `board.draw_tree(T)`: will draw the tree structure **T** in red over the graph
  * `board.draw_path(P)`: will draw the path structure **P** in red over the graph
  * `board.draw_coloring(C)`: will colour each node according to the colouring vector **C**. This vector has numbers from 0 to 13 and each represents a different colour. The list of colours is the following: `["white", "blue", "red", "green", "yellow", "gray75", "DarkMagenta", "Gold4", "navy", "cyan", "green4", "darkred", "black"]`
  * `board.draw_arc_saturation()`: this will paint every arc according to the amount of flow in them. If the arc colour and thickness of the line will depend on how saturated the arc is, in 7 different levels: gray, green thin, green thick, blue thin, blue thick, red thick, and magenta extra-thick. This last one corresponds to an arc having a flow above the capacity of the arc.
  * `board.draw_arc_flow()`: this is very similar to the saturation drawing, with the difference that now the colour and thickness will depend on the amount of volume with respect to all the arcs in the graph. The arc with the highest volume will be red, and from there downwards using the same scale as the previous drawing method.
  * `board.draw_cut(S)`: this will paint in blue all the nodes contained in the cut vector **S** and it will paint in red the rest of the nodes.
  * `board.draw_arc_set(AR)`: this will paint in red all the arcs contained in the list **AR**. This is a list of the position of each arc in the adjacency matrix **A**.

How to call them?
This is easy. For example let's say that you just programmed an algorithm that defines some sort of cut **S**. What you will do at the end of your algorithm is add the lines `board.draw_graph()` to reset the board and draw a clean graph, and then `board.draw_cut(S)` where **S** is the output of your algorithm. This will highlight your cut output over the graph previously drawn.

You can try all these functions by using the algorithms provided in the algorithm library. Check the code if you like to see how they are used.

# Step Visualization #

One additional cool feature of this program is that it allows you to show the steps given by your algorithm. Imagine you are trying a Cycle Cancelling Algorithm to fin a minimum cost flow. If you just run the algorithm you will get your final solution, but it will be very helpful for classes and demonstrations to show the intermediate steps. In order to do so you can use the `draw_graph` function that comes in the `graph_board.py` file. This will create a multi-page .ps file where you have each step of your algorithm in one page.

How to use it? Check the `min_cost_flow.py` library for an example.

You would first call:
```
    draw_graph(G, ["style", "write", "name.ps"])
```

This will create a file "name.ps", with the initial graph **G**.
After the first iteration you would like to add a page with the first step taken, then you add:
```
    draw_graph(G, ["style", "append", "name.ps"], ["path", nc_path])
```

Instead of "write" we now have "append", which adds a new page with the drawing, and the second structure indicates that over the graph it must add a "path" contained in the variable `nc_path`. Check the function code as you can add several additional pairs of parameters to draw additional thins like trees and colourings. For example the following code will append to the previous file the same drawing as before but with an additional colouring **C** over it:
```
    draw_graph(G, ["style", "append", "name.ps"], ["path", nc_path], ["coloring", C])
```

This allows for a very flexible way of showing intermediate steps that can help you illustrate how your algorithm works and build some examples.