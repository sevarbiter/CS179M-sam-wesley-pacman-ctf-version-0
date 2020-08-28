import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint
from util import raiseNotDefined
import math

class Finder:

  def __init__(self):
    self.x = 0
    self.y = 0
    self.pacmanPos = []
    self.ghostPos = []
    self.ghostStates = []
    self.foodList = []
    self.carrying1 = 0
    self.carrying2 = 0
    self.mostRecentlyEaten = None

  def getGrid(self, gameState):
    """
    Updates the class x and y variables with the size of the gameboard grid
    """
    self.y = gameState.data.food.height
    self.x = gameState.data.food.width

  def addLocations(self, gameState, agent):
    """
    Updates the class with locations of enemies before the agent makes 
    an action
    """
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
    """
    Checks if a food has been eatent recently and saves that position
    """
    myFoodList = agent.getFoodYouAreDefending(gameState).asList()
    myLastFoodList = agent.getFoodYouAreDefending(lastState).asList()
    eaten = list(set(myLastFoodList)-set(myFoodList))
    if len(eaten) > 0:
      self.mostRecentlyEaten = eaten[0]

  def getFeatures(self, gameState, agent):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    
    if agent.index == 0 or agent.index == 1:
      features['closestFood'] = self.closestFood(gameState, agent)
      features['foodCarrying'] = self.foodCarryingHeader(gameState, agent)
      features['ghostsNear'] = self.nearby(gameState, 1, agent)
    else:
      features['nearestEatenFood'] = self.nearestEatenFood(gameState, agent)

    features['pacmanNear'] = self.nearby(gameState, 0, agent)

    return features

  def closestFood(self, gameState, agent):
    """
    Returns the reciprocal of the distance from current position
    to the closest food, returns 0 if there are only 2 food left
    """
    minDistance = 0
    if len(self.foodList) > 2:
      myPos = gameState.getAgentState(agent.index).getPosition()
      minDistance = min([agent.getMazeDistance(myPos, food) for food in self.foodList])
    else:
      return 0
    if minDistance == 0:
      return 2
    return 1/minDistance
      
  def nearby(self, gameState, option, agent):
    """
    Returns the reciprocal of the distance away from the closest pacman
    or ghost
    """
    enemies = [i for i in agent.getOpponents(gameState)]
    if option == 0: #pacman near
      if len(self.pacmanPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.pacmanPos]
        minDist = min(dists)
        if minDist == 0:
          minDist = .5
        if gameState.getAgentState(agent.index).scaredTimer > 0 and (minDist == .5 or minDist == 1 or minDist == 2):
          #flip value if scared
          minDist = -minDist
        return 1/minDist
      else:
        return 0
    if option == 1: #ghost near
      flag = 0
      for ghosts in self.ghostStates:
        if ghosts.scaredTimer > 10: #disregard ghost if its scared
          for pos in self.ghostPos:
            if pos == ghosts.getPosition():
              self.ghostPos.remove(pos)
        elif ghosts.scaredTimer > 3: #attack ghost if its scared
          flag = 1
      if len(self.ghostPos) > 0:
        dists = [agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), a) for a in self.ghostPos]
        minDist = min(dists)
        if minDist > 5:
          minDist = minDist*2
        if minDist == 0:
          minDist = .5
        if flag == 1:
          minDist = -minDist
        return 1/minDist
      else:
        return 0
    return 0

  def inTunnel(self, gameState, agent):
    """
    Returns a 1 or 0 based on whether the agent is in a tunnel
    """
    myState = gameState.getAgentState(agent.index)
    myPos = myState.getPosition()
    x = int(myPos[0])
    y = int(myPos[1])
    if gameState.hasWall(x,y+1) and gameState.hasWall(x,y-1):
      return 1
    if gameState.hasWall(x+1,y) and gameState.hasWall(x-1,y):
      return 1
    return 0

  def deadendHeader(self, gameState, agent, count):
    """
    Header function that calls the recursive deadend function to
    check for deadends count away from the agent only if the 
    agent is on the enemy side
    """
    myX = gameState.getAgentState(agent.index).getPosition()[0]
    if gameState.isOnRedTeam(agent.index):
      if myX < self.x/2:
        return 0
    else:
      if myX >= self.x/2:
        return 0
    return self.deadend(gameState, agent, count)


  def deadend(self, gameState, agent, count):
    """
    Recursive call to return the reciprocal of distance away from a deadend
    if it is within count steps
    """
    legalActions = gameState.getLegalActions(agent.index)
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
      newCount = count-1
      routes.append(self.deadend(successor, agent, newCount)+1)
    minDistToDeadend = min(routes)
    if count == 3:
      print('min distance to deadend: ', minDistToDeadend)
      return 1/minDistToDeadend
    return minDistToDeadend

  def foodCarryingHeader(self, gameState, agent):
    """
    Header function that calls the recursiveFoodCarrying function to
    return the reciprocal of the distance away from the friendly side
    multiplied by the amount of food the agent is carrying
    """
    if agent.index == 0 or agent.index == 1:
      carryWeight = self.carrying1
    else:
      carryWeight = self.carrying2
    if carryWeight == 0:
      return 0
    else:
      return (1/self.recursiveFoodCarrying(gameState, agent, 0))*carryWeight

  def recursiveFoodCarrying(self, gameState, agent, count): 
    """
    Returns the minimum distance away from becoming a ghost for the agent
    If it encounters a ghost on that path it gives a very high number
    to indicate that that path is very bad
    """
    legalActions = gameState.getLegalActions(agent.index)
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)
    count = count+1
    if count >= 100:
      return 0
    myPos = gameState.getAgentState(agent.index).getPosition()
    if not gameState.getAgentState(agent.index).isPacman and myPos != gameState.getInitialAgentPosition(agent.index):
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
      if dist < minDist:
        actionToTake = action
        minDist = dist
    successor = gameState.generateSuccessor(agent.index, actionToTake)
    distanceToMiddle = self.recursiveFoodCarrying(successor, agent, count)+1
    
    if agent.index == 0 or agent.index == 1:
      carryWeight = self.carrying1
    else:
      carryWeight = self.carrying2
    return distanceToMiddle

  def isScared(self, gameState, agent):
    """
    Returns the distance away from a pacman if the agent is scared
    """
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
    """
    Returns the reciprocal of the distance away from the most recently 
    eaten food
    If it is within 3 moves of the location it is given the same
    value to allow it to patrol the area more freely
    If nothing has been eaten yet it find the distance to the furthest
    from the initial position
    """
    dist = 1
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
      if dist < 4: 
        dist = 1
      return 1/dist
    dist = agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), self.mostRecentlyEaten)
    if dist < 4:
      dist = 1
    return 1/dist

  def nearestFriendlyPowerPellet(self, gameState, agent):
    """
    Returns the reciprocal of the distance away from the nearest friendly power pellet
    """
    capsules = agent.getCapsulesYouAreDefending(gameState)
    if len(capsules) == 0:
      return 0
    dist = min([agent.getMazeDistance(gameState.getAgentState(agent.index).getPosition(), cap) for cap in capsules])
    if dist == 0:
      dist = 1
    return 1/dist
      
