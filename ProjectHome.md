### What's New? ###
Finally the Project Wiki is finished! All the information on how to use the classes and the code has been added. Check it out to see some of the cool functionalities of the program.

First revision, Graph Board v.1.01 is now available.

### Overview ###
The main objective of **graph\_board** is to build a library for visualizing and working with graphs, that can help prototyping and testing graph theory related algorithms and that can also be used with educational purposes.

The library has two main components, a **Graph** class, that provides the structure to store and work with graphs, and a **Graph Board** class, to visualize the graphs and highlight certain properties (like cycles, paths, etc.).

Additionally, the idea is to also start building a library of graph/network algorithms.

**graph\_board** is being developed in Pythion 2.6.2 using Tkinter as graphic module, and has only been tested in Windows Vista.


---

### Dependencies ###
You need to have [numpy](http://numpy.scipy.org/) installed in order to run this program


---

### Current Graph Board Features ###

  * Graph() class supports directed and undirected graphs, plus residual graphs for network flow problems.
  * GUI interface to move and manipulate graphs including adding/deleting nodes and arcs; set external flows per node; set capacities, costs and flows per arc.
  * GUI interface also allows to load external algorithm libraries.
  * Save graphs in text format
  * Export graphs in .ps format, including multiple pages .ps to show the steps of an algorithm

### Current Implemented Algorithms ###

  * **Search/Sort methods**: breath first search, depth first search and topological sorting.
  * **Minimum Spanning trees**: Kruskal's and Prim's algorithms.
  * **Colouring**: brute force exact colouring and also approximate colouring methods (greedy, tabu-saerch and tabu-precoloring search).
  * **Shortest Path**: DAG algorithm, Dijkstra's algorithm, Fifo-Labelling algorithm.
  * **Max Flow**: augmenting path and labelling algorithms.
  * **Min Cut**: simple min cut and global min cut algorithms.
  * **Min Cost Flow**: negative cycle cancelling and successive shortest path algorithms.


---

Give it a try and any feedback is appreciated. Have fun!

rax