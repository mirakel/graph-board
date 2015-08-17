# Introduction #

The graph class is the basic structure for working in graph board. These are later loaded to the board for further work or modification.

Here we give a small view of how the class is built and what modifiers are currently available. You can check the class help to see all of them in detail (just use `help(Graph())` to get the list)

It is important to note that the nodes of the graph are numbered from 1 onwards, whereas the matrices and vectors in numpy are indexed from 0 onwards. This implies that there is a   one element shift in some of the indices indicated below, and you must be careful in case you want to do any changes to the code.

# Graph Construction #

A Graph() object contains several different variables:
  * **type**: it is a char that defines the type of graph. Currently three types of graphs are available: _d_, directed; _u_, undirected; _r_, residual.
  * **A**: The most important one is the matrix **A**, which is an adjacency list of the arcs in the graph. Every row _i_ of **A** is a 3 element vector _[i, j, link]_, where _i_ is the tail of the arc, _j_ the head, and _link_ is the row value of the next arc going out from node _i_.
  * **N**: it is an index matrix that on each row _i-1_ has a two element vector _[en](st.md)_, where _st_ is the row in **A** where the first element of the adjacency list of node _i_ is, and _en_ is its last. This allows to check and update easily the adjacency list of each node.
  * **B**: this is a column vector where element _i-1_ contains the external flow or node label of node _i_. If no flows or labels are used in you algorithm, you can use this to store other data related to each node. In the case of external flows, numbers >0 imply the node is a source and <0 a sink.
  * **names**: not currently used. Element _i-1_ will have a string with a name assigned to node _i_.
  * **c**, **u**, and **f**: these three vectors have at position _pos_ some of the characteristics of arc _pos_. _c_ has the cost of the arc, _u_ the capacity, and _f_ the flow.
  * **coord**: each row _i-1_ contains a two dimensional vector with the _(x,y)_ position of node _i_ on the graph board.
  * **source** and **sink**: the number of the source and sink nodes respectively.
  * **mirror**: used mainly for residual graphs. It is a vector that on row _pos_ has the position of the "mirror" arc in the graph.

# Main Modifiers #

Please check the GraphClass.py file to see all the modifiers for the Graph() class or type `help(Graph())` so see a summary.

In the following description we will assume that we have a variable **G** that has stored a graph (which can be easily created by `G = Graph()`).

Many modifiers were implemented to allow for flexibility and control over the graph. Here is a short summary of the most important ones:
  * `G.nodes()` and `G.arcs()`: return the number of nodes or arcs respectively
  * `G.set_type(type)`: sets one of the valid graph types
  * `G.add_node()`: adds a disconnected node to the graph
  * `G.add_arc(i,j)`: adds an arc from node _i_ to node _j_
  * `G.del_arc(i,j)`: deletes an arc from node _i_ to node _j_ if exists
  * `G.del_node(i)`: deletes node _i_ if exists
  * `G.form_graph_from_file(file_name)`: loads the data of a text file as graph data. Check any of the example text files to see how they are stored.
  * `G.save_graph_to_file(file_name)`: saves the current graph into a text file
  * `G.get_adjacent_nodes(i)`: gives a list with all the nodes that are adjacent to node _i_
  * `G.residual_graph()`: builds the residual graph of _G_

  * `G.is_top_sort()`: determines if the graph is in topological order
  * `G.is_coloring(C)`: checks if _C_ is a stable colouring for the graph (where _C_ is a vector that has on each position _i-1_ the colour number assigned to node _i_

  * `G.total_tree_cost(T)`: give the total cost of a tree structure _T_ on the graph
Still there are many others that allow random graph creation (with or without random data added to them), add or remove data from the graph, find arc positions in the adjacency matrix, find adjacent arcs, swap arc direction, etc.

# Other Structures #

As you will see on the modifier functions, there are several other types of structures that certain modifiers understand. The most important ones are:
  * **T** tree: it is a vector that represents a tree on the graph. On position _i-1_ has the number of the parent node of node _i_ or a 0 if it has no parent. Vector **T** must have the same size as the number of nodes.
  * **P** path: is a vector that lists a path of nodes. The vector can have any length and it contains the sequence from start to end of the path.
  * **C** colouring: is a vector with the same number of elements as nodes in the graph, where on element _i-1_ has stored a number equivalent to the colour of node _i_. Check the BoardClass to see what colours are available.
  * **AR** set of arcs: is a vector with a list of positions of arcs in **A** to which we want to do something. It doesn't require any special size nor any special order.
  * **S** cut: it is a vector that contains the number of the nodes that are on the _S_ side of the cut. Clearly **S** needs to be smaller or equal than the number of nodes in _G_