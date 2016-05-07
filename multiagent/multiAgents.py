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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    def __init__(self):
        self.hasgone=[]
        self.z=(0,0)




    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        waytovec = {'North':(0,1), 'South':(0,-1), 'East':(1,0), 'West':(-1,0), 'Stop':(0,0)}
        self.hasgone.append(waytovec[legalMoves[chosenIndex]])
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
        newFood = list(successorGameState.getFood())
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        direc = [(0,0), (0,1), (0,-1), (1,0), (-1, 0)]
        ghostpos = [i.getPosition() for i in newGhostStates]
        dangerzone = [(x+i, y+j) for (x, y) in ghostpos for (i,j) in direc]
        x=100000000
        Food = list(currentGameState.getFood())
        if not Food[self.z[0]][self.z[1]]:
            for i in range(len(Food)):
                for j in range(len(Food[0])):
                    if Food[i][j]:
                        if manhattanDistance(newPos, (i,j))<x:
                            self.z=(i,j)
                            x=manhattanDistance(newPos, self.z)
        fooddirec=[]
        if newPos[0]>self.z[0]:
            fooddirec.append("West")
        if newPos[0]<self.z[0]:
            fooddirec.append("East")
        if newPos[1]>self.z[1]:
            fooddirec.append("South")
        if newPos[1]<self.z[1]:
            fooddirec.append("North")
        if newPos in dangerzone:
            k= -100000
        elif currentGameState.hasFood(newPos[0], newPos[1]):
            k= 50000
        elif action == Directions.STOP:
            k= -2000
        elif action in fooddirec:
            k=200
        elif newPos not in self.hasgone:
            k= 8
        else:
            k= -3
        return successorGameState.getScore()+k

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

          gameState.getLegal Actions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        a= self.value(gameState, self.index)
        return a[1]

    def value(self, state, index):
        mindex=index%state.getNumAgents()
        if index/state.getNumAgents() >= self.depth or state.isWin() or state.isLose():
            z= (self.evaluationFunction(state), "Stop")
            return z
        if mindex==0:
            i=self.maxv(state, index)
            return i
        else:
            j=self.minv(state, index)
            return j
        
    def maxv(self, state, index):
        v=(-999999999,'Stop')
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            k=(self.value(state.generateSuccessor(nindex, way),index+1)[0],way)
            if k[0]>=v[0]:
                v=k
        return v

    def minv(self, state, index):
        v=(999999999,'Stop')
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            k=(self.value(state.generateSuccessor(nindex, way),index+1)[0],way)
            if k[0]<=v[0]:
                v=k
        return v



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a= self.value(gameState, self.index, -999999999, 999999999)
        return a[1]

    def value(self, state, index, a, b):
        mindex=index%state.getNumAgents()
        if index/state.getNumAgents() >= self.depth or state.isWin() or state.isLose():
            z= (self.evaluationFunction(state), "Stop")
            return z
        if mindex==0:
            i=self.maxv(state, index, a, b)
            return i
        else:
            j=self.minv(state, index, a, b)
            return j
        
    def maxv(self, state, index, a, b):
        v=(-999999999,'Stop')
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            k=(self.value(state.generateSuccessor(nindex, way),index+1, a ,b)[0],way)
            if k[0]>=v[0]:
                v=k
            if v[0]>b:
                return v
            if v[0]>=a:
                a=v[0]
        return v

    def minv(self, state, index, a, b):
        v=(999999999,'Stop')
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            k=(self.value(state.generateSuccessor(nindex, way),index+1, a, b)[0],way)
            if k[0]<=v[0]:
                v=k
            if v[0]<a:
                return v
            if v[0]<=b:
                b=v[0]
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
        a= self.value(gameState, self.index)
        return a[1]

    def value(self, state, index):
        mindex=index%state.getNumAgents()
        if index/state.getNumAgents() >= self.depth or state.isWin() or state.isLose():
            z= (self.evaluationFunction(state), "Stop")
            return z
        if mindex==0:
            i=self.maxv(state, index)
            return i
        else:
            j=self.expv(state, index)
            return j
        
    def maxv(self, state, index):
        v=(-999999999,'Stop')
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            k=(self.value(state.generateSuccessor(nindex, way),index+1)[0],way)
            if k[0]>=v[0]:
                v=k
        return v

    def expv(self, state, index):
        v=0 
        nindex=(index)%state.getNumAgents()
        for way in state.getLegalActions(nindex):
            p=1.0/len(state.getLegalActions(nindex))
            k=(self.value(state.generateSuccessor(nindex, way),index+1)[0],way)
            v+=p * k[0]
        return (v, way)



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostpos =[]
    scaredghost =[]
    dangerzone =[]
    for i in newGhostStates:
        if newScaredTimes[newGhostStates.index(i)]==0:
            ghostpos.append(i.getPosition())
            for state in [currentGameState.generateSuccessor(newGhostStates.index(i), way) for way in currentGameState.getLegalActions(newGhostStates.index(i))]:
                for state2 in [state.generateSuccessor(newGhostStates.index(i), way2) for way2 in state.getLegalActions(newGhostStates.index(i))]:
                    for a in state2.getGhostStates():
                        dangerzone.append(a.getPosition())
        else:
            scaredghost.append(i.getPosition())
    """
    z : the nearest food position
    x : the manhattanDistance to z 
    h : fix x
    """
    h=0
    Food = list(currentGameState.getFood())
    z=(0,0)
    x=999999999999
    for i in range(len(Food)):
        for j in range(len(Food[0])):
            if Food[i][j]:
                h+=1
                if manhattanDistance(newPos, (i,j))<x:
                    z=(i,j)
                    x=util.manhattanDistance(newPos, z)
    """
    k : the number of food in this state
    x : k
    x4 : the number of scared ghost
    """
    k=0
    for i in Food:
        for j in i:
            if j:
                k-=1
    x4=0
    for i in newScaredTimes:
        if i >0:
            x4+=29
    '''
    x2 : chance the pacman might be eaten
    x3 : the manhattanDistance to scared ghosts
    a  : the value of this leaf
    '''
    if h==0:
        x=10
    x1=k
    x2=0
    if newPos in dangerzone:
        x2 = -60
    x3=-sum([util.manhattanDistance(newPos, y) for y in scaredghost])
    '''
    x  :when there is no food  nearby, get close to food will get higher score  
    x1 :the smaller the number of food, the higher the score it is
    x2 :when the state is too close to the ghost, x2 will make the value smaller
    x3 :get close to scared ghost will get somewhat higher grade
    x4 :the more ghost get scared, the higher grade you get
    x2 and x4 :the highest value for x4 is 58 < x2 = 60,
    which will make the pacman's move less risky
    '''
    a=-x*0.3 +x1  + x2 + x3*0.7 + x4 +successorGameState.getScore()
    return a

# Abbreviation
better = betterEvaluationFunction

