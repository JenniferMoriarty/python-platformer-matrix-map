import pygame
pygame.init()  
pygame.display.set_caption("platformer with inheritance")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

#--------------parent class--------------------------
class platform():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        
    def draw(self):
        pygame.draw.rect(screen, (100, 50, 100), (self.xpos, self.ypos, 80, 30))
        
    def move(self):
        pass 

#--------------child class---------------------------
class MovingBlock(platform): 
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.startX = self.xpos
        self.startY = self.ypos
        self.direction = 1
    
    def draw(self):
        pygame.draw.rect(screen, (200, 50, 100), (self.xpos, self.ypos, 80, 30))
        
    def move(self):
        if self.direction == 1:
            if self.xpos < self.startX:
                self.direction*=-1
            else:
                self.xpos-=.1
        else:
            if self.xpos>self.startX+200:
                self.direction*=-1
            else:
                self.xpos+=.1
        
        
#-----------------------main---------------------------

#instantiate some objects
b1 = platform(200, 300)
b2 = MovingBlock(400, 500)

while(1): #omg game lup---------
    b1.move()
    b2.move()
    
    #le render section
    screen.fill((0,0,0))
    b1.draw()
    b2.draw()

    pygame.display.flip()#this actually puts the pixel on the screen
    
pygame.quit()



