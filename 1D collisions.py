import pygame, sys, math, random
from pygame.locals import *
width = 800
height = 600
my_caption = ''
#Colours
BLACK = (0,0,0,255)
RED = (255,0,0,255)
BLUE = (0,0,255)
WHITE = (255,255,255)
windowColour = WHITE
screen = None
fpsClock = None
tickspeed = 50
time = 1/tickspeed
gravity = 50
top = 0
bottom = height
left = 0
right = width



class vectorObject():
       def __init__(self):
              self.vX = random.randint(-500,500)
              self.posX = random.randint(0,width)
              self.posY = height/2
       def move(self,):
              #s = s + ut
              self.posX = self.posX + time*self.vX
       def getvX(self):
              return self.vX
       def setvX(self,v):
              self.vX = v
       def setX(self, x):
              self.posX = x
       def getX(self):
              return self.posX
       def setY(self,y):
              self.posY = y
       def getY(self):
              return self.posY



class material():
       def __init__(self):
              self.colour = BLACK
              self.restitution = 0.8
       def setColour(self,c):
              self.colour = c
       def getColour(self):
              return self.colour
       def setRestitution(self,r):
              self.restitution = r
       def getRestitution(self):
              return self.restitution




class physicalObject():
       def __init__(self):
              self.vectors = vectorObject()
              self.mass = 100
              self.Material = material()
              self.radius = 80
       def wallCollision(self,wallMaterial,angle): #angle is measured in degrees with 0 being a horizontal flat surface
              self.vectors.setvX(wallMaterial.getRestitution()*self.Material.getRestitution()*(math.cos(2*math.radians(angle))*self.vectors.getvX()))
       def updateObject(self):
              self.vectors.move()
       def getMass(self):
              return self.mass
       def getRadius(self):
              return self.radius
       def setMass(self,m):
              self.mass = m
       def setRadius(self,r):
              self.radius = r
       def ballCollision(self,ball):
              m = self.getMass()
              M = ball.getMass()
              u = self.vectors.getvX()
              U = ball.vectors.getvX()
              print(m*u+U*M)
              e = ball.Material.getRestitution()*self.Material.getRestitution()
              v = (m*u+M*U+M*e*(U-u))/(m+M)
              V = e*(u-U)+v #(M*U+m*u+m*e*(u-U))/(m+M)

              print(m*v+V*M)
              self.vectors.setvX(v)
              ball.vectors.setvX(V)


############################Initialise##############################################
def initialise(windowWidth, windowHeight, windowName, windowColour):
       pygame.init()
       screen = pygame.display.set_mode((windowWidth,windowHeight),0,32)
       pygame.display.set_caption(windowName)
       screen.fill(windowColour) # change depending on requirements.
       fpsClock = pygame.time.Clock()
       return screen, fpsClock





############################Render##################################################
def render(screen,windowColour):
       screen.fill(WHITE)
       for i in range(len(balls)):
              pygame.draw.circle(screen,balls[i].Material.getColour(),(round(balls[i].vectors.getX()),round(balls[i].vectors.getY())),balls[i].getRadius())



def startPositions(balls):
        for i in range(len(balls)):
            balls[i] = physicalObject()
            balls[i].Material.setRestitution(1.0)
        balls[1].Material.setColour(RED)
        balls[0].vectors.setX(balls[0].getRadius()+1)
        balls[1].vectors.setX(width-balls[0].getRadius())
        return balls



       
def check(balls):
       for i in range(len(balls)):
              if balls[i].vectors.getY()- balls[i].getRadius() <= top and balls[i].vectors.getvY() < 0:
                     balls[i].wallCollision(wall,180)
              elif balls[i].vectors.getY() + balls[i].getRadius() >= bottom and balls[i].vectors.getvY() > 0:
                     balls[i].wallCollision(wall,0)
              if balls[i].vectors.getX() + balls[i].getRadius() >= right and balls[i].vectors.getvX() > 0:
                     balls[i].wallCollision(wall,90)
              elif balls[i].vectors.getX() - balls[i].getRadius() <= left and balls[i].vectors.getvX() < 0:
                     balls[i].wallCollision(wall,270)
              for j in range(i+1,len(balls)):
                     DistanceBetweenCentres = ((balls[i].vectors.getX()-balls[j].vectors.getX())**2)+ ((balls[i].vectors.getY()-balls[j].vectors.getY())**2)
                     if (balls[i].getRadius() - balls[j].getRadius())**2 <= DistanceBetweenCentres and DistanceBetweenCentres <= (balls[i].getRadius()+balls[j].getRadius())**2:
                            balls[i].ballCollision(balls[j])
                            #print((balls[i].getRadius() - balls[j].getRadius())**2 <= DistanceBetweenCentres)
                            P = (balls[i].vectors.getvX()*balls[i].getMass())+(balls[j].vectors.getvX()*balls[j].getMass())
                            #print(P)
       for i in range(len(balls)):
              balls[i].updateObject()
       return balls

if __name__ == "__main__":
       screen, fpsClock = initialise(width,height,my_caption,windowColour)
       balls = [None,None]
       balls = startPositions(balls)
       wall = material()
       wall.setRestitution(1.0)
       while True:
              fpsClock.tick(tickspeed)
              render(screen,windowColour)
              pygame.display.update()
              balls = check(balls)
              for event in pygame.event.get():
                     if event.type == QUIT:
                                 pygame.quit()
                                 sys.exit()









