import pygame
import random
import math
import time

from pygame.locals import *

# Credit to Dr. Robert Collier for providing me with the original majority of this code!

# the window is the actual window onto which the camera view is resized and blitted
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 40
delta_time = 1 / frame_rate



# In normal code, we shouldn't use globals - but for prototyping it will make our life significantly easier.
game_data = {}

class GameCircle:
    def __init__(self, position, radius, velocity ,current):      #current_action
        self.position = position
        self.radius = radius
        self.colliding = False
        self.current = current
        self.velocity = velocity

class RotatingLine:
    def __init__(self, origin, angle, intervals):
        self.origin = origin        # This is the origin point that the line will rotate around
        self.angle = angle          # This is the initial angle that the line will face, in degrees
        self.intervals = intervals  # This is a list of tuples representing the visible segments that create gaps
        self.segments = []          # Represents the actual segments we'll draw, handled in update

        ### Intervals Example ###
        # An "intervals" variable of [ (0.00, 0.50), (0.75, 1.00) ] represents a line with a gap
        # starting halfway through the line, the gap is 25% of the length of the line, followed by
        # the remaining 25% being a collidable line.

class Firewall:
    def __init__(self ,origin, height, width, velocity):
        self.origin = origin           #original position on the screen where the  firewall will orignate from
        self.velocity= velocity        #the velocity at which the firewall will move across the screen, might increase with the longer the player survives in the game
        self.segments = []
        self.height= height
        self.width = width


def main():
    # initialize pygame.
    pygame.init()
    pygame.mixer.init()
    pygame.key.set_repeat(1, 1)
    # create the window and set the caption of the window
    screen = pygame.display.set_mode( ((SCREEN_WIDTH+100), (SCREEN_HEIGHT)) )
    pygame.display.set_caption('"Toy" for the MDA Exercise')

    # create a clock
    clock = pygame.time.Clock()

    initialize()

    # music
    music=pygame.mixer.music.load("Trapped.mp3")
    pygame.mixer.music.play(-1)
    
    # the game loop is a postcondition loop controlled using a Boolean flag
    while not game_data["quit_game"]:
        handle_inputs()
        update_position_circle() 
        update()
        render(screen)
        
        # This where the screen showing results is displayed before the game terminates

        if  game_data["hits"] >= game_data["health"]:
            
            screen.fill((0,0,0))
            score_text=("SCORE:  "+str(game_data["score"]))
            game_over=("GAME OVER ")
            message( game_over,[255,0,0],screen,[400,200])
            message( score_text,[255,0,0],screen,[400,250])
            screen.blit (game_data["why"],(400,300))
            pygame.display.update()
            time.sleep(3)
            game_data["quit_game"]=True
       
        clock.tick(frame_rate)
    
    print("GAME OVER \n"+"You're health is", (game_data["health"] - game_data["hits"]))  #294 is current highscore lol
    print("SCORE:  ",game_data["score"])

def initialize():
    # Setup all of our initial data for the game
    game_data["quit_game"] = False
    game_data["lines"] = []
    game_data["circles"] = []
    game_data["Top_firewalls"]= []
    game_data["Side_firewalls"]= []
    game_data["Bottom_firewalls"]= []
    game_data["Otherside_firewalls"]= []
    game_data["number_of_lines"]=0
    game_data["number_of_fw"]=0
    game_data["hits"]=0
    game_data["health"]=100
    game_data["score"]=0
    game_data["inc"]=[0,0,0,0,0]
    game_data["why"]=pygame.image.load("why.png")
    game_data["idle"]=pygame.image.load("character_malePerson_idle.png")
    game_data["hit"]=pygame.image.load("character_malePerson_hit.png")
    game_data["hit_sound"]=pygame.mixer.Sound("grunt.wav")
    # Just one line and one circle for the initial toy

    
    game_data["lines"].append( RotatingLine( (SCREEN_WIDTH, 0), 135, [ (0.00, 0.50), (0.75, 1.00) ] ) )
      
    game_data["Top_firewalls"].append( Firewall((0,0), 20, 100, 5  ) )

    game_data["circles"].append( GameCircle( (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 30 , 20, "NA") )

def update_position_circle():
    current_circle=game_data["circles"][0]
    v = current_circle.velocity
    x_position=current_circle.position[0]
    y_position=current_circle.position[1]
    current_pos = current_circle.current

    if current_pos=="LEFT":
        if  current_circle.position[0]-((current_circle.radius))<0:
            pass
        else:
            current_circle.position = (((x_position- v), y_position))
    if current_pos=="RIGHT":
        if current_circle.position[0]+((current_circle.radius))>800:   #prevents character from going out of bounds
            pass
        else:
            current_circle.position = (((x_position+ v), y_position))
    if current_pos=="UP":
        if current_circle.position[1]-((current_circle.radius))<0:
            pass
        else:
            current_circle.position = (((x_position), y_position-v))
    if current_pos=="DOWN":
        if current_circle.position[1]+((current_circle.radius))>600:    #prevents character from going out of bounds
            pass
        else:
            current_circle.position = (((x_position), y_position+v)) 
    
    return


def handle_inputs():
    # look in the event queue for the quit event
    events = pygame.event.get()
    key=False
    for event in events:
        if event.type == QUIT:
            game_data["quit_game"] = True
        
    #KEY INPUT DATA
    #=========================================
        current_circle=game_data["circles"][0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_data["quit_game"] = True
            if event.key == pygame.K_LEFT or event.key== pygame.K_a:
                current_circle.current = ("LEFT")             
            if event.key == pygame.K_RIGHT or event.key== pygame.K_d:
                current_circle.current = ("RIGHT")  
            if event.key == pygame.K_UP or event.key== pygame.K_w:
                current_circle.current = ("UP")  
            if event.key == pygame.K_DOWN or event.key== pygame.K_s:
                current_circle.current = ("DOWN") 
                
        elif event.type == pygame.KEYUP:            
            if event.key == pygame.K_LEFT or event.key== pygame.K_a:        
                key=True
            
            if event.key == pygame.K_RIGHT or event.key== pygame.K_d:     
                key=True

            if event.key == pygame.K_UP or event.key== pygame.K_w:         
                key=True

            if event.key == pygame.K_DOWN or event.key== pygame.K_s:          
                key=True
    if key:
        current_circle.current = ("NA")
    return key
#=========================================




########### DATA UPDATES ###########    
def update():
    line_did_reset = False
    
    # Rotate each line, and see if they reset at all
    for line in game_data["lines"]:
        line_did_reset = rotate_line(line)
        update_line_segments(line)
        
    # Now we'll update the data for our circle(s)
    # Presently, that means looking for collisions with other line segments
    for circle in game_data["circles"]:
        update_circle_line_collisions(circle)
       
    # The for loops below are used to detect collision of the ball with the firewalls
     
    for firewall in game_data["Top_firewalls"]:
        firewall_hit(firewall , game_data["circles"][0] )
        bot_firewall_hit(firewall , game_data["circles"][0] ) 

    for firewall in game_data["Side_firewalls"]:
        firewall_hit(firewall , game_data["circles"][0] )
        bot_firewall_hit(firewall , game_data["circles"][0] ) 

    for firewall in game_data["Bottom_firewalls"]:
        firewall_hit(firewall , game_data["circles"][0] )
        bot_firewall_hit(firewall , game_data["circles"][0] )    
       
    for firewall in game_data["Otherside_firewalls"]:
        firewall_hit(firewall , game_data["circles"][0] )
        bot_firewall_hit(firewall , game_data["circles"][0] )    



def rotate_line(line):
    # Rotate the line by 1 degree
    # Return TRUE if the line reset to 90 degrees, FALSE otherwise
    reset = False
    a = game_data["circles"][0]
    
    # increase the angle of the rotating line
    line.angle = (line.angle + 1)
    line1=game_data["lines"][0]
    
    

    # the rotating line angle ranges between 90 and 180 degrees
    if line1.angle > 180:
        # when it reaches an angle of 180 degrees, reset it 
        line.angle = 90
        reset = True
        game_data["number_of_lines"] += 1
        game_data["score"]+= 1

        #!!!!!!!Here I implemented the procees whereby the broken segments of the lines appear at different positions on the line
        random_pos=round((random.uniform(0.1,0.70)),2)
        line1=game_data["lines"][0]
        line1.intervals= [ (0.00, random_pos), ((random_pos+0.30), 1.00) ]
        
        # Here I add the second line 

        if game_data["number_of_lines"]==4:
            game_data["lines"].append( RotatingLine( (0, 0), 0, [ (0.00, 0.20), (0.50, 1.00) ] ) )
            a.velocity += 2
    
    if len(game_data["lines"])>1:
        line2=game_data["lines"][1]
        
        if line2.angle > 90:
            line2.angle = 0
            reset=True            
            
            game_data["score"]+= 1
            random_pos2=round((random.uniform(0.1,0.70)),2)
            line2.intervals= [ (0.00, random_pos2), ((random_pos2+0.30), 1.00) ]
    
        
    update_line_segments(line1)

    if len(game_data["lines"])>1:
        update_line_segments(line2)

    return reset

def update_line_segments(line):
    # This function is going to set up the coordinates for the enpoints
    # of each "segment" of our line.

    # The points associated with each line segment must be recalculated as the angle changes
    line.segments = []
    
    # consider every line segment length
    for partial_line in line.intervals:
        # compute the start of the line...
        sol_x = line.origin[0] + math.cos(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[0]    #SW 800
        sol_y = line.origin[1] + math.sin(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[0]
        
        # ...and the end of the line...
        eol_x = line.origin[0] + math.cos(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[1]
        eol_y = line.origin[1] + math.sin(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[1]
        

        # compute the start of the line...
        sol_x2 = line.origin[0] + math.cos(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[0]    #SW 800
        sol_y2 = line.origin[1] + math.sin(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[0]
        
        # ...and the end of the line...
        eol_x2 = line.origin[0] + math.cos(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[1]
        eol_y2 = line.origin[1] + math.sin(math.radians(line.angle)) * SCREEN_WIDTH * partial_line[1]
        # ...and then add that line to the list
        line.segments.append( ((sol_x, sol_y), (eol_x, eol_y)) )

def update_circle_line_collisions(circle):
    # Look at every line and see if the input circle collides with any of them; return if collided
    # Assume we aren't colliding
    circle.colliding = False

    # We'll need to look at each of our lines, if we had more than one
    # If any of them are colliding, we can break out because we only need one
    for line in game_data["lines"]:
        # Look at each segment of the line
        for segment in line.segments:                       #!!!!!!!!!!!!!!!!!!!
            if detect_collision_line_circ(segment, circle):   #!!!!!!!!!!!!!!!!!
                circle.colliding = True
                break
    
    return circle.colliding

  


########### RENDERING ###########
def render(screen):
    # clear the window surface (by filling it with black)
    screen.fill( (0,0,0) )

    
    #These set the health bar and the line separating the gameplay screen and display screen

    pygame.draw.rect(screen ,(255,255,255), [SCREEN_WIDTH,0, 2, SCREEN_HEIGHT ])
    pygame.draw.rect(screen ,(255,255,255), [(SCREEN_WIDTH+40)-3,147, 36, ((game_data["health"]*2)+6) ]) 
    pygame.draw.rect(screen ,(0,255,0), [(SCREEN_WIDTH+40),150, 30, (game_data["health"]*2) ])   # health bar
    pygame.draw.rect(screen ,(0,0,0), [(SCREEN_WIDTH+40),150, 30, (game_data["hits"]*2) ])         # decrease in health bar
    
    # thsi prints the messages(score and health) on the current gameplay screen
    score_txt=("SCORE ")
    ac_sc=(str(game_data["score"]))
    health_txt=("HEALTH")
    message( score_txt ,(135,206,235),screen,[810,500])
    message( ac_sc ,(135,206,235),screen,[830,530])
    message( health_txt ,(135,206,235),screen,[810,360])
    
    # Draw the line(s)
    for line in game_data["lines"]:
        render_line(screen, line)
    

    # Draw the circle(s)
    for circle in game_data["circles"]:
        render_circle_color(screen, circle)

    # Draw the firewalls
    for rect in game_data["Top_firewalls"]:
        render_top_firewall(screen, rect)
    
    for rect2 in game_data["Side_firewalls"]:
        render_side_firewall(screen, rect2)
    
    for rect3 in game_data["Bottom_firewalls"]:
        render_bottom_firewall(screen, rect3)
    
    for rect4 in game_data["Otherside_firewalls"]:
        render_otherside_firewall(screen,rect4)

    # update the display
    pygame.display.update() 


def render_top_firewall(screen, firewall):
    # This function draw the firewall coming from the top of the screen

    random_pos= random.randint(0,((SCREEN_WIDTH/100) - (firewall.width/100)))

    #I excluded the adding of the flame images to represent fire as it was making my game hang so please bear with the bland graphics :)
    '''
    fire_face=pygame.image.load("fire.png")
    fire=pygame.transform.scale(fire_face,(firewall.width, firewall.height))
    screen.blit(fire, (firewall.origin[0], firewall.origin[1]))
    '''
    pygame.draw.rect(screen, (255,201,33), [ firewall.origin[0], firewall.origin[1] , firewall.width, firewall.height] )
    
    if firewall.origin[1]<600:
        firewall.origin=(firewall.origin[0], firewall.origin[1]+ firewall.velocity)
        
    else:
        firewall.origin=((random_pos*100),0)
        game_data["number_of_fw"]+=1
        game_data["score"]+= 1
        if game_data["number_of_fw"]==10:                                           # The if functions below check whether enough firerewalls have been overcome by the player
            game_data["Side_firewalls"].append( Firewall((0,0), 100, 20, 4.5) )     # inorder to add the side firewalls and the bottom ones.

        if game_data["number_of_fw"]==15:
            game_data["Bottom_firewalls"].append( Firewall((0,600), 20, 100, 4.5) )

        if game_data["number_of_fw"]==20:
            game_data["Otherside_firewalls"].append( Firewall((0,0), 100, 20, 4.5 ) )

    if game_data["score"]==100 or game_data["score"]==150 or game_data["score"]==200:  # This function which is seen in each of the firewall functions is what increases
        if game_data["inc"][0]==0:                                                     # the speed of the firewalls as the players score increases (this what difficulty of the game)
            print("increased")
            game_data["inc"][0]+=1
            firewall.velocity+=0.3
    else:
        game_data["inc"][0]=game_data["inc"][0]-1   
        
    # The rest of the firewall functions are similar to the one explained above. They only differ in reset positions and direction of movement.

def render_side_firewall(screen, firewall):
    
    random_pos2= random.randint(0,(((SCREEN_HEIGHT)/100)-(firewall.height/100)))

    pygame.draw.rect(screen, (255,152,23), [ firewall.origin[0], firewall.origin[1] , firewall.width, firewall.height] )
    

    if firewall.origin[0]<800:
        firewall.origin=(firewall.origin[0]+ firewall.velocity , firewall.origin[1])
        
    else:
        firewall.origin=(0,random_pos2*100)
        game_data["score"]+= 1

    if game_data["score"]==100 or game_data["score"]==150 or game_data["score"]==200:
        if game_data["inc"][1]==0:
            print("increased")
            game_data["inc"][1]+=1
            firewall.velocity+=0.3
    else:
        game_data["inc"][1]=game_data["inc"][1]-game_data["inc"][1]  


def render_otherside_firewall(screen, firewall):
    inc=0
    random_pos4= random.randint(0,(((SCREEN_HEIGHT)/100)-(firewall.height/100)))

    pygame.draw.rect(screen, (255,152,23), [ firewall.origin[0], firewall.origin[1] , firewall.width, firewall.height] )    

    if firewall.origin[0]>0:
        firewall.origin=(firewall.origin[0]- firewall.velocity , firewall.origin[1])
        
    else:
        firewall.origin=(800-firewall.width ,random_pos4*100)
        game_data["score"]+= 1

    if game_data["score"]==100 or game_data["score"]==150 or game_data["score"]==200:
        if game_data["inc"][2]==0:
            print("increased")
            game_data["inc"][2]+=1
            firewall.velocity+=0.3
    else:
        game_data["inc"][2]=game_data["inc"][2]-game_data["inc"][2] 
        

def render_bottom_firewall(screen, firewall):
    
    random_pos3= random.randint(0,((SCREEN_WIDTH/100) - (firewall.width/100)))

    #random_pos2= random.randint((SCREEN_HEIGHT-firewall.height),0)
    
    pygame.draw.rect(screen, (255,152,23), [ firewall.origin[0], firewall.origin[1] , firewall.width, firewall.height] )
    

    if firewall.origin[1]>0:
        firewall.origin=(firewall.origin[0], firewall.origin[1] - firewall.velocity)
        
    else:
        firewall.origin=((random_pos3*100),600)
        game_data["score"]+= 1

    if game_data["score"]==100 or game_data["score"]==150 or game_data["score"]==200:
        if game_data["inc"][3]==0:
            print("bot increased")
            game_data["inc"][3]+=1
            firewall.velocity+=0.3
    else:
        game_data["inc"][3]=game_data["inc"][3]-game_data["inc"][3]
        

def render_line(screen, line):
    # draw each of the rotating line segments
    for seg in line.segments:
        pygame.draw.aaline(screen, (25, 255, 255), seg[0], seg[1])

# In the render circle function is where I implemented the character image to change upon impact and make a sound
def render_circle_color(screen, circle):
    inc=0
    # draw the circle hitbox, in red if there has been a collision or in white otherwise
    hit_face=game_data["hit"]
    hit=pygame.transform.scale(hit_face,(90,80))
    idle_face=game_data["idle"]
    idle=pygame.transform.scale(idle_face,(90,80))
    if circle.colliding:
        #pygame.draw.circle(screen, (255, 0, 0), circle.position, circle.radius)
        screen.blit(hit, ((circle.position[0]-45),circle.position[1]-50))
        game_data["hits"]+=1
        game_data["hit_sound"].play()
        
    else:
        #pygame.draw.circle(screen, (255, 255, 255), circle.position, circle.radius)
        screen.blit(idle, ((circle.position[0]-45),circle.position[1]-50))

    if game_data["score"]==100 or game_data["score"]==150 or game_data["score"]==200:   #This function increases the speed of the character to account for the increase in speed of the firewalls
        if game_data["inc"][4]==0:
            print("top increased")
            game_data["inc"][4]+=1
            circle.velocity+=1
    else:
        game_data["inc"][4]=game_data["inc"][4]-1  
       
#The function below is what I used to print out messages onto the screen

def message (text,color,screen, position ):
    font= pygame.font.SysFont(None, 28 )
    screen_text= font.render(text, True, color)
    screen.blit(screen_text, position)


############## CODE HELPERS ################

#The function below detects collision of the top of the firewalls with the character
def firewall_hit( firewall, circle):
    position=firewall.origin
    width= firewall.width
    height= firewall.height
    circle_pos=circle.position
    radius=circle.radius 
   
    if (circle_pos[1]-radius <= position[1]+height) and (circle_pos[1]-radius >= position[1]) :
        if(circle_pos[0]>= position[0]-radius) and (circle_pos[0]<= position[0]+width+radius):
            #print("touched")
            circle.colliding=True
            game_data["hits"]+=1 
    
    
#The function below detects collision of the bottom of the firewalls with the character
def bot_firewall_hit( firewall, circle):
    position=firewall.origin
    width= firewall.width
    height= firewall.height
    circle_pos=circle.position
    radius=circle.radius 
    #for i in range(position[0],(position[0]+width)):    
    if (circle_pos[1]+radius >= position[1]) and (circle_pos[1]+radius <= position[1]+height) :
        if(circle_pos[0]>= position[0]) and (circle_pos[0]<= position[0]+width):
            circle.colliding=True
            game_data["hits"]+=1



def detect_collision_line_circ(line_points, circle):
    # line_points is a pair of points, where each point is a tuple of (x, y) coordinates.
    # Eg. line_points = ( (0, 0), (100, 100) ) represents a line down and right.
    # circle is just a circle class
    
    # unpack u; a line is an ordered pair of points and a point is an ordered pair of co-ordinates
    (u_sol, u_eol) = line_points
    (u_sol_x, u_sol_y) = u_sol   #when is it that i can get the problem of both being zero
    (u_eol_x, u_eol_y) = u_eol   #when is it that i can get the problem of both being zero

    # unpack v; a circle is a center point and a radius (and a point is still an ordered pair of co-ordinates)
    (v_ctr, v_rad) = (circle.position, circle.radius)
    (v_ctr_x, v_ctr_y) = v_ctr

    # the equation for all points on the line segment u can be considered u = u_sol + t * (u_eol - u_sol), for t in [0, 1]
    # the center of the circle and the nearest point on the line segment (that which we are trying to find) define a line 
    # that is is perpendicular to the line segment u (i.e., the dot product will be 0); in other words, it suffices to take
    # the equation v_ctr - (u_sol + t * (u_eol - u_sol)) · (u_evol - u_sol) and solve for t
    if ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)==0:
        t=0
    else:    
        t = ((v_ctr_x - u_sol_x) * (u_eol_x - u_sol_x) + (v_ctr_y - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

    # this t can be used to find the nearest point w on the infinite line between u_sol and u_sol, but the line is not 
    # infinite so it is necessary to restrict t to a value in [0, 1]
    t = max(min(t, 1), 0)
    
    # so the nearest point on the line segment, w, is defined as
    w_x = u_sol_x + t * (u_eol_x - u_sol_x)
    w_y = u_sol_y + t * (u_eol_y - u_sol_y)
    
    # Euclidean distance squared between w and v_ctr
    d_sqr = (w_x - v_ctr_x) ** 2 + (w_y - v_ctr_y) ** 2
    
    # if the Eucliean distance squared is less than the radius squared
    if (d_sqr <= v_rad ** 2):
    
        # the line collides
        return True  # the point of collision is (int(w_x), int(w_y))
        
    else:
    
        # the line does not collide
        return False

    

if __name__ == "__main__":
    main()
