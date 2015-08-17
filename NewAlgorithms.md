# Introduction #

The graph board was designed with the possibility of adding new algorithms easily, without need of going under the hood of the graph board itself. In order to do this there are simple instructions you need to add to your algorithm that allow the board to load it as part of the menu.

Here we detail what are the required steps to add your algorithm(s) to the board and what tools are available from the graph and board classes that can help you improve the visualization of the results.


# Creating Your Library #

If you want to build your own library with new algorithms, the best way to start is to check the currently available libraries. The current version of the library package comes with several of them and on each you have multiple algorithms.

Also read the GraphClass and BoardClass sections as those can give you some ideas on the modifiers that already exist to work on the Graph class, and that could help you in the implementation of your algorithm.

The most important part is that, if you finally create a new algorithm please share it so that more people can use it on this program. You can send it to me and I'll be pleased to add it to the library package zip and of course add you to the collaborator's list.

# Adding Your Library #

Once you have created your set of algorithms, you need to do a couple of steps in order to be able to import your library to the GUI.

The first thing is that you need to do is a mapping function for each algorithm in your library. Check the current libraries to see some examples, they are all at the end of the library file.

What this mapping functions do is use your algorithm and apply it to a graph, printing on the screen important information such as the results, maybe the time taken (to compare algorithms) and possibly draw your solution over the current graph. The BoardClass accepts some data structures you can add over the graph in the GUI such as paths, trees, or colourings, and that can help you show the result of the algorithm.

The second thin you need to do is create the menu for the GUI. As an example here is the menu created for the Min Cut algorithm library:
```
def menu_items():
    """ 
    returns the list of algorithms available for populating the GUI menu
    
    @param: None
    
    @rtype: list
    @return: list of algorithms and menu to add to the GUI 
    """
    menu_name = "Min Cut"
    algorithm_list = [["Min Cut from Max Flow", board_min_cut_from_mf],
                      ["separator", "separator"],
                      ["Global Min Cut by n Max Flow", board_global_min_cut]]
    
    return [menu_name, algorithm_list]
```

The function should always be called `menu_items()` and have these two vectors: `menu_name`, which is the name you will see in the GUI, and `algorithm_list` which will add the list of algorithms to the GUI.
As you can see in the example the algorithm list consists on several two element vectors. The first element is the name that you will see in the GUI and the second one is the name of the function to call when you want to run the algorithm. In general this last one should be the different mapping functions you created previously.
To make things easier, I also added a "separator" option, as shown in the example. If both elements of the vector contain "separator" a line separator will be added to the pop-up menu in the GUI.

Once you have done this, as you see on the Getting Started page, you just need to add the name of your library file to the `modules` vector before you call the GUI. For example if you created a set of algorithms in a file `new_algorithms.py` you can run the GUI with just your library by doing the following:
```
    modules = ["new_algorithms"]
    graph_gui(G, modules)
```

Last but not least, don't forget to add comments to your code so other people can read it.