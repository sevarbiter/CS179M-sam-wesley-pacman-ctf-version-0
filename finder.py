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
    self.foodList = []
    self.carrying1 = 0
    self.carrying2 = 0

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
    self.ghostPos = ghosts
    self.pacmanPos = invaders
    self.foodList = agent.getFood(gameState).asList()
    if agent.index == 0 or agent.index == 2:
      self.carrying1 = gameState.getAgentState(agent.index).numCarrying
    else:
      self.carrying2 = gameState.getAgentState(agent.index).numCarrying

  def getFeatures(self, gameState, agent):
    """
    Returns a counter of features for the state
    """
    # print('inside getFeatures ', gameState.getAgentPosition(agent.index))
    features = util.Counter()
    
    # features['ghostDistance'] = -(self.nearby(gameState, 3, agent))

    features['closestFood'] = self.closestFood(gameState, agent)

    features['ghostsNear'] = self.nearby(gameState, 0, agent)

    features['pacmanNear'] = self.nearby(gameState, 1, agent)

    # # features['inTunnel'] = self.inTunnel(gameState, agent)

    # features['inDeadend'] = self.inDeadend(gameState, agent)

    # features['scaredGhostNear'] = -(self.nearby(gameState, 2, agent))

    features['foodCarrying'] = self.foodCarrying(gameState, agent)

    features['isScared'] = self.isScared(gameState, agent)

    return features

  def closestFood(self, gameState, agent):
    minDistance = 0
    #foodList = agent.getFood(gameState).asList()
    if len(self.foodList) > 0:
      #myPos current position of agent on board as tuple ex. (1,2)
      myPos = gameState.getAgentState(agent.index).getPosition()
      #finds all food positions and returns the closest one to the agent
      minDistance = min([agent.getMazeDistance(myPos, food) for food in self.foodList])
    else:
      return 0
    if minDistance == 0:
      # print("close")
      minDistance = .5
    # print(minDistance)
    return 1/minDistance
    
  def nearby(self, gameState, option, agent):
    enemies = [i for i in agent.getOpponents(gameState)]
    # print(enemies)   
    if option == 1: #pacman near
      if len(self.pacmanPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.pacmanPos]
        minDist = min(dists)
        if minDist == 0:
          minDist = .5
        return 1/minDist
      else:
        return 0
    if option == 0: #ghost near
      if len(self.ghostPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.ghostPos]
        minDist = min(dists)
        if minDist == 0:
          minDist = .5
        return 1/minDist
      else:
        return 0
    if option == 2: #scared ghost near
      scaredy_cats = [a for a in enemies if gameState.getAgentState(a).scaredTimer > 0 and gameState.getAgentPosition(a) != None]
      return len(scaredy_cats)
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

  def inDeadend(self, gameState, agent):
    myState = gameState.getAgentState(agent.index)
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

  def foodCarrying(self, gameState, agent):
    carrying = gameState.getAgentState(agent.index).numCarrying
    if agent.index == 0 or agent.index == 2:
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

  
