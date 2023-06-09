
Introduction to Artificial Intelligence - maman 11

Name: Ofek Yaari


Questions 1-4:
-------------- 
    It is required to build a graph search algorithm 
     which is compatible with the DFS, BFS, UCS and A* search algorithms
     except for the way the frontier is managed.

    I implemented a search function named dataStructureSearch
     that performs the graph search according to the data structure it received.
    For each search algorithm, we send to dataStructureSearch the 
     data structure type which the search algorithm is managed by.


    Question 1:
    -----------
        The DFS algorithm guarantees us finding a valid path that reaches a goal state.
        The order of investigation is random and difficult to predict.
        Pacman goes to the goal state only according to the selected route 
         and does not go through all the explored squares.

        DFS does not necessarily return the shortest path. 
        It is built in such a way that it moves randomly from state to state until 
         it gets stuck and then returns to a state where it has some move to make. 
        With this method, he may reach a goal state when he goes through a route that
         is not optimal.
 
 
    Question 2:
    -----------
        BFS finds the optimal solution. 
        This is because it guarantees that the path from the starting state to each of 
         the states is the least-cost path in the graph.
 
 
    Question 4:
    -----------
        | Search Algorithm | Path found with total cost | Search nodes expanded | Score |
        |------------------|----------------------------|-----------------------|-------|
        |       DFS        |            298             |           576         |  212  |
        |       BFS        |            54              |           682         |  456  |
        |       UCS        |            54              |           682         |  456  |
        |        A*        |            54              |           682         |  456  |
        |   A*, Manhattan  |            54              |           535         |  456  |
        |-------------------------------------------------------------------------------|

        We can conclude from the table that: 
            DFS does develop a relatively low number of nodes but it is not optimal in its cost
             and therefore its score is also not optimal.
 
            BFS, UCS and A* (without heuristic function) behave identically
             because the weight function is the same, so there is no advantage to using UCS or A*. 
            Therefore, they develop a large (identical) number of nodes,
             but the resulting cost is optimal and therefore its score is also not optimal.
 
            A* using the ManhattanHeuristic, develop a minimum number of cheapest nodes and therefore  
             the resulting cost is optimal and the score is also optimal.
 

Question 5:
-----------
    We will represent each state using the initial state and the location of the 4 corners.
    To return the successor states from current state, we check all possible directions of movement,
     if none of them is a wall, then we check if the state is a corner.
    If the state is a corner then the state is returned after adding the corner. 
 
 
Question 6:
-----------
    We know that there are 4 corners.
    I implemented the heuristic function as the Manhattan distance from the nearest corner.
    Therefore A* will prefer a route that brings us closer to a corner.


Question 7:
-----------
    I implemented thr heuristic function as the distance to the furthest food.
    The distance is the actual maze distance that calculated by the given function mazeDistance.
    Therefore, A* will prefer a route that brings us closer to the farthest food from the starting point.


Question 8:
-----------
    I added to Class AnyFoodSearchProblem the test whether a state is a target state.
    To make the agent greedily eat the nearest point, we will use the BFS implementation.
