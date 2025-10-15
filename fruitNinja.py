import math
import random
import cv2

fruit = cv2.imread("watermelon.png",-1)
bomb = cv2.imread("bomb.png",-1)

def getDistance(pos1, pos2):
  deltaX = (pos1.x - pos2.x)**2
  deltaY = (pos1.y- pos2.y)**2
  return math.sqrt(deltaX+deltaY)

def generateElements(width, height):
  elementsQnt = 3 if random.randint(0, 10) < 8 else 5

  newElements = []

  for i in range(elementsQnt):
    element = Element(
    random.randint(0,width),
    (int)(height + 0.04 * i * height),
    random.randint(-10, 10),
    (int)(random.uniform(-0.05,-0.04)*height),
    random.randint(1,4) <= 3,
    (int)(random.uniform(0.05,0.08)*height)
    )
    newElements.append(element)

  return newElements  

def renderElement(image, width, height, element):
  startX = element.x-element.radius
  trueStartX = max(0,startX)
  imgStartX = trueStartX-startX

  endX = element.x+element.radius
  trueEndX = min(endX,width)
  imgEndX = element.radius*2-(endX-trueEndX)

  startY = element.y-element.radius
  trueStartY = max(0,startY)
  imgStartY = trueStartY-startY

  endY = element.y+element.radius
  trueEndY = min(endY,height)
  imgEndY = element.radius*2-(endY-trueEndY)

  elementImg = fruit if element.isFruit else bomb
  try:
    elementImg = cv2.resize(elementImg, (element.radius*2,element.radius*2))[
      imgStartY:imgEndY,
      imgStartX:imgEndX
    ]

    alphaElement = elementImg[:, :, 3] / 255.0
    alphaBack = 1.0 - alphaElement

    for c in range(0, 3):
      image[
        trueStartY:trueEndY,
        trueStartX:trueEndX, c
      ] = (
        alphaElement * elementImg[:, :, c] +
        alphaBack * image[
          trueStartY:trueEndY,
          trueStartX:trueEndX, c
        ] 
      )


    image[
      trueStartY:trueEndY,
      trueStartX:trueEndX
    ] = elementImg
  except:
    pass
  

class Element:
  def __init__(self, x, y, velX, velY, isFruit, radius):
    self.x = x
    self.y = y
    self.velX = velX
    self.velY = velY
    self.isFruit = isFruit
    self.radius = radius

  def gotCut(self, pos, vel):
    return getDistance(self,pos) <= self.radius*2 and vel >= 750

def fruitNinja(image, width, height, 
              elements, score, lives, 
              posLeft, velocityLeft,
              posRight, velocityRight):

  if len(elements) == 0:
    if random.randint(1,1000) <= 100:
      elements += generateElements(width, height)

  else:
    if random.randint(1,1000) <= 3:
      elements += generateElements(width, height)

    #element = Element(
    #  random.randint(0,width),
    #  height,
    #  random.randint(-10, 10),
    #  (int)(random.uniform(-0.07,-0.06)*height),
    #  random.randint(1,4) <= 3,
    #  (int)(random.uniform(0.05,0.08)*height)
    #)
    #elements.append(element)

  for element in elements:

    if element.y >= 2*height:
      elements.remove(element)

    renderElement(image, width, height, element)

    element.x = (element.x + element.velX) % width
    element.y += element.velY
    element.velY += (int)(0.002*height)

    if element.gotCut(posLeft,velocityLeft) or element.gotCut(posRight,velocityRight):
      elements.remove(element)
      if element.isFruit:
        score += 1
      else:
        lives -= 1
        if lives == 0:
          print("Finished with " + str(score) + " points!")
          exit()

    if element.y+element.radius <= 0:
      elements.remove(element)

    
  return elements, score, lives