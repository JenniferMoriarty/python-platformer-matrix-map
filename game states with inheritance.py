import pygame as pg
import sys

#--------------------------------------------------------------------------------
#the parent class!
#stuff you want to persist should go in here (i.e. fonts, player health, etc)
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
#-------------------------------------------------------------------------------- 
class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
#--------------------------------------------------------------------------------
class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
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
        self.state = self.state_dict[self.state_name]
        
    def flip_state(self):
        self.state.done = False
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
    'size':(600,400),
    'fps' :60
}

#a dictionary containing all the different states available
state_dict = {
    'menu': Menu(),
    'game': Game()
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
app.setup_states(state_dict, 'menu')
#------------------------------------

#------------------------------------
app.main_game_loop() #OMG GAME LUP!


pg.quit()
sys.exit()
