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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    s=util.Stack()
    state=problem.getStartState()
    current = state
    q=problem.getSuccessors(current)
    q.reverse()
    s.push((current , q))
    visit=[problem.getStartState()]

    while not problem.isGoalState(current):
        #print s.list
        current, Next=s.pop()
        Next=[i[:2] for i in Next if i[0] not in visit]
        s.push((current, Next))
        #print Next
        if Next == []:
            s.pop()
            current=s.pop()
            s.push(current)
            continue
        if problem.isGoalState(Next[0][0]):
            break
        if Next[0][0] not in visit:
            q=problem.getSuccessors(Next[0][0])
            q.reverse()
            s.push((Next[0][0], q))

        visit.append(Next[0][0])
        #print visit

        #print current

    #print s.list
    action=[path[1][0][1] for path in s.list]


    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors((5,4))
    #print action
    return action

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    q=util.Queue()
    state=problem.getStartState()
    q.push((state, []))
    current = state
    state =  []
    visit =  [problem.getStartState()]
    action = []
    while not problem.isGoalState(current):
        #print "q:", q.list
        k=q.pop()
        current=k[0]
        state=k[-1]
        if problem.isGoalState(current):
            #print state
            action=state
            break
        Next=[i[:2] for i in problem.getSuccessors(current) if i[0] not in visit]
        #print "next:", Next
        #raw_input()
        for i in Next:
            #print "i:", i
            q.push(i+(state+[i[1]],))

            visit.append(i[0])
        #print "curreent:", current
        #print "state:", state


    #print action
    return action

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    q=util.PriorityQueue()
    state=problem.getStartState()
    q.push(((state, []),problem.getSuccessors(state), 0) ,0)
    cost = 0
    current = state
    state =  []
    visit =  []
    action = []
    a=raw_input()
    """((point,way,cost,path),Next,totalcost )"""
    while not problem.isGoalState(current):
        if a=="1":
            print "q:"
            for i in q.heap:
                print "ss:", i[2][0]
                print "Next:", i[2][1]
                #print "totalcost:", i[2][2]
        k=q.pop()
        current=k[0][0]
        print current
        if current in visit:
            continue
        visit.append(current)
        state=k[0][-1]
        Next=k[-2]
        cost = k[-1]
        if problem.isGoalState(current):
            #print state
            action=state
            break
        print Next
        Next=[i for i in Next if i[0] not in visit]
        if a=="1":
            print "next:", Next
            print "visit:", visit
            raw_input()
        for i in Next:
            #print "i:", i
            q.push((i+(state+[i[1]],),problem.getSuccessors(i[0]) ,cost+i[-1]), cost+i[-1])

            #visit.append(i[0])

        #print "state:", state

    #print action
    return action



    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors((5,4))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
