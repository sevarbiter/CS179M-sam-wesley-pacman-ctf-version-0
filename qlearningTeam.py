from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint
from util import raiseNotDefined
from learningAgents import ReinforcementAgent
from myTeam import DefensiveDummyAgent
from finder import Finder
import os
import json

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed, first = 'Agent1', second = 'Agent2'):
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
  locationFinder = Finder()
  locationFinder.__init__()

  return [eval(first)(firstIndex, locationFinder), eval(second)(secondIndex, locationFinder)]

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
      If no legalActions returns 0.
    """
    #remove STOP as from possible actions to take
    # legalActions = state.getLegalActions(self.index)

    # if Directions.STOP in legalActions:
    #   legalActions.remove(Directions.STOP)

    # if len(legalActions) == 0:
    #   return 0.0
    # else:
    #   values = []

    # print(legalActions)

    # for action in legalActions:
    #   values.append(self.getQValue(state,action))

    # return max(values)
    legalActions = state.getLegalActions(self.index)
    # print(legalActions)
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)
    
    values = []
    for action in legalActions:
        # newState = state.generateSuccessor(self.index,action)
        # print('Taking Action :', action, 'Position :', newState.getAgentPosition(self.index))
        successor = self.getQValue(state, action)
        # print(successor)
        values.append(successor)
    
    # values = [self.getQValue(state, action) for action in state.getLegalActions(self.index)]
    # print('Values ', values)
    if len(values) > 0:
        return max(values)
    else:
        return 0.0

  def computeActionFromQValues(self, state):
    """
      Compute the best action to take in a state.
      If no legal actions are availabe return NONE.
    """
    legalActions = state.getLegalActions(self.index)
    
    #remove STOP as from possible actions to take
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    maxValue = 0
    maxAction = None

    for action in legalActions:
      value = self.getQValue(state, action)
      print('Value: %d' % value)
      print('Action:', action)
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
      # print('exploring')
      action = random.choice(legalActions)
    else:
      # print('exploiting')
      action = self.computeActionFromQValues(state)
    # print(action)
    print(self.locationFinder.getFeatures(state, self))
    # print(Agent1.getWeights())
    self.locationFinder.getGrid(state)
    self.locationFinder.addDistance(self.index, state.getAgentDistances(), state.getAgentState(self.index).getPosition(), state)
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
    # print('updating state qvalue')
    value = (1-self.alpha) * (self.getQValue(state,action)) + self.alpha * (reward + self.discount * self.computeValueFromQValues(state))
    self.qValues[(state,action)] = value
    # print('print state values: %d' % value)
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

class Agent1(QLearningAgent):

    def __init__(self, index, locationFinder, numTraining=100, epsilon=0, alpha=0, gamma=1, **args):
        """
        index       - agent index
        alpha       - learning rate 0.5
        epsilon     - exploration rate 0.6
        gamma       - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        print('AGENT1 INIT')
        args['index'] = index
        args['locationFinder'] = locationFinder
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        args['locationFinder'].print()
        print(args['epsilon'])
        print(args['gamma'])
        print(args['alpha'])
        print(args['numTraining'])
        QLearningAgent.__init__(self, **args)
        if os.stat("qPolicy0.txt").st_size == 0:
          self.weights = util.Counter()
        else:
          self.weights = util.Counter()
          test = open("qPolicy0.txt", 'r').read()
          print("FILE READ: ",test)
          parsedDict = json.loads(test)
          for features in parsedDict:
            self.weights[features] = parsedDict[features]
          print('STARTING FEATURES: ',self.getWeights())
        # self.weights = util.Counter()

    
    # def getAction(self, state):
    #     """
    #     Simply calls the getAction method of QLearningAgent and then
    #     informs parent of action for Pacman.  Do not change or remove this
    #     method.
    #     """
    #     print('GETACTION')
    #     action = QLearningAgent.getAction(self,state)
    #     self.doAction(state,action)
    #     return action
    
    def getWeights(self):
        return self.weights
    
    def getQValue(self, state, action):
        """
        Returns the qValue of state and action. By adding all features * weights.
        """
        qValue = 0
        # print("inside getQValue")
        features = self.locationFinder.getFeatures(state.generateSuccessor(self.index, action), self)
        # print('features: ',features)
        # print('weights: ',self.getWeights())

        for feature in features:
            qValue += features[feature] * self.weights[feature]

        return qValue

    def update(self, state, action, nextState, reward):
        """
            Should update your weights based on transition
        """
        # print("inside update")
        features = self.locationFinder.getFeatures(state, self)
        # featuresList = features.sortedKeys()
        # print(features)
        # counter = 0
        # for feature in features:
        #     difference = 0
        #     if len(self.getLegalActions(nextState)) == 0:
        #         difference = reward - self.getQValue(state, action)
        #     else:
        #         # maxList = []
        #         # for action in self.getLegalActions(state):
        #         #   successor = state.generateSuccessor(self.index, action)
        #         #   maxList.append(self.getQValue(successor,action))
        #         # maxQ = max(maxList)
        # maxQ = max([self.getQValue(nextState, nextAction) for nextAction in self.getLegalActions(nextState)])
        #         difference = (reward + self.discount * maxQ - self.getQValue(state, action))
        #         print('maxQ: %d' % maxQ)
        #         print(difference)
        #     self.weights[feature] = (self.weights[feature] + self.alpha * difference * features[feature]) % 10 
        #     print(self.getWeights())
        #     counter += 1
        # print(self.getWeights())
        legalActions = state.getLegalActions(self.index)
    
        #remove STOP as from possible actions to take
        if Directions.STOP in legalActions:
          legalActions.remove(Directions.STOP)

        '''
        getValue computes all possible actions from the given state and returns the
        the highest value
        '''
        maxQValue = self.getValue(nextState)

        # print('Best Action :', action, 'Position :', state.getAgentPosition(self.index))
        prevQValue = self.getQValue(state, action)
        # print('Discount: %d' % self.discount)
        # print('maxQValue: %d' % maxQValue)
        # print('currQValue: %d' % currQValue)

        # if self.alpha == 0 and self.epsilon == 0:
        #   return

        
        difference = (reward + self.discount * maxQValue) - prevQValue

        for feature in features:
          self.weights[feature] = self.weights[feature] + self.alpha * features[feature] * difference
          # self.weights[feature] = self.weights[feature] % 10
          self.weights.normalize()
        # print(features)
        # print(self.getWeights())

    def final(self, state):
        "Called at the end of each game."
        print('-----FINAL-----')
        # call the super-class final method
        QLearningAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining: 
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            # print(self.getWeights())
            self.printToFile()
            pass
        # print(self.getWeights())
        # self.printToFile()

    def printToFile(self):
      f = open("qPolicy0.txt","w+")
      dumps = json.dumps(self.getWeights())
      f.write(dumps)
      f.close()

class Agent2(Agent1):

  def __init__(self, index, locationFinder, numTraining=100, epsilon=0, alpha=0, gamma=1, **args):
        """
        index       - agent index
        alpha       - learning rate 0.5
        epsilon     - exploration rate 0.6
        gamma       - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        print('AGENT 2 INIT')
        args['index'] = index
        args['locationFinder'] = locationFinder
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        args['locationFinder'].print()
        print(args['epsilon'])
        print(args['gamma'])
        print(args['alpha'])
        print(args['numTraining'])
        QLearningAgent.__init__(self, **args)
        if os.stat("qPolicy1.txt").st_size == 0:
          self.weights = util.Counter()
        else:
          self.weights = util.Counter()
          test = open("qPolicy1.txt", 'r').read()
          print("FILE READ: ",test)
          parsedDict = json.loads(test)
          for features in parsedDict:
            self.weights[features] = parsedDict[features]
          print('STARTING FEATURES: ',self.getWeights())
        # self.weights = util.Counter()
  
  def getReward(self, gameState):

    '''
    Modifiers
    '''
    SCORES = 15
    DIED = -20
    ATE_FOOD = 4
    ATE_PACMAN = 20
    reward = 0

    #SCORES
    if self.getScore(gameState) > self.lastState.getScore():
        reward += self.getScore(gameState) - self.lastState.getScore() + SCORES
        print('REWARD AGENT2 Scored: %d' % reward)
    
    #ATE_FOOD
    foodList = self.getFood(gameState).asList()
    prevFood = self.getFood(self.lastState).asList()
    if len(foodList) > len(prevFood):
        reward += len(foodList) - len(prevFood) + ATE_FOOD
        print('REWARD AGENT2 Ate Food: %d' % reward)
    
    #DIED
    if gameState.getAgentPosition(self.index) == gameState.getInitialAgentPosition(self.index):
        lastX=self.lastState.getAgentPosition(self.index)[0]
        lastY=self.lastState.getAgentPosition(self.index)[1]
        currentX=gameState.getAgentPosition(self.index)[0]
        currentY=gameState.getAgentPosition(self.index)[1]
        if (lastX == currentX+1 or lastX == currentX-1) and (lastY == currentY+1 or lastY == currentY-1):
            reward += DIED
        # if(not(lastX == currentX+1 or lastX == currentX-1)):
        # # print('current x: %d' % currentX)
        # # print('last x: %d' % lastX)
        # #reward += -1000
        # # print('Reward Eaten: %d' % reward)
        # j=1
        # elif(not(lastY == currentY+1 or lastY == currentY-1)):
        # # print('current x: %d' % currentX)
        # # print('last x: %d' % lastX)
        # #reward += -1000
        # # print('Reward Eaten: %d' % reward)
        # j=1 
        # else:
        # reward += DIED
            print('REWARD AGENT2 DIED: %d' % reward)
    # print('REWARD: %d' % reward)

    #ATE_PACMAN
    oldEnemies = [self.lastState.getAgentState(i) for i in self.getOpponents(self.lastState)]
    newEnemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    oldPacmen = [a for a in oldEnemies if a.isPacman and a.getPosition() != None]
    newPacmen = [a for a in newEnemies if a.isPacman and a.getPosition() != None]
    if len(oldPacmen) > 0:
        dists=[self.getMazeDistance(self.lastState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
        if min(dists) == 1:
            if len(newPacmen) == 0:
                reward += ATE_PACMAN
                print('REWARD AGENT2 Ate Pacman: %d' % reward)
            else:
                if len(newPacmen) > 0:
                    dists=[self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
                if min(dists) > 2:
                    reward += ATE_PACMAN
                    print('REWARD AGENT2 Ate Pacman: %d' % reward)
    return reward

  def final(self, state):
    "Called at the end of each game."
    print('-----FINAL AGENT2-----')
    # call the super-class final method
    QLearningAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining: 
        # you might want to print your weights here for debugging
        "*** YOUR CODE HERE ***"
        # print(self.getWeights())
        self.printToFile()
        pass
    print(self.getWeights())
    self.printToFile()

  def printToFile(self):
    f = open("qPolicy1.txt","w+")
    dumps = json.dumps(self.getWeights())
    f.write(dumps)
    f.close()


