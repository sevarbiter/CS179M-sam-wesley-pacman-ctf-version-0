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
from learningAgents import ReinforcementAgent

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'Agent1', second = 'DummyAgent'):
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
    #pacman = 0
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

    myState = gameState.getAgentState(self.index)
    print(myState.isPacman) 
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
    print('evalutate: %d'% (features * weights))
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
    print('numGhosts: %s' % ghosts)
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      features['ghostDistance'] = min(dists)

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
    print('action to proceed: %s'% action)
    return action
  
  def minMax(self,gameState, index, depth, maxi = True, action = Directions.STOP):
    print('agent: %d'% index)

    if gameState.isOver() or depth == 0:
      print('depth reached')
      return self.evaluate(gameState, action)
    
    if gameState.getAgentPosition(index) != None:
      actions = gameState.getLegalActions(index)
      print('move to take: %s' %actions)
    else:
      return
    
    if maxi:
      print('values for pacman')
      values = [self.minMax(gameState.generateSuccessor(index, action), index, depth-1, False) for action in actions]
      print('values: %s'%values)
      maxValue = max(values)
      print('maxi value: %s' %maxValue)
      bestActions = [a for a, v in zip(actions,values) if v == maxValue]
      print('maxi bestActions: %s '%bestActions)
      # return (maxValue, actions[random.choice(bestActions)])
      # return random.choice(bestActions)
      return random.choice(bestActions)
    else:
      values = []
      if index in self.getOpponents(gameState):
        print('values for opponent')
        values = [self.minMax(gameState.generateSuccessor(index, action), index+2, depth-1, False) for action in actions]
      else:
        print('values for pacman')
        values = [self.minMax(gameState.generateSuccessor(index, action), self.index, depth-1, True) for action in actions]
      print('printing mini values: %s'%values)
      minValue = max(values)
      print(minValue)
      # bestActions = [a for a, v in zip(actions,values) if v == minValue]
      # print(bestActions)
      return minValue
      # return actions[random.choice(bestActions)]
      # return (minValue, actions[random.choice(bestActions)])




  def miniMax(self, gameState, index, depth):
    print('---miniMax---')
    maxCost = float('-inf')
    print(index)
    actions = gameState.getLegalActions(index)
    print('index: %d'% index)
    print(actions)
    for move in actions:
      tempValue = maxCost
      successor = gameState.generateSuccessor(index, move)
      maxCost = self.minValue(successor, index + 1, depth, move)
      if maxCost > tempValue:
        action = move
    return action

  def minValue(self, gameState, index, depth, action):
    print('--minValue--')
    if gameState.isOver() or depth == 0:
      return self.evaluate(gameState, action)
    
    #very big value (inf)
    minCost = float('inf')
    print('index: %d'% index)
    if gameState.getAgentPosition(index) != None:
      #if we can see opponent move then we calculate move
      actions = gameState.getLegalActions(index)
      print(actions)
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
    print('--maxValue--')
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

    print(features['hazzyDist'])

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: 
      features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev:
      features['reverse'] = 1


    return features

  def getWeights(self, gameState, action):
    return {'numInvaders':-1000, 'defending':100, 'invaderDistance':-10, 'stop':-100, 'reverse': -2, 'pelletDistance':-6, 'hazzyDist':-1}

####################################
#     Reinforcement Learning       #
####################################

#To run game with training session and small map
#python3 capture.py -r myteam -b baselineteam -q --numGames 10 -l tinycapture

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent
    
    Functions:
      - computeValueFromQValues
      - computeActionFromQValues
      - getQValue
      - getAction
      - update
  """

  def __init__(self, **args):
    """
    init parent class with parameters that are called from 
    Agent1 subclass qValues is a dict that stores all the 
    values of that state and action
    """
    ReinforcementAgent.__init__(self, **args)
    self.qValues = util.Counter()

  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we have never seen a state
      or the Q node value otherwise
    """
    return self.qValues[(state, action)]

  def computeValueFromQValues(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.
      If no legalActions available return 0.
    """
    #remove STOP as from possible actions to take
    legalActions = state.getLegalActions(self.index)

    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    if len(legalActions) == 0:
      return 0.0
    else:
      values = []
    print(legalActions)
    for action in legalActions:
      values.append(self.getQValue(state,action))

    return max(values)

  def computeActionFromQValues(self, state):
    """
      Compute the best action to take in a state.
      If no legal actions are availabe return NONE.
    """
    legalActions = state.getLegalActions(self.index)
    maxValue = 0
    maxAction = None

    for action in legalActions:
      value = self.getQValue(state, action)
      if value > maxValue or maxAction is None:
        maxValue = value
        maxAction = action
    return maxAction

  def chooseAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise. 
      If no legal actions are availabe return NONE.
    """
    # Pick Action
    legalActions = state.getLegalActions(self.index)
    if len(legalActions) == 0:
      return None
    
    #remove STOP as from possible actions to take
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    #explore before exploit
    if util.flipCoin(self.epsilon):
      print('exploring')
      action = random.choice(legalActions)
    else:
      print('exploiting')
      action = self.computeActionFromQValues(state)

    "*** YOUR CODE HERE ***"
    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    # QLearning - Compute running average as we go (off policy learning)
    # Q(s,a) = (1-alpha)*Q(s,a)+(alpha)[r + gamma * maxQ(s',a'))]
    
    # DEBUGGING
    print('updating state qvalue')
    value = (1-self.alpha) * (self.getQValue(state,action)) + self.alpha * (reward + self.discount * self.computeValueFromQValues(state))
    self.qValues[(state,action)] = value
    print(value)
    # WORKING CODE
    # self.qValues[(state,action)] = (1-self.alpha) * (self.getQValue(state,action)) + self.alpha * (reward + self.discount * self.computeValueFromQValues(state))
    

  def getPolicy(self, state):
    return self.computeActionFromQValues(state)

  def getValue(self, state):
    return self.computeValueFromQValues(state)
  
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
  
  # def final(self, state):
  #   print('GAME FINISH!')


class Agent1(QLearningAgent):

  def __init__(self, index, numTraining=100, epsilon=0.8, alpha=0.5, gamma=1, **args):
    """
    index       - agent index
    alpha       - learning rate
    epsilon     - exploration rate
    gamma       - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes

    """
    args['index'] = index
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    QLearningAgent.__init__(self, **args)
  
  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action