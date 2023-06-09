# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

PACMAN_AGENT = 0
POSITIVE_INFINITY = float('+inf')
NEGATIVE_INFINITY = float('-inf')
STOP = ('stop')

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
       # print('legalmoves: ',legalMoves)
       # print('scores: ',scores)
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
     #   print('evaluationFunction:')
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        if not newFood.count(): #If there is no more food then we finish.
            return 0

        for ghostState in newGhostStates:

            if  newPos == ghostState.getPosition(): # If there is a ghost on the next state

                if ghostState.scaredTimer:
                    return POSITIVE_INFINITY

                return NEGATIVE_INFINITY


        if newFood.count() != currentGameState.getFood().count(): # if we get food in this move
            return POSITIVE_INFINITY

        newFood = newFood.asList()
        foodDistance = []
        for food in newFood:
            def res(food): return manhattanDistance(newPos,food)
            foodDistance.append(res(food))

        score = (-1 * min(foodDistance))

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        agent = PACMAN_AGENT

        action = self.minMax_value(gameState, depth, agent)
        return action[1]

    def minMax_value(self, state, depth, agent):

        if depth == self.depth or not state.getLegalActions(agent):
            return self.evaluationFunction(state), None

        minimax_lst = self.minMax_lst(state, depth, agent)

        #if agent is PACMAN_AGENT --> pacman turn (max player)
        #else --> ghost turn (min player)
        return (max if agent is PACMAN_AGENT else min)(minimax_lst)


    def minMax_lst(self, state, depth, agent):

        actions = state.getLegalActions(agent)
        next_agent = (agent + 1) % state.getNumAgents()
        depth += 1 if next_agent is PACMAN_AGENT else 0
        next_states = [(state.generateSuccessor(agent, action), action) for action in actions]
        return [(self.minMax_value(state, depth, next_agent)[0], action) for state, action in next_states]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        "*** YOUR CODE HERE ***"
        depth = 0
        agent = PACMAN_AGENT
        alpha = NEGATIVE_INFINITY
        beta = POSITIVE_INFINITY

        action = self.miniMax_value(gameState, depth, agent, alpha, beta)
        return action[1]

    def miniMax_value(self, state, depth, agent, alpha, beta):

        if depth == self.depth or not state.getLegalActions(agent):
            return self.evaluationFunction(state), STOP

        actions = state.getLegalActions(agent)
        next_agent = (agent + 1) % state.getNumAgents()

        depth += 1 if next_agent is PACMAN_AGENT else 0

        bestMove = [NEGATIVE_INFINITY, STOP] if agent is PACMAN_AGENT else [POSITIVE_INFINITY, STOP]

        for action in actions:
            succesor = state.generateSuccessor(agent, action)
            currentMove = [self.miniMax_value(succesor, depth, next_agent, alpha, beta)[0], action]
            if agent is PACMAN_AGENT:
                bestMove = max(bestMove, currentMove)
                alpha = max(alpha, bestMove[0])

            else:
                bestMove = min(bestMove, currentMove)
                beta = min(beta, bestMove[0])

            if alpha > beta:  # Prune the branch

                break

        return bestMove


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        agent = PACMAN_AGENT

        action = self.minMax_value(gameState, depth, agent)
        return action[1]

    def minMax_value(self, state, depth, agent):

        if depth == self.depth or not state.getLegalActions(agent):
            return self.evaluationFunction(state), STOP

        minmax_lst = MinimaxAgent.minMax_lst(self, state, depth, agent)

        return (max if agent is PACMAN_AGENT else average)(minmax_lst)

def average(lst):
    sum_minmax_lst = sum(value for value,action in lst)
    avg = (sum_minmax_lst / len(lst)), STOP
    return avg


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


def betterEvaluationFunction(currentGameState):
    """
   Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
   evaluation function (question 5).

   DESCRIPTION: <write something here so we know what you did>
     """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newScore = currentGameState.getScore()

    newFood = newFood.asList()
    newFood_len = len(newFood) + 1
    foodDistance = 1
    foodDistances = []
    ghostScore = 0

    if newFood:
        score = 0
        for food in newFood:
            def res(food): return manhattanDistance(newPos, food)
            foodDistances.append(res(food))
    else:
        score = 100000


    if newGhostStates:
        for ghostState in newGhostStates:

            def res(ghostState): return manhattanDistance(newPos, ghostState.getPosition())
            ghostDistance = res(ghostState)

            if not ghostState.scaredTimer and not ghostDistance:
                ghostScore -= 1

            elif ghostState.scaredTimer < ghostDistance:
                ghostScore += 1 / ghostDistance


    foodDistance += sum(val for val in foodDistances)

    if newScaredTimes[0]:
        ghostScore += 100

    scores = [ghostScore, newScore, (1 / newFood_len), (1 / foodDistance)]
    score += sum(val for val in scores)

    return score


# Abbreviation
better = betterEvaluationFunction