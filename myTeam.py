# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
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
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    ''' 
    self.defense = False

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    ''' 
    You should change this in your own agent.
    '''
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

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
    #return random.choice(actions)
  
  def isGhost(self, gameState, index):
      return not gameState.getAgentState(self.index).isPacman
  
  def isScared(self, gameState, index):
      return gameState.data.agentStates[index].scaredTimer > 0
    
  def nearGhost(self,gameState):
      if self.isGhost(gameState, self.index):
          return False
      else:
          for agent in self.getOpponents(gameState):
              if self.getMazeDistance(self.index,agent)<=5:
                  return True
      return False

class OffensiveReflexAgent(DummyAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    features['successorScore'] = self.getScore(successor)
    features['onOffense'] = 0
    if myState.isPacman: features['onOffense'] = 25

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    guards = [a for a in enemies if (not a.isPacman) and a.getPosition() != None]
    if len(guards) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in guards]
      features['guardDistance'] = 1/(min(dists))
    features['goCatch'] = 0
    for invader in invaders:
        if self.getMazeDistance(myPos, invader.getPosition()) <=5:
            features['goCatch'] = 1
            features['onOffense'] = 0
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'goCatch': 120, 'onOffense':1, 'guardDistance': -10}
  
  
class DefensiveReflexAgent(DummyAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
    foodList = self.getFoodYouAreDefending(successor).asList()
    features['nearCluster'] = 0
    if len(foodList)>0:
        for food in foodList:
            features['nearCluster'] += self.getMazeDistance(myPos,food)
    dangers = [self.fry(invader,foodList) for invader in invaders]
    if len(dangers) > 0:
      features['foodDanger'] = min(dangers)
    else:
      features['foodDanger'] = 0
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'nearCluster':-1, 'foodDanger': -10, 'stop': -100, 'reverse': -2}
  
  def fry(self, invader, foodList):
    dists = [self.getMazeDistance(invader.getPosition(),food) for food in foodList]
    return min(dists)