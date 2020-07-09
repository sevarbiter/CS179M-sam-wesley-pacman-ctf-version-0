# myTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    #prints agent's position for red it will print (1,2)
    #pacman is 0
    #ghost >= 1
    #at the start of the game we will have an index of 1 and 2 meaning
    #we have 2 ghost on the board
    self.start = gameState.getAgentPosition(self.index)
    #prints none at the start of game
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''
  
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)
    
    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print('eval time for agent %d: %.4f' % (self.index, time.time() - start))

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    
    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction
    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != util.nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveAgent(DummyAgent):
  
  ################
  # MiniMaxAgent # 
  ################
  maxCarry = 4
  localCarry = 0
    
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    print('---START---')
    actions = gameState.getLegalActions(self.index)
    
    print(actions)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print('eval time for agent %d: %.4f' % (self.index, time.time() - start))

    print(values)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    print('bestActions: %s'% bestActions)

    
    foodLeft = len(self.getFood(gameState).asList())
    if self.getPreviousObservation():
      previousStateFood = len(self.getFood(self.getPreviousObservation()).asList())
      if foodLeft < previousStateFood:
        self.localCarry += 1
        # print(self.localCarry)
      if gameState.getScore() > self.getPreviousObservation().getScore():
        self.localCarry = 0
    

    # if foodLeft <= 2:
    #   bestDist = 9999
    #   for action in actions:
    #     successor = self.getSuccessor(gameState, action)
    #     pos2 = successor.getAgentPosition(self.index)
    #     dist = self.getMazeDistance(self.start,pos2)
    #     if dist < bestDist:
    #       bestAction = action
    #       bestDist = dist
    #   return bestAction
    print('---END---')
    return random.choice(bestActions)

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    # print(features)
    weights = self.getWeights(gameState, action)
    # print(weights)
    # print('evalutate: %d'% (features * weights))
    return features * weights

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    print('agent distances: %s'% gameState.getAgentDistances())

    if self.localCarry == self.maxCarry:
      defFoodList = self.getFoodYouAreDefending(successor).asList()
      features['successorScore'] = -len(defFoodList)

    else:
      # print(-len(foodList)) prints the -20 at the start of the game
      # we add this to features value
      features['successorScore'] = -len(foodList)

    if len(foodList) > 0 and self.localCarry != self.maxCarry:
      #myPos current position of agent on board as tuple ex. (1,2)
      myPos = successor.getAgentState(self.index).getPosition()
      #finds all food positions and returns the closest one to the agent
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      print(action, minDistance)
      features['distanceToFood'] = minDistance
    else:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in defFoodList])
      features['distanceToFood'] = minDistance

    return features
  
  def getWeights(self, gameState, action):
    # weights to be used as a multiplier for the given features
    # for example if successorScore is -20 & distanceToFood is 30 then
    # the total weight is -20*100 + -1*30 = -2030  
    return {'successorScore': 100, 'distanceToFood': -1}
  
  def minimax(self, gameState):
    
    self.numAgents = gameState.getNumAgents()
    self.myDepth = 0
    self.action = Directions.STOP
    self.maxFood = 4

    #very small value (-inf)
    def miniMax(gameState, index, depth, action):
      maxCost = float('-inf')
      legalMoves = gameState.getLegalActions(self.index)
      for move in legalMoves:
        tempValue = maxCost
        successor = gameState.generateSuccessor(self.index, move)
        maxCost = minValue(successor, index + 1, depth)
        if maxCost > tempValue:
          action = move
      return action
  
    def minValue(successor, index, depth):
      if gameState.isWin() or gameState.isLose() or depth == depth:
        return self.evaluate(successor, self.action)
      
      #very big value (inf)
      minCost = float('inf')
      legalMoves = gameState.getLegalActions(self.index)
      if index + 1 == self.numAgents:
        for move in legalMoves:
          successor = gameState.generateSuccessor(index, move)
          minCost = min(minCost, maxValue(successor, index, depth+1))
      else:
        for move in legalMoves:
          successor = gameState.generateSuccessor(index, move)
          minCost = min(minCost, minValue(successor, index+1, depth))
      return minCost
    
    def maxValue(successor, index, depth):
      if gameState.isWin() or gameState.isLose() or depth == depth:
        #need to create evaluate function
        return self.evaluate(successor, self.action) 

      index %= (self.numAgents - 1)
      maxCost = float('-inf')
      legalMoves = gameState.getLegalActions(index)
      for move in legalMoves:
        successor = gameState.generateSuccessor(index, move)
        maxCost = max(maxCost, minValue(successor, index+1, depth))
      return maxCost
  
    return miniMax(gameState, self.index, self.myDepth, self.action)