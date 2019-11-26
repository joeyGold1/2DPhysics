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
GREEN = (0,255,0,255)
YELLOW = (255,255,0,255)
PURPLE = (255,0,255,255)
windowColour = WHITE
screen = None
fpsClock = None
tickspeed = 60
time = 1/tickspeed
gravity = 50
top = 0
bottom = height
left = 0
right = width
g = 0

class GameState():
       def __init__(self):
              self.player1Turn = True
              self.gameOver = False
              self.playerAiming = False
       def getplayer1Turn(self):
              return self.player1Turn
       def togglePlayerTurn(self):
              if self.player1Turn:
                     self.player1Turn = False
              else:
                     self.player1Turn = True
       def setplayer1Turn(self,b):
              self.player1Turn = b
       def getgameOver(self):
              return self.gameOver
       def setgameOver(self,g):
              self.gameOver = g
       def getplayerAiming(self):
              return self.playerAiming
       def setplayerAiming(self,a):
              self.playerAiming = a

class vectorObject():
       def __init__(self):
              self.vX = random.randint(-500,500)
              self.vY = random.randint(-500,500)
              self.posX = width/2
              self.posY = height/2
       def move(self):
              #s = s + vt
              self.posX = self.posX + time*self.vX
              self.posY = self.posY + time*self.vY
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
       def getvY(self):
              return self.vY
       def setvY(self,y):
              self.vY = y


class material():
       def __init__(self):
              self.colour = BLACK
              self.restitution = 0.95
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
              self.mass = 500
              self.Material = material()
              self.radius = 90
              self.cooldown = 0
       def wallCollision(self,wallMaterial,angle): #angle is measured in degrees with 0 being a horizontal flat surface
              self.vectors.setvX(wallMaterial.getRestitution()*self.Material.getRestitution()*(math.cos(2*math.radians(angle))*self.vectors.vX - math.sin(2*math.radians(90-angle))*self.vectors.vY))
              self.vectors.setvY(wallMaterial.getRestitution()*self.Material.getRestitution()*((math.sin(2*math.radians(angle))*self.vectors.vX*-1) + (math.cos(2*math.radians(90-angle))*self.vectors.vY)))
       def updateObject(self):
              self.vectors.move()
              self.cooldown -= tickspeed
       def getMass(self):
              return self.mass
       def getRadius(self):
              return self.radius
       def setMass(self,m):
              self.mass = m
       def setRadius(self,r):
              self.radius = r
       def setcooldown(self,c):
              self.cooldown = c
       def getcooldown(self):
              return self.cooldown
       def ballCollision(self,ball):
              e = ball.Material.getRestitution()*self.Material.getRestitution()
              m = self.getMass()
              M = ball.getMass()
              x = self.vectors.getX()
              X = ball.vectors.getX()
              y = self.vectors.getY()
              Y = ball.vectors.getY()
              Ux = ball.vectors.getvX()
              Uy = ball.vectors.getvY()
              ux = self.vectors.getvX()
              uy = self.vectors.getvY()
              try:
                     angle = math.pi/2 - math.atan((Y-y)/(X-x))
              except ZeroDivisionError:
                     angle = 0
              ue = uy*math.cos(angle)+ux*math.sin(angle)
              ua = ux*math.cos(angle)-uy*math.sin(angle)
              Ue = Uy*math.cos(angle)+Ux*math.sin(angle)
              Ua = Ux*math.cos(angle)-Uy*math.sin(angle)
              ve = (m*ue+M*Ue+M*e*(Ue-ue))/(m+M)
              Ve = (M*Ue+m*ue+m*e*(ue-Ue))/(m+M)#e*(ue-Ue)+ve
              vx = ve*math.sin(angle)+ua*math.cos(angle)
              Vx = Ve*math.sin(angle)+Ua*math.cos(angle)
              vy = ve*math.cos(angle)-ua*math.sin(angle)
              Vy = Ve*math.cos(angle)-Ua*math.sin(angle)
              self.vectors.setvX(vx)
              ball.vectors.setvX(Vx)
              self.vectors.setvY(vy)
              ball.vectors.setvY(Vy)

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
       for i in range(0,round(width/20)):
              pygame.draw.line(screen,BLUE,(i*20,0),(i*20,height),1)
       for i in range(0,round(height/20)):
              pygame.draw.line(screen,BLUE,(0,i*20),(width,i*20),1)
                      
       for i in range(len(balls)):
              pygame.draw.circle(screen,balls[i].Material.getColour(),(round(balls[i].vectors.getX()),round(balls[i].vectors.getY())),balls[i].getRadius())



def startPositions(balls):
        for i in range(len(balls)):
            balls[i] = physicalObject()
        #balls[1].Material.setColour(RED)
        balls[0].vectors.setY(balls[0].getRadius())
        balls[1].vectors.setY(height-balls[0].getRadius())
        balls[2].vectors.setX(width/4)
        #balls[4].vectors.setX(3*width/4)
        balls[1].Material.setColour(YELLOW)
        balls[0].Material.setColour(RED)
        balls[0].setRadius(40)
        balls[0].setMass(140)
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
                     if ((balls[i].getRadius() - balls[j].getRadius())**2 <= DistanceBetweenCentres and DistanceBetweenCentres <= (balls[i].getRadius()+balls[j].getRadius())**2):
                            balls[i].vectors.setX(balls[i].vectors.getX()-balls[i].vectors.getvX()*time)
                            balls[i].vectors.setY(balls[i].vectors.getY()-balls[i].vectors.getvY()*time)
                            balls[j].vectors.setX(balls[j].vectors.getX()-balls[j].vectors.getvX()*time)
                            balls[j].vectors.setY(balls[j].vectors.getY()-balls[j].vectors.getvY()*time)
                            balls[i].ballCollision(balls[j])
                            #print((balls[i].getRadius() - balls[j].getRadius())**2 <= DistanceBetweenCentres)
                            #P = (balls[i].vectors.getvX()*balls[i].getMass())+(balls[j].vectors.getvX()*balls[j].getMass())
                            #print(P)
       for i in range(len(balls)):
              balls[i].updateObject()
       return balls

if __name__ == "__main__":
       screen, fpsClock = initialise(width,height,my_caption,windowColour)
       balls = [None,None,None]
       balls = startPositions(balls)
       wall = material()
       while True:
              fpsClock.tick(tickspeed)
              render(screen,windowColour)
              pygame.display.update()
              balls = check(balls)
              for ball in balls:
                     ball.vectors.setvY(ball.vectors.getvY()-g)
              for event in pygame.event.get():
                     if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                     if event.type == MOUSEBUTTONDOWN:
                            balls = startPositions(balls)









