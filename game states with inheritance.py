import pygame as pg
import sys
import pygame.font
pygame.init()


#platform class-------------------------------------------------------------
class platform():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
       
    def draw(self, screen):
        pg.draw.rect(screen, (100, 250, 100), (self.xpos, self.ypos, 80, 30))
       
plats = [] #list to hold platforms

#goal class-------------------------------------------------------------
class goal():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def draw(self, screen):
        pg.draw.rect(screen, (250, 0, 0), (self.xpos, self.ypos, 20,20))

goals = [] #you can have more than one in each level :)

#--------------------------------------------------------------------------------

#player class
class player():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = 0
        self.yvel = 0
        self.isOnGround = False
       
    def draw(self, screen):
        pg.draw.rect(screen, (250, 0, 0), (self.xpos, self.ypos, 10, 30))
       
    def move_left(self):
        self.xvel = -5
       
    def move_right(self):
        self.xvel = 5
       
    def stop(self):
        self.xvel = 0
       
    def jump(self):
        if self.isOnGround == True:
            self.yvel = -8    
       
    def update(self, platforms):
       
        self.xpos += self.xvel
        self.ypos += self.yvel
       
        if self.collision(platforms):
            self.isOnGround = True
            self.yvel = 0

        else:
            self.isOnGround = False
       
        if self.ypos > 760:
            self.isOnGround = True
            self.yvel = 0
            self.ypos = 760
           
        if self.isOnGround == False:
            self.yvel+=.2
           
        for goal in goals:
            if self.xpos + 10 >= goal.xpos and self.xpos <= goal.xpos + 20:
                if self.ypos + 30 >= goal.ypos and self.ypos + 30 <= goal.ypos + 20:
                    print("goal hit!")
                    self.xpos = 100
                    self.ypos = 100
                    return True  # Change state when player touches a red square
           
    def collision(self, platforms):
        for plat in platforms:
            if self.xpos + 10 >= plat.xpos and self.xpos <= plat.xpos + 80:
                if self.ypos + 30 >= plat.ypos and self.ypos + 30 <= plat.ypos + 30:
                    return True
        return False
       
       
p1 = player(100,100)

#--------------------------------------------------------------------------------
#the parent class!
#stuff you want to persist should go in here (i.e. fonts, player health, etc)
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.font = pg.font.Font(None, 36)
       
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                p1.move_left()
            elif event.key == pg.K_RIGHT:
                p1.move_right()
            elif event.key == pg.K_UP:
                p1.jump()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                p1.stop()
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

#--------------------------------------------------------------------------------
class End(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'LevelOne'
       
    def cleanup(self):
        print('cleaning up End state stuff')
       
    def startup(self):
        print('starting End state stuff')

    def update(self, screen, dt):
        self.draw(screen)
        if p1.update(plats)==True:
            self.done = True
       
    def draw(self, screen):
        screen.fill((0,0,80))
        text = self.font.render("You Win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 400))  
        screen.blit(text, text_rect)

#--------------------------------------------------------------------------------

class LevelOne(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'LevelTwo'
       
       
    def cleanup(self):
        print('cleaning up Level 1 stuff')
        plats.clear();
       
    def startup(self):
        print('Level 1!')
        plats.append(platform(200, 400))
        plats.append(platform(500, 200))
        plats.append(platform(400, 500))
        plats.append(platform(100, 200))
        goals.append(goal(250, 350))
       

    def update(self, screen, dt):
        self.draw(screen)
        if p1.update(plats)==True:
            self.done = True
       
    def draw(self, screen):
        screen.fill((0,0,0))
        p1.draw(screen)
        for i in range (len(plats)):
            plats[i].draw(screen)
        for i in range (len(goals)):
            goals[i].draw(screen)
        text = self.font.render("Level 1", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 20))  
        screen.blit(text, text_rect)
       
       
#--------------------------------------------------------------------------------

class LevelTwo(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'End'
       
    def cleanup(self):
        print('cleaning up Level 2 stuff')
        plats.clear();
       
    def startup(self):
        print('Level 2!')
        plats.append(platform(100, 500))
        plats.append(platform(400, 300))
        plats.append(platform(400, 600))
        plats.append(platform(600, 700))
        goals.append(goal(250, 350))

    def update(self, screen, dt):
        self.draw(screen)
        if p1.update(plats)== True:
            self.done = True
       
    def draw(self, screen):
        screen.fill((0,0,255))
        p1.draw(screen)
        for i in range (len(plats)):
            plats[i].draw(screen)
        for i in range (len(goals)):
            goals[i].draw(screen)
        text = self.font.render("Level 2", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 20))  
        screen.blit(text, text_rect)
#--------------------------------------------------------------------------------      
class Control:
    def __init__(self, **settings): # ** denotes a KWARG, which lets you have an unknown num of parameters
        self.__dict__.update(settings) #double underscore helps to avoid naming conflicts in subclasses
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
       
       
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name] #state has been set to an OBJECT
       
       
    def flip_state(self):
        self.state.done = False #we are referencing the variable of whatever OBJECT is in "state"
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
       
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
       
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
           
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
 
#--------------------------------------------------------------------------------
#"main"
           
#a dictionary containing the settings
settings = {
    'size':(800,800),
    'fps' :60
}

#a dictionary containing all the different states available
state_dict = {
    'End': End(),
    'LevelOne': LevelOne(),
    'LevelTwo': LevelTwo()
}

#------------------------------------
#instantiate a control object named "app"
#after running this constructor, "app" will have 4 variables:
#a copy of the settings dictionary, a boolean named "done" set to False,
#a screen variable holding the pygame display, and a clock variable
app = Control(**settings)
#------------------------------------

#------------------------------------
#the setup_states function passes in the dictionary of available states
#and also sets what the begnning state will be
app.setup_states(state_dict, 'LevelOne')
app.state.startup() #call startup for the initial state, Level One
#------------------------------------

#------------------------------------
app.main_game_loop() #OMG GAME LUP!


pg.quit()
sys.exit()
