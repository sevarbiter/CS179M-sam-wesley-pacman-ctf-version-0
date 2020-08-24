from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
import game
import os
import json
from game import Directions
from util import nearestPoint
from util import raiseNotDefined
from myTeam import DefensiveDummyAgent
from finder import Finder
from random import sample

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

class ApproximateQLearning(CaptureAgent):

    def __init__(self, index, locationFinder, timeForComputing=0.1, actionFn = None, numTraining=95, epsilon=0.8, alpha=0.5, gamma=1):
        """
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        CaptureAgent.__init__(self, index, timeForComputing)
        self.locationFinder = locationFinder

        self.episodesSoFar = 1
        self.numTraining = int(numTraining)
        self.accumTrainingRewards = 0.0
        self.accumExploitRewards = 0.0

        self.EXPLORE = float(epsilon)
        self.LEARNING = float(alpha)
        self.DISCOUNT = float(gamma)
        
        self.weights = util.Counter()
        self.buffer = []
        self.dict = util.Counter()

        """
        MODIFIERS
        """
        self.SCORES = 10
        self.DIED = -7
        self.ATE_FOOD = 1
        self.ATE_PACMAN = 5

    def getPolicy(self, policyName):
        """
        Checks to see if there is a policy already written
        if there is then load policy else create new policy
        """
        if os.stat(policyName).st_size == 0:
          self.weights = util.Counter()
        else:
          self.weights = util.Counter()
          test = open(policyName, 'r').read()
          print("FILE READ: ",test)
          parsedDict = json.loads(test)
          for features in parsedDict:
            self.weights[features] = parsedDict[features]
          print('STARTING FEATURES: ',self.getWeights())
        
        if os.stat("buffer"+policyName).st_size == 0:
          self.buffer = []
        else:
          self.buffer = util.Counter()
          b = open("buffer"+policyName, 'r').read()
          print("FILE READ: ",b)
          parsedBuffer = json.loads(b)
          self.buffer = parsedBuffer
        #   print('PARSED :',parsedDict)
        #   for features in range(len(parsedDict)):
            # self.buffer[features] = parsedDict[features]
          print('STARTING BUFFER: ',self.getBuffer())
    
    def writePolicy(self, policyName):
        f = open(policyName,"w+")
        dumps = json.dumps(self.getWeights())
        f.write(dumps)
        f.close()

        b = open("buffer"+policyName,"w+")
        dumpsB = json.dumps(self.getBuffer())
        b.write(dumpsB)
        b.close()
    
    def registerInitialState(self, gameState):
        """
        Override function from CaptureAgents.py, call original function
        and initiates starting episodes to keep track of the number of
        games played
        """
         #self.start I dont know where we used this yet called in baselineTeam?????
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)
        self.startEpisode()
        if self.episodesSoFar == 0:
            print('Beginning %d episodes of Training' % (self.numTraining))
    
    def getWeights(self):
        return self.weights
    
    def getBuffer(self):
        return self.buffer

    def startEpisode(self):
        """
        Called at the start of game (registerInitialState) when new episode 
        is starting
        """
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0
    
    def stopEpisode(self):
        """
        Called at the end of game (final) when episode is done. This will print
        out the reward results for rewards in exploring and exploiting.
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainingRewards += self.episodeRewards
        else:
            self.accumExploitRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            print('----------------EXPLOIT MODE----------------')
            self.epsilon = 0.0    #no exploration
            self.alpha = 0.0      #no learning
    
    def final(self, gameState):
        #observationHistory comes from default captureAgents.py
        self.observationHistory = []
        #-----

        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += self.getScore(gameState)

        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainingRewards / float(self.episodesSoFar)
                print('\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % (
                        trainAvg))
            else:
                testAvg = float(self.accumExploitRewards) / (self.episodesSoFar - self.numTraining)
                print('\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining))
                print(')\tAverage Rewards over testing: %.2f' % testAvg)
            print('\tAverage Rewards for last %d episodes: %.2f'  % (
                    NUM_EPS_UPDATE,windowAvg))
            print('\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime))
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print('%s\n%s' % (msg,'-' * len(msg)))
    
    def getRewards(self, gameState):
        pass

    def getQValue(self, gameState, action):
        """
         Returns the qValue of state and action. By adding all features * weights.
        """
        qValue = 0
        succesor = gameState.generateSuccessor(self.index, action)

        features = self.locationFinder.getFeatures(succesor,self)
        for feature in features:
             #print(features)
             #print(self.getWeights())
             qValue += features[feature] * self.weights[feature]
        return qValue
    
    def chooseAction(self, gameState):
        """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise. 
        If no legal actions are availabe return NONE.
        """
        # self.episodeRewards += deltaReward
        #print(self.lastState)
        if self.lastState != None:
            self.update(gameState, self.getRewards(gameState))
        
        # print(self.getWeights())

        legalActions = gameState.getLegalActions(self.index)

        if len(legalActions) == 0:
            return None
        
        if Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        
        #explore and exploit
        if util.flipCoin(self.EXPLORE):
            action = random.choice(legalActions)
        else:
            self.locationFinder.addLocations(gameState, self)
            action = self.computeActionFromQValues(gameState)
        
        #what are we using this for???
        self.locationFinder.getGrid(gameState)
        self.locationFinder.addDistance(self.index, gameState.getAgentDistances(), \
            gameState.getAgentState(self.index).getPosition(), gameState)

        #update lastState and lastAction
        self.lastState = gameState
        self.lastAction = action
        
        #buffer check if full if True then pop first item, store current state,
        #action, and weights.
        if len(self.buffer) ==  1000:
            self.buffer.pop(0)

        # print('BUFFER :',list(self.buffer.queue))
        # print('BUFFER Size After :', len(self.buffer))

        return action
    
    def getMaxQValue(self, gameState):
        maxVal = []
        for action in gameState.getLegalActions(self.index):
            maxVal.append(self.getQValue(gameState, action))
        return max(maxVal)
    
    def computeActionFromQValues(self, gameState):
        """
        Compute the best action to take in a state.
        If no legal actions are availabe return NONE.
        """
        legalActions = gameState.getLegalActions(self.index)
        
        #remove STOP as from possible actions to take
        if Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)

        maxValue = 0
        maxAction = None
        print("------------")
        print("Agent%d" % self.index)
        for action in legalActions:
            value = self.getQValue(gameState, action)
            #print('Value: %d' % value)
            #print('Action:', action)
            if value > maxValue or maxAction is None:
                maxValue = value
                maxAction = action
        return maxAction


    def update(self, gameState, reward):

        features = self.locationFinder.getFeatures(gameState,self)
        
        prevQValue = self.getQValue(self.lastState, self.lastAction)
        print('Reward : ',reward)
        
        if len(gameState.getLegalActions(self.index)) == 0:
            difference =  reward - prevQValue
        else:
            maxQ = self.getMaxQValue(gameState)
            self.buffer.append((maxQ, reward))
            # print(self.buffer)
            avgList = sample(self.buffer, int(len(self.buffer)/10))
            #print('maxQ :',  maxQ)
            # print('avgList :', len(avgList))
            total = reward + self.DISCOUNT*maxQ
            for i in avgList:
                total += i[1] + self.DISCOUNT*i[0]
            # print('total of avgList :', total)
            total = total/(len(avgList) + 1)
            difference = total - prevQValue
        # print('difference : %d' % difference)
        for feature in features:
            self.weights[feature] += self.LEARNING * features[feature] * difference

        #print(features)
        #print(self.getWeights())

class Agent1(ApproximateQLearning):

    def __init__(self, index, locationFinder):
        ApproximateQLearning.__init__(self, index, locationFinder)
        self.ATE_FOOD =  7
        self.getPolicy("qPolicy0.txt")
    
    def getRewards(self, gameState):
        reward = 0
        #SCORES
        if self.getScore(gameState) > self.lastState.getScore():
            reward += self.getScore(gameState) - self.lastState.getScore() + self.SCORES
            print('REWARD Scored: %d' % reward)
        
        #ATE_FOOD
        foodList = self.getFood(gameState).asList()
        prevFood = self.getFood(self.lastState).asList()
        if len(foodList) > len(prevFood):
            reward += len(foodList) - len(prevFood) + self.ATE_FOOD
            #reward += len(foodList) - len(prevFood)
            print('REWARD Ate Food: %d' % reward)
        
        #DIED
        if gameState.getAgentPosition(self.index) == gameState.getInitialAgentPosition(self.index):
            lastX=self.lastState.getAgentPosition(self.index)[0]
            lastY=self.lastState.getAgentPosition(self.index)[1]
            currentX=gameState.getAgentPosition(self.index)[0]
            currentY=gameState.getAgentPosition(self.index)[1]
            if not (lastX == currentX+1 or lastX == currentX-1) and not (lastY == currentY+1 or lastY == currentY-1):
                reward += self.DIED
                print('REWARD DIED: %d' % reward)

        #ATE_PACMAN
        oldEnemies = [self.lastState.getAgentState(i) for i in self.getOpponents(self.lastState)]
        newEnemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        oldPacmen = [a for a in oldEnemies if a.isPacman and a.getPosition() != None]
        newPacmen = [a for a in newEnemies if a.isPacman and a.getPosition() != None]
        if len(oldPacmen) > 0:
            dists=[self.getMazeDistance(self.lastState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
            if min(dists) == 1:
                if len(newPacmen) == 0:
                    reward += self.ATE_PACMAN
                    print('REWARD Ate Pacman: %d' % reward)
                else:
                    if len(newPacmen) > 0:
                        dists=[self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
                    if min(dists) > 2:
                        reward += self.ATE_PACMAN
                        print('REWARD Ate Pacman: %d' % reward)
        return reward
    
    def final(self, gameState):
        print('AGENT1')
        ApproximateQLearning.final(self, gameState)
        self.writePolicy("qPolicy0.txt")

class Agent2(ApproximateQLearning):
    
    def __init__(self, index, locationFinder):
        ApproximateQLearning.__init__(self, index, locationFinder)
        self.ATE_PACMAN = 7
        self.getPolicy("qPolicy1.txt")
    
    def getRewards(self, gameState):
        reward = 0
        #SCORES
        if self.getScore(gameState) > self.lastState.getScore():
            reward += self.getScore(gameState) - self.lastState.getScore() + self.SCORES
            print('REWARD Scored: %d' % reward)
        
        #ATE_FOOD
        foodList = self.getFood(gameState).asList()
        prevFood = self.getFood(self.lastState).asList()
        if len(foodList) > len(prevFood):
            reward += len(foodList) - len(prevFood) + self.ATE_FOOD
            #reward += len(foodList) - len(prevFood)
            print('REWARD Ate Food: %d' % reward)
        
        #DIED
        if gameState.getAgentPosition(self.index) == gameState.getInitialAgentPosition(self.index):
            lastX=self.lastState.getAgentPosition(self.index)[0]
            lastY=self.lastState.getAgentPosition(self.index)[1]
            currentX=gameState.getAgentPosition(self.index)[0]
            currentY=gameState.getAgentPosition(self.index)[1]
            if not (lastX == currentX+1 or lastX == currentX-1) and not (lastY == currentY+1 or lastY == currentY-1):
                reward += self.DIED
                print('REWARD DIED: %d' % reward)

        #ATE_PACMAN
        oldEnemies = [self.lastState.getAgentState(i) for i in self.getOpponents(self.lastState)]
        newEnemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        oldPacmen = [a for a in oldEnemies if a.isPacman and a.getPosition() != None]
        newPacmen = [a for a in newEnemies if a.isPacman and a.getPosition() != None]
        if len(oldPacmen) > 0:
            dists=[self.getMazeDistance(self.lastState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
            if min(dists) == 1:
                if len(newPacmen) == 0:
                    reward += self.ATE_PACMAN
                    print('REWARD Ate Pacman: %d' % reward)
                else:
                    if len(newPacmen) > 0:
                        dists=[self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
                    if min(dists) > 2:
                        reward += self.ATE_PACMAN
                        print('REWARD Ate Pacman: %d' % reward)
        return reward
    
    def final(self, gameState):
        print('AGENT2')
        ApproximateQLearning.final(self, gameState)
        self.writePolicy("qPolicy1.txt")
