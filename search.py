# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

#####################################################
# Question_1-4
#####################################################
def dataStructureSearch(problem, frontier, heuristic = nullHeuristic):
    """
    Algorithm to graph search.
    Can be used for DFS, BFS, UCS and A* algorithm,
    depending the frontier type that passed.
    """

    # node format is (state, moves, cost)
    node = problem.getStartState()  # get the start state for the search problem.
    path = []
    cost = heuristic(node, problem)
    frontier.push((node, path, cost))
    explored = set()

    while not frontier.isEmpty():

        state, actions, cost = frontier.pop()
        if state not in explored:
            explored.add(state)

            if problem.isGoalState(state):
                return actions

            else:
                successors = problem.getSuccessors(state)
                for nextState, nextAction, nextCost in successors:
                    child = nextState
                    child_path = actions + [nextAction]
                    child_cost = cost + nextCost
                    frontier.push((child, child_path, child_cost))

    return []

#####################################################
# Question_1
#####################################################
def depthFirstSearch(problem):
    """ Search the deepest nodes in the search tree first. """

    return dataStructureSearch(problem, frontier = util.Stack())

#####################################################
# Question_2
#####################################################
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    return dataStructureSearch(problem, frontier = util.Queue())

#####################################################
# Question_3
#####################################################
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    """ Creating a new Priority Queue where the priority is the cost of the route
        to state n from the start state, 
        known as: g(n) """

    # g(n) = node[-1] --> The cost of getting to the current state from the starting state.
    priority_queue_by_cost = util.PriorityQueueWithFunction(lambda node: node[-1])

    return dataStructureSearch(problem, frontier = priority_queue_by_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#####################################################
# Question_4
#####################################################
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """ Creating a new Priority Queue where the priority is The estimated cost of
        a route from the start state to a goal state passing through node n,
        known as: f(n) = g(n) + h(n) """

    # g(n) = node[-1] --> The cost of getting to the current state from the starting state.
    # h(n) = heuristic(node[0],problem) --> The estimated cost of the cheapest route from state n to a goal state.
    priority_queue_by_cost = util.PriorityQueueWithFunction(lambda node: node[-1] + heuristic(node[0], problem))

    return dataStructureSearch(problem, frontier = priority_queue_by_cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
