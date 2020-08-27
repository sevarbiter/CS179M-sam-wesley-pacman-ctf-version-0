import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint
from util import raiseNotDefined
import math

class Finder:

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
    self.pacmanPos = []
    self.ghostPos = []
    self.ghostStates = []
    self.foodList = []
    self.carrying1 = 0
    self.carrying2 = 0
    self.mostRecentlyEaten = None

  def increment(self):
    self.test = self.test+1
    # print(self.test)

  def getGrid(self, gameState):
    self.y = gameState.data.food.height
    self.x = gameState.data.food.width
    #print(self.y)
    #print(self.x)

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

  def addLocations(self, gameState, agent):
    enemies = [i for i in agent.getOpponents(gameState)]
    invaders = [gameState.getAgentPosition(a) for a in enemies if gameState.getAgentState(a).isPacman and gameState.getAgentPosition(a) != None]
    ghosts = [gameState.getAgentPosition(a) for a in enemies if not gameState.getAgentState(a).isPacman and gameState.getAgentPosition(a) != None]
    self.ghostStates = [gameState.getAgentState(a) for a in enemies if not gameState.getAgentState(a).isPacman and gameState.getAgentPosition(a) != None]
    self.ghostPos = ghosts
    self.pacmanPos = invaders
    self.myFoodList = agent.getFoodYouAreDefending(gameState).asList()
    self.foodList = agent.getFood(gameState).asList()
    if agent.index == 0 or agent.index == 1:
      self.carrying1 = gameState.getAgentState(agent.index).numCarrying
    else:
      self.carrying2 = gameState.getAgentState(agent.index).numCarrying

  def updateMyFood(self, gameState, lastState, agent):
    myFoodList = agent.getFoodYouAreDefending(gameState).asList()
    myLastFoodList = agent.getFoodYouAreDefending(lastState).asList()
    spot = list(set(myLastFoodList)-set(myFoodList))
    if len(spot) > 0:
      self.mostRecentlyEaten = spot[0]
    #print(self.mostRecentlyEaten)

  def getFeatures(self, gameState, agent):
    """
    Returns a counter of features for the state
    """
    # print('inside getFeatures ', gameState.getAgentPosition(agent.index))
    features = util.Counter()
    
    # features['ghostDistance'] = -(self.nearby(gameState, 3, agent))
    if agent.index == 0 or agent.index == 1:
      features['closestFood'] = self.closestFood(gameState, agent)
      features['foodCarrying'] = self.foodCarryingHeader(gameState, agent)
      features['ghostsNear'] = self.nearby(gameState, 0, agent)
    else:
      features['nearestEatenFood'] = self.nearestEatenFood(gameState, agent)
      #features['isScared'] = self.isScared(gameState, agent)
      #features['nearestPowerPellet'] = self.nearestFriendlyPowerPellet(gameState, agent)

    # features['randomClosestFood'] = self.randomClosestFood(gameState, agent)


    features['pacmanNear'] = self.nearby(gameState, 1, agent)

    # # features['inTunnel'] = self.inTunnel(gameState, agent)

    #features['inDeadend'] = self.inDeadend(gameState, agent)

    # features['scaredGhostNear'] = self.nearby(gameState, 2, agent)

    #features['isScared'] = self.isScared(gameState, agent)

    #features['deadend'] = self.deadendHeader(gameState, agent, 3)

    return features

  def closestFood(self, gameState, agent):
    minDistance = 0
    #foodList = agent.getFood(gameState).asList()
    if len(self.foodList) > 2:
      #myPos current position of agent on board as tuple ex. (1,2)
      myPos = gameState.getAgentState(agent.index).getPosition()
      #finds all food positions and returns the closest one to the agent
      minDistance = min([agent.getMazeDistance(myPos, food) for food in self.foodList])
    else:
      return 0
    if minDistance == 0:
      # print("close")
      # minDistance = .5
      return 2
    #print(minDistance)
    return 1/minDistance
  
  def randomClosestFood(self, gameState, agent):
    randomDistance = 0
    #foodList = agent.getFood(gameState).asList()
    if len(self.foodList) > 2:
      #myPos current position of agent on board as tuple ex. (1,2)
      myPos = gameState.getAgentState(agent.index).getPosition()
      #finds all food positions and returns the closest one to the agent
      foodList = [agent.getMazeDistance(myPos, food) for food in self.foodList]
      randomDistance = min(foodList)
      foodList.remove(randomDistance)
      # minDistance = min(foodList)
      randomDistance = random.choice(foodList)
    else:
      return 0
    if randomDistance == 0:
      # print("close")
      randomDistance = .5
    # print(randomDistance)
    return 1/randomDistance*0.10
    
  def nearby(self, gameState, option, agent):
    enemies = [i for i in agent.getOpponents(gameState)]
    # print(enemies)   
    if option == 1: #pacman near
      if len(self.pacmanPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.pacmanPos]
        minDist = min(dists)
        if minDist == 0:
          minDist = .5
        if gameState.getAgentState(agent.index).scaredTimer > 0 and (minDist == .5 or minDist == 1 or minDist == 2):
          minDist = -minDist
        return 1/minDist
      else:
        return 0
    if option == 0: #ghost near
      flag = 0
      for ghosts in self.ghostStates:
        if ghosts.scaredTimer > 10:
          for pos in self.ghostPos:
            if pos == ghosts.getPosition():
              self.ghostPos.remove(pos)
        elif ghosts.scaredTimer > 3:
          flag = 1
      if len(self.ghostPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.ghostPos]
        minDist = min(dists)
        if minDist > 5:
          return 0
        if minDist == 0:
          minDist = .5
        if flag == 1:
          minDist = -minDist
        return 1/minDist
      else:
        return 0
    if option == 3: #estimated position
      myPos = gameState.getAgentPosition(agent.index)
      # print('index: %d' % agent.index)
      # print('inside nearby ',myPos)
      x = int(myPos[0])
      y = int(myPos[1])
      myPosInt = (x, y)
      places = self.getEnemies()
      dists = [agent.getMazeDistance(myPosInt, a) for a in places]
      return min(dists)
    return 0

  def inTunnel(self, gameState, agent):
    myState = gameState.getAgentState(agent.index)
    myPos = myState.getPosition()
    x = int(myPos[0])
    y = int(myPos[1])
    if gameState.hasWall(x,y+1) and gameState.hasWall(x,y-1):
      return 1
    if gameState.hasWall(x+1,y) and gameState.hasWall(x-1,y):
      return 1
    return 0

  def inDeadend(self, gameState, agent, lastPos, count):
    myState = gameState.getAgentState(agent.index)
    myPos = myState.getPosition()
    x = int(myPos[0])
    y = int(myPos[1])
    walls = 0
    if gameState.hasWall(x+1,y):
      walls=walls+1
    if gameState.hasWall(x-1,y):
      walls=walls+1
    if gameState.hasWall(x,y+1):
      walls=walls+1
    if gameState.hasWall(x,y-1):
      walls=walls+1
    if walls == 3:
      return 1
    return 0

  def deadendHeader(self, gameState, agent, count):
    myX = gameState.getAgentState(agent.index).getPosition()[0]
    if gameState.isOnRedTeam(agent.index):
      if myX < self.x/2:
        return 0
    else:
      if myX >= self.x/2:
        return 0
    return self.deadend(gameState, agent, count)


  def deadend(self, gameState, agent, count):
    legalActions = gameState.getLegalActions(agent.index)
    # print(count)
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)
    
    x = int(gameState.getAgentState(agent.index).getPosition()[0])
    y = int(gameState.getAgentState(agent.index).getPosition()[1])
    if gameState.isOnRedTeam(agent.index):
      if x < self.x/2:
        return 100
    else:
      if x >= self.x/2:
        return 100

    #if len(legalActions) == 1: #its in deadend
    walls = 0
    if gameState.hasWall(x+1,y):
      walls=walls+1
    if gameState.hasWall(x-1,y):
      walls=walls+1
    if gameState.hasWall(x,y+1):
      walls=walls+1
    if gameState.hasWall(x,y-1):
      walls=walls+1
    if walls == 3:
      print(x,y)
      return 1
    if count == 0: #end of search
      return 100
    routes = []
    for action in legalActions:
      successor = gameState.generateSuccessor(agent.index, action)
      # print(successor)
      newCount = count-1
      routes.append(self.deadend(successor, agent, newCount)+1)
    minDistToDeadend = min(routes)
    if count == 3:
      print('min distance to deadend: ', minDistToDeadend)
      return 1/minDistToDeadend
    return minDistToDeadend


  def foodCarrying(self, gameState, agent):
    carrying = gameState.getAgentState(agent.index).numCarrying
    if agent.index == 0 or agent.index == 1:
      carryWeight = self.carrying1
    else:
      carryWeight = self.carrying2

    myPos = gameState.getAgentState(agent.index).getPosition()

    dist = agent.getMazeDistance(myPos, gameState.getInitialAgentPosition(agent.index))
    # print('distance: %d' % dist)
    if dist == 0:
      dist = 1
    if carryWeight == 0:
      return 0
    else:
      value = (1/dist)*carryWeight
      # print('value: ', value)
      return (1/dist)*carryWeight

  def foodCarryingHeader(self, gameState, agent):
    if agent.index == 0 or agent.index == 1:
      carryWeight = self.carrying1
    else:
      carryWeight = self.carrying2

    if carryWeight == 0:
      return 0
    else:
      return (1/self.recursiveFoodCarrying(gameState, agent, 0))*carryWeight

  def recursiveFoodCarrying(self, gameState, agent, count): 
    legalActions = gameState.getLegalActions(agent.index)
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)
    count = count+1
    if count >= 100:
      return 0
    myPos = gameState.getAgentState(agent.index).getPosition()
    if not gameState.getAgentState(agent.index).isPacman and myPos != gameState.getInitialAgentPosition(agent.index):
      #print('back on our side')
      return 0.5
    if myPos == gameState.getInitialAgentPosition(agent.index):
      return 1000
    dists = []
    actionToTake = legalActions[0]
    minDist = 1000
    for action in legalActions:
      temp = gameState.generateSuccessor(agent.index, action)
      newPos = temp.getAgentState(agent.index).getPosition()
      dist = agent.getMazeDistance(newPos, gameState.getInitialAgentPosition(agent.index))
      #print(dist)
      if dist < minDist:
        actionToTake = action
        minDist = dist
    successor = gameState.generateSuccessor(agent.index, actionToTake)
    #print(actionToTake)
    #print(successor)
    distanceToMiddle = self.recursiveFoodCarrying(successor, agent, count)+1
    
    if agent.index == 0 or agent.index == 1:
      carryWeight = self.carrying1
    else:
      carryWeight = self.carrying2
    #print('dist: ', distanceToMiddle)
    return distanceToMiddle

  def isScared(self, gameState, agent):
    if gameState.getAgentState(agent.index).scaredTimer > 0:
      if len(self.pacmanPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.pacmanPos]
        minDist = min(dists)
        if minDist == 0:
          minDist = .5
        return 1/minDist
      else:
        return 0
    else:
      return 0

  def nearestEatenFood(self, gameState, agent):
    if self.mostRecentlyEaten == None:
      myFoodList = agent.getFoodYouAreDefending(gameState).asList()
      intitialFurthest = 0
      for a in myFoodList:
        furthest = 0
        distToFood = agent.getMazeDistance(gameState.getInitialAgentPosition(agent.index), a)
        if distToFood > furthest:
          initialFurthest = a
          furthest = distToFood
      dist = agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), initialFurthest)
      if dist == 0:
        dist = 1
      return 1/dist
    dist = agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), self.mostRecentlyEaten)
    if dist == 0 or dist == 1 or dist == 2:
      dist = 1
    return 1/dist

  def nearestFriendlyPowerPellet(self, gameState, agent):
    capsules = agent.getCapsulesYouAreDefending(gameState)
    if len(capsules) == 0:
      return 0
    dist = min([agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), cap) for cap in capsules])
    if dist == 0:
      dist = 1
    return 1/dist
      
