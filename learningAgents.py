# learningAgents.py
# -----------------
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
from game import Directions, Agent, Actions
from finder import Finder
import random,util,time

class ReinforcementAgent(CaptureAgent):
    """
      Abstract Reinforcemnt Agent: A ValueEstimationAgent
      which estimates Q-Values (as well as policies) from experience
      rather than a model
      
      What you need to know:
        -   The environment will call
            observeTransition(state,action,nextState,deltaReward),
            which will call update(state, action, nextState, deltaReward)
            a function that we override in q learning class.
    """
    ####################################
    #    Override These Functions      #
    ####################################

    def update(self, state, action, nextState, reward):
        """
        This class will call this function, which you write, after
        observing a transition and reward
        """
        util.raiseNotDefined()

    ####################################
    #    Read These Functions          #
    ####################################

    def getLegalActions(self,state):
        """
        Get the actions available for a given
        state. This is what you should use to
        obtain legal actions for a state
        """
        return self.actionFn(state)

    def observeTransition(self, state,action,nextState, deltaReward):
        """
        Called by environment to inform agent that a transition has
        been observed. This will result in a call to self.update
        on the same arguments

        NOTE: Do *not* override or call this function
        """
        # print('TRANSITION')
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        """
        Called by environment when new episode is starting
        """
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
        Called by environment when episode is done
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            print('----------------EXPLOIT MODE----------------')
            self.epsilon = 0.0    #no exploration
            self.alpha = 0.0      #no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def __init__(self, index, locationFinder, timeForComputing=0.1, actionFn = None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        CaptureAgent.__init__(self, index, timeForComputing)
        if actionFn == None:
            actionFn = lambda state: state.getLegalActions()
        self.locationFinder = locationFinder
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    ################################
    # Controls needed for Crawler  #
    ################################
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discount = discount

    def doAction(self,state,action):
        """
        Called by inherited class when
        an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action

    ###################
    # Pacman Specific #
    ###################
    def observationFunction(self, state):
        """
        This is where we ended up after our last action.
        The simulation should somehow ensure this is called
        """
        gameState = state.makeObservation(self.index)

        if not self.lastState is None:
            reward = self.getReward(gameState)    
            self.observeTransition(self.lastState, self.lastAction, gameState, reward)
        return gameState

    def registerInitialState(self, state):
        CaptureAgent.registerInitialState(self, state)
        self.startEpisode()
        if self.episodesSoFar == 0:
            print('Beginning %d episodes of Training' % (self.numTraining))

    def final(self, state):
        """
        Called by Pacman game at the terminal state
        """
        # print('FINAL CALL')
        # deltaReward = self.getScore(state) - self.lastState.getScore()
        # self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        # self.stopEpisode()

        # Make sure we have this var
        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += self.getScore(state)

        NUM_EPS_UPDATE = 5
        if self.episodesSoFar % NUM_EPS_UPDATE == 10:
            print('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                print('\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % (
                        trainAvg))
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
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

    def getReward(self, gameState):

        '''
        Modifiers
        '''
        SCORES = 15
        DIED = -20
        ATE_FOOD = 7
        ATE_PACMAN = 5
        reward = 0

        #SCORES
        if self.getScore(gameState) > self.lastState.getScore():
            reward += self.getScore(gameState) - self.lastState.getScore() + SCORES
            print('REWARD Scored: %d' % reward)
        
        #ATE_FOOD
        foodList = self.getFood(gameState).asList()
        prevFood = self.getFood(self.lastState).asList()
        if len(foodList) > len(prevFood):
            reward += len(foodList) - len(prevFood) + ATE_FOOD
            print('REWARD Ate Food: %d' % reward)
        
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
                print('REWARD DIED: %d' % reward)
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
                    print('REWARD Ate Pacman: %d' % reward)
                else:
                    if len(newPacmen) > 0:
                        dists=[self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), a.getPosition()) for a in oldPacmen]
                    if min(dists) > 2:
                        reward += ATE_PACMAN
                        print('REWARD Ate Pacman: %d' % reward)
        return reward
  
