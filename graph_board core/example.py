"""
Example File v.1.0

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
from numpy import *                  # matrix manipulation
# personal modules and classes
from GraphClass import *             # Graph classes
from graph_board import *            # Graph Printing & Drawing

if __name__ == '__main__':
    # graph definition
    G = Graph()
    
    # build graph from data file
    G.form_graph_from_file("graph3.txt")
    # load previously saved file
    #G.form_graph_from_file("draw_tmp.txt")

    # add algorithm libraries here
    #modules = ["search_order", "spanning_trees", "shortest_path",\
    #           "coloring", "max_flow", "min_cut", "min_cost_flow"]
    modules = []
    graph_gui(G, modules)
