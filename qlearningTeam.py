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

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'Agent1', second = 'DefensiveDummyAgent'):
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
    print('print state values: %d' % value)
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

  def __init__(self, numTraining=100, epsilon=0.8, alpha=0.5, gamma=1, **args):
    """
    index       - agent index
    alpha       - learning rate
    epsilon     - exploration rate
    gamma       - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes

    """
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
