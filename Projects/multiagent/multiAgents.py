from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        resFood = 1 / (
            min([manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()])) if newFood.asList() else 0

        ghostDist = []
        for i in range(len(newGhostStates)):
            dist = manhattanDistance(newPos, newGhostStates[i].getPosition()) + newScaredTimes[i]
            reciprocal = 1 / dist if dist != 0 else 0
            ghostDist.append(reciprocal)
        resGhost = max(ghostDist)

        return resFood - resGhost + successorGameState.getScore()
        # return successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, self.depth) for action in legalMoves]
        return legalMoves[scores.index(max(scores))]

    # return minimax value of the given state
    def value(self, currentGameState, agentIndex, depth):
        if depth == 0 or currentGameState.isWin() or currentGameState.isLose():
            return self.evaluationFunction(currentGameState)

        newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
        depth -= (newIndex == 0)  # if next layer is Pacman, depth decreases by 1
        legalMoves = currentGameState.getLegalActions(agentIndex)
        scores = [self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth) for action in
                  legalMoves]
        result = max(scores) if agentIndex == 0 else min(scores)  # minimax
        return result


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions()
        v = alpha = -999999999
        beta = 999999999
        result = legalMoves[0]
        for action in legalMoves:
            currV = self.value(gameState.generateSuccessor(0, action), 1, self.depth, alpha, beta)
            if currV > v:
                result = action
                v = currV
            alpha = max(alpha, v)
        return result

    # return minimax value of the given state with alpha-beta pruning
    def value(self, currentGameState, agentIndex, depth, alpha, beta):
        if depth == 0 or currentGameState.isWin() or currentGameState.isLose():
            return self.evaluationFunction(currentGameState)

        legalMoves = currentGameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            v = -999999999
            for action in legalMoves:
                v = max(v, self.value(currentGameState.generateSuccessor(0, action), 1, depth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v
        else:
            v = 999999999
            newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
            depth -= (newIndex == 0)
            for action in legalMoves:
                v = min(v, self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth, alpha,
                                      beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v


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
        legalMoves = gameState.getLegalActions()
        scores = [self.value(gameState.generateSuccessor(0, action), 1, self.depth) for action in legalMoves]
        return legalMoves[scores.index(max(scores))]

    # return minimax value of the given state
    def value(self, currentGameState, agentIndex, depth):
        if depth == 0 or currentGameState.isWin() or currentGameState.isLose():
            return self.evaluationFunction(currentGameState)

        legalMoves = currentGameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            scores = [self.value(currentGameState.generateSuccessor(0, action), 1, depth) for action in legalMoves]
            return max(scores)
        else:
            newIndex = (agentIndex + 1) % currentGameState.getNumAgents()
            depth -= (newIndex == 0)  # if next layer is Pacman, depth decreases by 1
            scores = [self.value(currentGameState.generateSuccessor(agentIndex, action), newIndex, depth) for action in
                      legalMoves]
            return sum(scores) / len(legalMoves)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    A = the reciprocal of the manhattan distance to the closet food
    B = the reciprocal of the maximum sum of the manhattan distance to the ghost and its scared time
    C = the currentGameState score
    value = A - 1 * B + C
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    resFood = 1 / min([manhattanDistance(pos, food) for food in foods.asList()]) if foods.asList() else 0

    ghostDist = []
    for i in range(len(ghostStates)):
        dist = manhattanDistance(pos, ghostStates[i].getPosition()) + scaredTimes[i]
        reciprocal = 1 / dist if dist != 0 else 0
        ghostDist.append(reciprocal)
    resGhost = max(ghostDist)

    # print(resFood, resGhost, currentGameState.getScore())
    return resFood - 10 * resGhost + currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction
