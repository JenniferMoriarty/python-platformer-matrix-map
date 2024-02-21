import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Side-Scrolling Game')
clock = pygame.time.Clock()

#globals
player = [400, 450, 0, 0] #xpos, ypos, xvel, yvel
isOnGround = False
offset = 0

platforms = [(500, 400), (700, 300)]

def move_player():

      global isOnGround #needed to modify a global variable from within a function
      global offset
      print(player[0], offset)
      
      #assume we're in the air, but change it if needed
      isOnGround = False
      
      #check for ground collision
      if player[1] > 450: #reset player to ground
         player[1] = 450
         player[3] = 0
         isOnGround = True
         
        #platform collision
      for i in range(len(platforms)):
          if player[0]+50>platforms[i][0]+offset and player[0]<platforms[i][0]+100+offset and player[1]+50>platforms[i][1] and player[1]+50< platforms[i][1]+50:
              isOnGround = True #stop gravity
              player[1]=platforms[i][1]-50 #reset player's feet
              player[3] = 0 #stop downward velocity
              #print("on platform") #for testing
      
      if keys[pygame.K_LEFT]:
          if offset > 260 and player[0]>0: #check if you've reached the left edge of the map
              player[2] = -5 #let player approach side of game screen
              
          elif player[0]>400 and offset < -1500: #check if we're on the far right edge of the map
              player[2] = -5 #let player get back to the center of the game screen
                            
          elif player[0]>0: #if player is recentered, move the *offset*, not the player
              offset += 5
              player[2] = 0
              
          else:
              player[2]=0 #make sure motion is off (stops from going off edge)
             
    
      elif keys[pygame.K_RIGHT]:
          if offset < -1500 and player[0]<750:
              player[2] = 5
              
          elif offset >260 and player[0]<400:
              player[2] = 5
              
          elif player[0]<750:
              offset -= 5
              player[2] = 0
              
          else:
              player[2]=0
          
      #make sure player velocity is turned off if neither key is being pressed...       
      else:
          player[2] = 0
    

      # Jump mechanics
      if isOnGround == True and keys[pygame.K_UP]:
        player[3] = -15  # Player jumps
        isOnGround = False
        
    #apply gravity
      if isOnGround == False:
          player[3] += 1 #gravity
          
    #update player position
      player[0]+=player[2] #add x velocity to x position
      player[1]+=player[3] #add y velocity to y position
          
          
def draw_platforms():
    for i in range(len(platforms)):
        pygame.draw.rect(screen, (150, 10, 10), (platforms[i][0] + offset, platforms[i][1], 100, 30))
        
def draw_clouds():
    # Draw clouds in the background
    for x in range(100, 1800, 300): #this loop controls WHERE and HOW MANY clouds are drawn       
        for i in range(3): #draw 3 circles
            pygame.draw.circle(screen, (255, 255, 255), (x + offset, 100), 40)
            pygame.draw.circle(screen, (255, 255, 255), (x - 50 + offset, 125), 40)
            pygame.draw.circle(screen, (255, 255, 255), (x + 50 + offset, 125), 40)
        pygame.draw.rect(screen, (255, 255, 255), (x - 50 + offset, 100, 100, 65)) #flatten bottom edge
        
        
def draw_trees():
    
    for x in range(150, 1800, 300):
        pygame.draw.rect(screen, (50,50,0), (x-10+offset, 275, 20, 400)) #trunk
        for i in range(3): #draw 3 circles
            pygame.draw.circle(screen, (30, 130, 30), (x+offset, 275), 40)
            pygame.draw.circle(screen, (30, 130, 30), (x-40+offset, 310), 40)
            pygame.draw.circle(screen, (30, 130, 30), (x+40+offset, 310), 40)
        


running = True
while running: # Main game loop++++++++++++++++++++++++
    clock.tick(60)
    #input section--------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    
    #physics section+++++++++++++++++++++++++++++++++++
    move_player()
    # Render section+++++++++++++++++++++++++++++++++++
    screen.fill((135, 206, 235))  # Sky blue background
    draw_clouds() 
    draw_trees()
    draw_platforms()
    
    pygame.draw.rect(screen, (255, 0, 255), (player[0], player[1], 50, 50)) #player
    
    pygame.draw.rect(screen, (50, 150, 50), (0, 500, 800, 200)) #ground
    
    
    
    pygame.display.flip()

pygame.quit()


