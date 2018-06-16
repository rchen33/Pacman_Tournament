# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 16:25:11 2018

@author: Rachel
"""

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
    myPos = successor.getAgentState(self.index).getPosition()
    features['successorScore'] = self.getScore(successor)
    features['onOffense'] = 0
    if myState.isPacman: 
        features['onOffense'] = 50

    #Checks for walls
    '''features['walls'] = 0
    x, y = myPos
    x = int(x)
    y = int(y)
    if successor.hasWall(x-1,y) and successor.hasWall(x+1,y):
        if successor.hasWall(x,y-1) or successor.hasWall(x,y+1):
            features['walls'] = 2
        else:
            features['walls'] = 1
    elif successor.hasWall(x,y-1) and successor.hasWall(x,y+1):
        if successor.hasWall(x-1,y) or successor.hasWall(x+1,y):
            features['walls'] = 2
        else:
            features['walls'] = 1
    if not myState.isPacman:
        features['walls'] = 0'''
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    guards = [a for a in enemies if (not a.isPacman) and a.getPosition() != None]
    #features['run'] = 0
    if len(guards) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in guards]
      features['guardDistance'] = 1/(min(dists))
      if min(dists) <= 5:
          features['onOffense'] = 0
      '''if min(dists) <=5:
          features['run'] = 1'''
    features['goCatch'] = 0
    for invader in invaders:
        distance = self.getMazeDistance(myPos, invader.getPosition())
        if distance <=5:
            features['goCatch'] = 1
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'goCatch': 50, 'onOffense':2, 'guardDistance': -10}

capsuleList = self.getCapsulesYouAreDefending(successor)
    if len(capsuleList)>0:
        for capsule in capsuleList:
            features['nearCluster'] += self.getMazeDistance(myPos,capsule)
            
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
    if myState.isPacman: features['onOffense'] = 50

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      cluster = [food for food in foodList if self.getMazeDistance(myPos, food) <= 5]
      features['distanceToFood'] = minDistance
      if len(cluster) > 0:
          features['distanceToFood'] = minDistance * (1/(len(cluster)))
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
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'goCatch': 100, 'onOffense':1, 'guardDistance': -10}