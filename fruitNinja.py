import math
import random
import cv2

def getDistance(pos1, pos2):
  deltaX = (pos1.x - pos2.x)**2
  deltaY = (pos1.y- pos2.y)**2
  return math.sqrt(deltaX+deltaY)


class Element:
  def __init__(self, x, y, velX, velY, isFruit, radius):
    self.x = x
    self.y = y
    self.velX = velX
    self.velY = velY
    self.isFruit = isFruit
    self.radius = radius

  def gotCut(self, pos, vel):
    return getDistance(self,pos) <= self.radius and vel >= 800

def fruitNinja(image, width, height, 
              elements, score, lives, 
              posLeft, velocityLeft,
              posRight, velocityRight):
  
  if random.randint(1,100) <= 2:
    element = Element(
      random.uniform(0,width),
      height,
      random.uniform(-20, 20),
      random.uniform(-65,-50),
      random.randint(1,4) <= 3,
      random.randint(50,80)
    )
    elements.append(element)

  for element in elements:
    color = (255,255,0) if element.isFruit else (0,0,255)
    cv2.circle(image, ((int)(element.x), (int)(element.y)), element.radius, color, cv2.FILLED)

    element.x = (element.x + element.velX) % width
    element.y += element.velY
    element.velY += 2

    if element.gotCut(posLeft,velocityLeft) or element.gotCut(posRight,velocityRight):
      elements.remove(element)
      if element.isFruit:
        score += 1
      else:
        lives -= 1

    if element.y+element.radius <= 0:
      elements.remove(element)

    
  return elements, score, lives
  


  

  
  