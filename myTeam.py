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
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint
from util import raiseNotDefined
<<<<<<< HEAD
<<<<<<< HEAD
=======
import math
>>>>>>> distancing
#from learningAgents import ReinforcementAgent
=======
from learningAgents import ReinforcementAgent
from finder import Finder
>>>>>>> agent1FinalTesting

#################
# Team creation #
#################

class finder:

  def __init__(self):
    self.startup = 0
    self.list1 = []
    self.list2 = []
    self.index1 = 0
    self.index2 = 0
    self.test = 0
    self.enemy1 = (1,1)
    self.enemy2 = (1,1)
    self.location1 = (1,1)
    self.location2 = (1,1)
    self.x = 0
    self.y = 0

  def increment(self):
    self.test = self.test+1
    print(self.test)

  def getGrid(self, gameState):
    self.y = gameState.data.food.height
    self.x = gameState.data.food.width
    print(self.y)
    print(self.x)

  def addDistance(self, index, distances, position, gameState):
    if self.startup < 10:
      self.startup=self.startup+1
    if index == 0 or index == 1:
      self.index1 = index
    else:
      self.index2 = index
    temp = distances
    if index == self.index1:
      self.list1.append(distances)
      self.location1 = position
    else:
      self.list2.append(distances)
      self.location2 = position
    if len(self.list1) > 5:
      del self.list1[0]
    if len(self.list2) > 5:
      del self.list2[0]
    if self.startup > 4:
      self.updateLocations(gameState)

  def updateLocations(self, gameState):
    a1=0
    a2=0
    b1=0
    b2=0
    count = 0
    for x in self.list1:
      count=count+1
      if self.index1 == 0:
        a1=a1+x[1]
        a2=a2+x[3]
      else:
        a1=a1+x[0]
        a2=a2+x[2]
    if count>0:
      a1=a1/count
      a2=a2/count
    count = 0
    for y in self.list2:
      count=count+1
      if self.index2 == 2:
        b1=b1+y[1]
        b2=b2+y[3]
      else:
        b1=b1+y[0]
        b2=b2+y[2]
    if count>0:
      b1=b1/count
      b2=b2/count
    #print(a1)
    #print(a2)
    #print(b1)
    #print(b2)
    a1=a1-4
    a2=a2-4
    b1=b1-4
    b2=b2-4
    c = math.sqrt(pow((self.location2[0]-self.location1[0]),2) + pow((self.location2[1]-self.location2[1]),2))
    #print(c)
    if c == 0:
      c=1
    #enemy1
    x1 = int(abs((pow(a1, 2) - pow(b1, 2) + pow(c,2))/(2*c)))
    y1 = int(abs(math.sqrt(abs(pow(a1,2) - pow(x1,2)))))
    if x1 >= self.x-1:
      x1 = self.x-2
    if y1 >= self.y-1:
      y1 = self.y-2
    if x1 <= 0:
      x1 = 2
    if y1 <= 0:
      y1 = 2
    if gameState.hasWall(x1, y1):
      tuplelist = []
      #cross  
      if (not gameState.hasWall(x1+1, y1)):
        tuplelist.append((x1+1,y1))
      if (not gameState.hasWall(x1-1, y1)):
        tuplelist.append((x1-1,y1))
      if (not gameState.hasWall(x1, y1+1)):
        tuplelist.append((x1,y1+1))
      if (not gameState.hasWall(x1, y1-1)):
        tuplelist.append((x1,y1-1))
      #x
      if (not gameState.hasWall(x1+1, y1+1)):
        tuplelist.append((x1+1,y1+1))
      if (not gameState.hasWall(x1-1, y1+1)):
        tuplelist.append((x1-1,y1+1))
      if (not gameState.hasWall(x1+1, y1-1)):
        tuplelist.append((x1+1,y1-1))
      if (not gameState.hasWall(x1-1, y1-1)):
        tuplelist.append((x1-1,y1-1))
      temptuple = random.choice(tuplelist)
      x1 = temptuple[0]
      y1 = temptuple[1]
    #enemy2
    x2 = int(abs((pow(a2, 2) - pow(b2, 2) + pow(c,2))/(2*c)))
    y2 = int(abs(math.sqrt(abs(pow(a1,2) - pow(x2,2)))))
    if x2 >= self.x-1:
      x2 = self.x-2
    if y2 >= self.y-1:
      y2 = self.y-2
    if x2 <= 0:
      x2 = 2
    if y2 <= 0:
      y2 = 2
    if gameState.hasWall(x2, y2):
      tuplelist = []
      #cross
      if (not gameState.hasWall(x2+1, y2)):
        tuplelist.append((x2+1,y2))
      if (not gameState.hasWall(x2-1, y2)):
        tuplelist.append((x2-1,y2))
      if (not gameState.hasWall(x2, y2+1)):
        tuplelist.append((x2,y2+1))
      if (not gameState.hasWall(x2, y2-1)):
        tuplelist.append((x2,y2-1))
      #x
      if (not gameState.hasWall(x2+1, y2+1)):
        tuplelist.append((x2+1,y2+1))
      if (not gameState.hasWall(x2-1, y2+1)):
        tuplelist.append((x2-1,y2+1))
      if (not gameState.hasWall(x2+1, y2-1)):
        tuplelist.append((x2+1,y2-1))
      if (not gameState.hasWall(x2-1, y2-1)):
        tuplelist.append((x2-1,y2-1))
      temptuple = random.choice(tuplelist)
      x2 = temptuple[0]
      y2 = temptuple[1]

    self.enemy1 = (x1, y1)
    self.enemy2 = (x2, y2)
    #print(self.enemy1)
    #print(self.enemy2)

  def getEnemies(self):
    return (self.enemy1, self.enemy2)

  def print(self):
    print(self.location1)
    print(self.list1)
    print(self.location2)
    print(self.list2)

def createTeam(firstIndex, secondIndex, isRed,
<<<<<<< HEAD
<<<<<<< HEAD
               first = 'DummyAgent', second = 'DummyAgent'):
=======
               first = 'Agent1', second = 'DummyAgent'):
>>>>>>> agent1Sam
=======
               first = 'OffensiveAgent', second = 'DefensiveDummyAgent'):
>>>>>>> agent1FinalTesting
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
<<<<<<< HEAD
  # (firstindex, sharedobj)
  # The following line is an example only; feel free to change it.
  locationFinder = finder()
  locationFinder.__init__()
  #locationFinder.increment()
  #return [eval(first)(firstIndex), eval(second)(secondIndex)]
  return [OffensiveAgent(firstIndex, locationFinder), DummyAgent(secondIndex, locationFinder)]
  #return [eval(first)(firstIndex, locationFinder), eval(second)(secondIndex, locationFinder)]
=======
  locationFinder=Finder()
  locationFinder.__init__()
  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex, locationFinder), eval(second)(secondIndex, locationFinder)]
>>>>>>> agent1FinalTesting

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

<<<<<<< HEAD
  def registerInitialState(self, gameState, locationFinder=finder()):
=======
  def __init__(self, index, locationFinder):
    CaptureAgent.__init__(self, index)
    self.index = index
    self.locationFinder = locationFinder

  def registerInitialState(self, gameState):
>>>>>>> agent1FinalTesting
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
    #pacman = 0
    #ghost >= 1
    #at the start of the game we will have an index of 1 and 2 meaning
    #we have 2 ghost on the board
    self.start = gameState.getAgentPosition(self.index)
    self.location_finder = locationFinder
    self.location_finder.getGrid(gameState)
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
    self.location_finder.addDistance(self.index, gameState.getAgentDistances(), gameState.getAgentState(self.index).getPosition(), gameState)

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
    features['ghostDistance'] = self.nearby(gameState, 3)
    features['closestFood'] = self.closestFood(gameState)
    features['ghostsNear'] = self.nearby(gameState, 0)
    features['pacmanNear'] = self.nearby(gameState, 1)
    features['inTunnel'] = self.inTunnel(gameState)
    features['inDeadend'] = self.inDeadend(gameState)
    features['scaredGhostNear'] = self.nearby(gameState, 2)
    features['foodCarrying'] = self.foodCarrying(gameState)
    return features

  def closestFood(self, gameState):
    foodList = self.getFood(gameState).asList()
    if len(foodList) > 0:
      #myPos current position of agent on board as tuple ex. (1,2)
      myPos = gameState.getAgentState(self.index).getPosition()
      #finds all food positions and returns the closest one to the agent
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
    return minDistance
    
  def nearby(self, gameState, option):
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    if option == 1:
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      return len(invaders)
    if option == 0:
      ghosts = [a for a in enemies if (not a.isPacman) and a.getPosition() != None]
      return len(ghosts)
    if option == 2:
      scaredy_cats = [a for a in enemies if a.scaredTimer > 0 and a.getPosition() != None]
      return len(scaredy_cats)
    if option == 3:
      myPos = gameState.getAgentState(self.index).getPosition()
      x = int(myPos[0])
      y = int(myPos[1])
      myPosInt = (x, y)
      places = self.location_finder.getEnemies()
      dists = [self.getMazeDistance(myPosInt, a) for a in places]
      return min(dists)
    return 0

  def inTunnel(self, gameState):
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    x = int(myPos[0])
    y = int(myPos[1])
    if gameState.hasWall(x,y+1) and gameState.hasWall(x,y-1):
      return 1
    if gameState.hasWall(x+1,y) and gameState.hasWall(x-1,y):
      return 1
    return 0

  def inDeadend(self, gameState):
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    x = int(myPos[0])
    y = int(myPos[1])
    count = 0
    if gameState.hasWall(x+1,y):
      count=count+1
    if gameState.hasWall(x-1,y):
      count=count+1
    if gameState.hasWall(x,y+1):
      count=count+1
    if gameState.hasWall(x,y-1):
      count=count+1
    if count == 3:
      return 1
    return 0

  def foodCarrying(self, gameState):
    return gameState.getAgentState(self.index).numCarrying

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
    # print('---START---') 
    actions = gameState.getLegalActions(self.index)
    
    # print(actions)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print('eval time for agent %d: %.4f' % (self.index, time.time() - start))

    # print(values)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    # print('bestActions: %s'% bestActions)

    myState = gameState.getAgentState(self.index)
    # print(myState.isPacman) 
    foodLeft = len(self.getFood(gameState).asList())

    #checks to see if a
    if self.getPreviousObservation():
      previousStateFood = len(self.getFood(self.getPreviousObservation()).asList())
      if foodLeft < previousStateFood:
        self.localCarry += 1
        # print(self.localCarry)
        # if gameState.getScore() > self.getPreviousObservation().getScore():
        # self.localCarry = 0
      if myState.isPacman == False:
        self.localCarry = 0
<<<<<<< HEAD
    
    self.location_finder.addDistance(self.index, gameState.getAgentDistances(), gameState.getAgentState(self.index).getPosition(), gameState)
=======
 
    # self.location_finder.addDistance(self.index, gameState.getAgentDistances(), gameState.getAgentState(self.index).getPosition(), gameState)
>>>>>>> agent1FinalTesting
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
    # print('---END---')
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
    # print('getFeatures cost')
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    # print('agent distances: %s'% gameState.getAgentDistances())
    # print('numCarrying: %d' % myState.numCarrying)

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
      # print(action, minDistance)
      features['distanceToFood'] = minDistance
    else:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in defFoodList])
      features['distanceToFood'] = minDistance
    
    # Computes distance to ghosts we can see in order to avoid
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    # print('numGhosts: %s' % ghosts)
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      features['ghostDistance'] = min(dists)
      print('Ghost Near: %d' % min(dists))

    if action == Directions.STOP: features['stop'] = 1
    return features
  

  def getWeights(self, gameState, action):
    # weights to be used as a multiplier for the given features
    # for example if successorScore is -20 & distanceToFood is 30 then
    # the total weight is -20*100 + -1*30 = -2030  
    return {'successorScore': 100, 'distanceToFood': -1, 'numGhosts': -10, 'ghostDistance': 90, 'stop': -100}

class MiniMaxAgent(OffensiveAgent):
  
  myDepth = 4

  def chooseAction(self, gameState):
    action = self.minMax(gameState, self.index, self.myDepth)
    # print('action to proceed: %s'% action)
    return action
  
  def minMax(self,gameState, index, depth, maxi = True, action = Directions.STOP):
    # print('agent: %d'% index)

    if gameState.isOver() or depth == 0:
      # print('depth reached')
      return self.evaluate(gameState, action)
    
    if gameState.getAgentPosition(index) != None:
      actions = gameState.getLegalActions(index)
      # print('move to take: %s' %actions)
    else:
      return
    
    if maxi:
      # print('values for pacman')
      values = [self.minMax(gameState.generateSuccessor(index, action), index, depth-1, False) for action in actions]
      # print('values: %s'%values)
      maxValue = max(values)
      # print('maxi value: %s' %maxValue)
      bestActions = [a for a, v in zip(actions,values) if v == maxValue]
      # print('maxi bestActions: %s '%bestActions)
      # return (maxValue, actions[random.choice(bestActions)])
      # return random.choice(bestActions)
      return random.choice(bestActions)
    else:
      values = []
      if index in self.getOpponents(gameState):
        # print('values for opponent')
        values = [self.minMax(gameState.generateSuccessor(index, action), index+2, depth-1, False) for action in actions]
      else:
        # print('values for pacman')
        values = [self.minMax(gameState.generateSuccessor(index, action), self.index, depth-1, True) for action in actions]
      # # print('printing mini values: %s'%values)
      minValue = max(values)
      # print(minValue)
      # bestActions = [a for a, v in zip(actions,values) if v == minValue]
      # print(bestActions)
      return minValue
      # return actions[random.choice(bestActions)]
      # return (minValue, actions[random.choice(bestActions)])




  def miniMax(self, gameState, index, depth):
    # print('---miniMax---')
    maxCost = float('-inf')
    # print(index)
    actions = gameState.getLegalActions(index)
    # print('index: %d'% index)
    # print(actions)
    for move in actions:
      tempValue = maxCost
      successor = gameState.generateSuccessor(index, move)
      maxCost = self.minValue(successor, index + 1, depth, move)
      if maxCost > tempValue:
        action = move
    return action

  def minValue(self, gameState, index, depth, action):
    # print('--minValue--')
    if gameState.isOver() or depth == 0:
      return self.evaluate(gameState, action)
    
    #very big value (inf)
    minCost = float('inf')
    # print('index: %d'% index)
    if gameState.getAgentPosition(index) != None:
      #if we can see opponent move then we calculate move
      actions = gameState.getLegalActions(index)
      # print(actions)
      for move in actions:
        successor = gameState.generateSuccessor(index, move)
        minCost = min(minCost, self.minValue(successor, index+2, depth-1, move))
      return minCost
    elif gameState.getAgentPosition(index+2) != None:
      #else we look for second opponent
      actions = gameState.getLegalActions(index+2)
      for move in actions:
        successor = gameState.generateSuccessor(index+2, move)
        minCost = min(minCost, self.maxValue(successor, self.index, depth-1, move))
      return minCost
    else:
      return self.evaluate(gameState, action)
  
  def maxValue(self, gameState, index, depth, action):
    # print('--maxValue--')
    if gameState.isOver() or depth == depth:
      #need to create evaluate function
      return self.evaluate(gameState, action) 

    # index %= (gameState.getNumAgents() - 1)
    maxCost = float('-inf')
    if gameState.getAgentPosition(index) != None:
      actions = gameState.getLegalActions(index)
      for move in actions:
        successor = gameState.generateSuccessor(index, move)
        maxCost = max(maxCost, self.minValue(successor, index+1, depth, move))
    return maxCost

class DefensiveDummyAgent(DummyAgent):
  
  def __init__(self, index, locationFinder):
    DummyAgent.__init__(self, index, locationFinder)

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''
    #print("Actions")
    values = [self.evaluate(gameState, a) for a in actions]

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    #print("best actions")
    #print(bestActions)
<<<<<<< HEAD
    self.location_finder.addDistance(self.index ,gameState.getAgentDistances(), gameState.getAgentState(self.index).getPosition(), gameState)
    self.location_finder.print()
=======
    # self.locationFinder.getGrid(gameState)
    # self.locationFinder.addDistance(self.index, gameState.getAgentDistances(), gameState.getAgentState(self.index).getPosition(), gameState) 
    #self.locationFinder.getFeatures(gameState, self)
>>>>>>> agent1FinalTesting
    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    #print(action)
    #print(features)
    #print(features * weights)
    return features * weights

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    features['defending'] = 1
    if myState.isPacman:
      features['defending'] = 0
    
    pellets = gameState.getCapsules()
    bestDist = 1000
    for a in pellets:
      thisDist = self.getMazeDistance(myPos, a)
      if thisDist < bestDist:
        bestDist = thisDist
        features['pelletDistance'] = self.getMazeDistance(myPos, a)

    distances = gameState.getAgentDistances()
    if gameState.isOnRedTeam(self.index):
      if distances[1] < distances[3]:
        features['hazzyDist'] = distances[1]
      else:
        features['hazzyDist'] = distances[3]
    else:
      if distances[0] < distances[2]:
        features['hazzyDist'] = distances[0]
      else:
        features['hazzyDist'] = distances[2] 

<<<<<<< HEAD
    print(gameState.getAgentState(0))
=======
    # print(features['hazzyDist'])
>>>>>>> agent1FinalTesting

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
      print('Pacman Near: %d' % min(dists))

    if action == Directions.STOP: 
      features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev:
      features['reverse'] = 1


    return features

  def getWeights(self, gameState, action):
    return {'numInvaders':-1000, 'defending':100, 'invaderDistance':-10, 'stop':-100, 'reverse': -2, 'pelletDistance':-6, 'hazzyDist':-1}
