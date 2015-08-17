# Installation #

Before you can use graph-board, you need to make sure that you have both [python](http://www.python.org/) and [numpy](http://numpy.scipy.org/) installed in your system.

For the moment graph-board doesn't have an setup program, so you need to either manually move the files to your program folder or to the python folder, whichever you prefer, and run it from there.


### Example ###

The example.py file, included in the main .zip file, has a simple example on how to run the program's GUI, loading a graph stored in the graph3.txt file, but without loading any of the libraries.

```
    # graph definition
    G = Graph()
    
    # build graph from data file
    G.form_graph_from_file("graph3.txt")

    # add algorithm libraries here
    modules = []
    graph_gui(G, modules)
```

Run this example to start the GUI and play around with the loaded graph. You should see a similar window to this one:

![http://sites.google.com/site/rodrigocarrasco/config/app/images/example_output.jpg](http://sites.google.com/site/rodrigocarrasco/config/app/images/example_output.jpg)

# Using Graph Board #

The basic GUI window consists of just 2 menus: **File** and **Graph Tools**
### File ###
  * **Quit**

### Graph Tools ###
  * **Export**: export the current graph to the file graph.ps.
  * **Clean**: eliminate all highlighting elements in the graph (just leave the nodes and arcs).
  * **Show External Flows**: toggle between showing and hiding the external flow labels on each node.
  * **Flow Views**: select one of the current two modes of viewing flows: saturation or volume.

  * **Re-position Nodes**: **DRAFT** automatically re-position the nodes in the canvas in a "better" way. When you select this option, the program simulates a dynamic model, where the graph is assumed to be floating on a flat surface, with a positive charge given to each node (and the borders, so the graph is repelled from the borders). On the other hand each arc is simulated as an elastic or spring connecting the nodes. The model is then simulates until the graph "converges" to its new position. Try it out!

  * **Graph Types**: set the graph to directed or undirected.
  * **New Random Graph**: create a new graph, and add random costs and capacities to the arcs. The user is asked to input the number of nodes and arcs for the new graph, as well as the min/max costs and max capacity of each arc.
  * **Remove Parameters**: Eliminate the costs, capacities, flow or external flow from the graph.

### Right Toolbar ###

Currently the right-hand side toolbar only has the **Export**, **Clean**, and **Quit** buttons implemented, replicating functions from the main menu.

### The Canvas ###

You can do several actions over the graph in the canvas using the mouse, such as move nodes, add nodes and arcs, change arc weights, etc. Check the BoardClass page to see what things you can do.

# Loading New Algorithms #

The GUI allows you to add new algorithms to use with the graph in the canvas. To do so, first add the algorithm library to the same folder as your program and then you just need to add the name of the python file with the algorithm to the `module` variable before running the GUI. E.g.:

```
    # add algorithm libraries here
    modules = ["search_order", "spanning_trees", "shortest_path"]
    graph_gui(G, modules)
```

This example loads all the algorithms from the **serach\_order**, **spanning\_trees**, and **shortest\_path** libraries, leaving them as part of the menu. The [Adding New Algorithms](http://code.google.com/p/graph-board/wiki/NewAlgorithms) page has more details on how to add your own algorithms to the board