import pygame
import time as t
from random import randint

pygame.init()


global SCALE_FACTOR
SCALE_FACTOR = 2 #relative to screen size

#OBSTACLE_SPACING = 4 * 50 * SCALE_FACTOR


class Window():
    def __init__(self):
        self.width = 450 * SCALE_FACTOR#width of window
        self.height = 250 * SCALE_FACTOR#height of window
        self.caption = "Game"#Name of window
        self.end_pic = pygame.image.load("game_over3.PNG")
        #self.end_pic.set_colorkey((0, 0, 0))
        self.create()
        
    def create(self):
        self.window = pygame.display.set_mode((self.width, self.height))#displays the window
        #self.window.fill(self.colour)
        pygame.display.set_caption(self.caption)
        background_image = pygame.image.load("ocean3.JPG")
        self.background = pygame.transform.scale(background_image, (self.width, self.height))
        self.position_of_image = 0 , 0
        self.window.blit(self.background, (self.position_of_image))
        
        
    def draw(self, position_x, position_y, image):
        x = position_x
        y = position_y
        width = image.get_rect()[2]
        height = image.get_rect()[3]
        self.window.blit(image, [x, y, width, height])

    def flip(self):
        pygame.display.flip()
        #self.window.fill(self.colour)
        self.window.blit(self.background, (self.position_of_image))

    def game_over(self):
        return True


    def draw_game_over(self):
        if self.game_over() == True:
            width = self.end_pic.get_rect()[2]
            height = self.end_pic.get_rect()[3]
            self.end_pic = pygame.transform.scale(self.end_pic, ((int(width/2)), height))
            width = int(width/2) # Update width
            self.window.blit(self.end_pic, [((self.width/2) - (width/2)), (self.height/2) - (height/2), width, height])
            

    def border(self, myfish):
        if myfish.position_y >= self.height - myfish.image_height:
            self.game_over()
            return True
        
            


class Fish():
    def __init__(self, window):
        self.position_x = 210
        self.position_y = 0
        self.velocity = 1000
        self.file = "fish.PNG"
        self.initial_velocity = 90
        self.jump_velocity = -120
        self.traj_start_time = 0
        self.initial_position = 210
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(self.file)
        self.image = pygame.transform.scale(self.image, (18 * SCALE_FACTOR , 18 * SCALE_FACTOR))
        self.image_width = self.image.get_rect()[2]
        self.image_height = self.image.get_rect()[3]

    def movement(self, time):
        if window.height < (self.position_y + self.image_height): # Stops fish falling through border.
            self.initial_position = window.height - self.image_height
            self.initial_velocity = 0
            self.traj_start_time = time
            
        elif self.position_y < 0:
            self.initial_position = 0
            self.initial_velocity = 0
            self.traj_start_time = time

        time_since_traj_began = time - self.traj_start_time      # WE FIND HOW LONG IT IS FALLING AS SPEED INCREASES WITH TIME (LOGIC OF ACCELERATION)
        self.position_y = self.initial_position + ((self.initial_velocity * time_since_traj_began) + (0.5 * +119.81 * (time_since_traj_began ** 2)))#calculate new position of fish
                    

        
    def event(self, time):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.traj_start_time = time
                    self.initial_velocity = self.jump_velocity
                    self.initial_position = self.position_y
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

class Obstacle():
    def __init__(self, position_y, window_width, offset):
        self.speed = 100
        self.position_y = position_y
        self.position_x = (window_width - 100)
        self.file = "obstacle.PNG"
        self.image1, self.image1_width, self.image2_height = self.load_image(self.file)
        self.image2, self.image2_width, self.image2_height  = self.load_image(self.file)
        self.reset_time = 0
        self.offset = window_width + offset
        self.rotate()

    def load_image(self, file):
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, (40 * SCALE_FACTOR , 274 * SCALE_FACTOR))
        image_width = image.get_rect()[2]
        image_height = image.get_rect()[3]
        return image, image_width, image_height

    def rotate(self):
        self.image2 = pygame.transform.rotate(self.image2, 180)

    def movement(self, window):
        time_since_reset = (time - self.reset_time)
        distance = (self.speed * time_since_reset)
        self.position_x = (-distance + self.offset)

    def setxposition(self, x_pos):
        self.reset_time = time
        self.offset = x_pos
        


class ObstacleManager():
    def __init__(self, window_height, window_width):
        flag1 = False
        flag2 = False
        flag3 = False
        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3
        self.flags = []
        self.flags.append(flag1)
        self.flags.append(flag2)
        self.flags.append(flag3)

        self.obstacles = []
        self.window_height = window_height
        for number in range(0, 3):
            real_obstacle_spacing = OBSTACLE_SPACING * number
            myobstacle = Obstacle(randint(0,window_height), window_width, real_obstacle_spacing)
            self.obstacles.append(myobstacle)
        self.position()
    
    def position(self):
        self.obstacles[1].position_x += 100
        self.obstacles[2].position_x += 200

        
    def sketch(self, window, myobstacle):
        window.draw(myobstacle.position_x, myobstacle.position_y + 50, myobstacle.image1)
        window.draw(myobstacle.position_x, (myobstacle.position_y - 50 - myobstacle.image2_height), myobstacle.image2)

    def draw(self, window):
        for item in range(0, 3):
            self.sketch(window, self.obstacles[item])
        

    def movement(self, window):
        for item in range(0, 3):
            self.obstacles[item].movement(window)
        
    def conveyor_belt(self, window):
        for item in range (0,3):
            if self.obstacles[item].position_x < -(self.obstacles[item].image1_width):
                self.obstacles[item].setxposition(window.width + OBSTACLE_SPACING)
                self.obstacles[item].position_y = randint(0, self.window_height)
                

    def obstacle_collision(self, myfish, window):
        for item in range(0, 3):
            x = False
            y = False
            rect1 = myfish.image.get_rect()
            rect1[0] = myfish.position_x
            rect1[1] = myfish.position_y###Position of Fish
            rect2 = self.obstacles[item].image1.get_rect()
            rect2[0] = self.obstacles[item].position_x
            rect2[1] = self.obstacles[item].position_y + 50###Position of Obstacle 1
            rect3 = self.obstacles[item].image2.get_rect()
            rect3[0] = self.obstacles[item].position_x
            rect3[1] = self.obstacles[item].position_y - 50 - self.obstacles[item].image2_height###Position of Obstacle 2
            x = self.collision(rect1, rect2)#Checks if fish colided with obstacle1
            y = self.collision(rect1, rect3)#Checks if fish colided with obstacle2

            if x == True or y == True:
                window.game_over()
                return True
        return False #Returns if it has colided

    def collision(self, rect1, rect2):
        collision = False#Asume no collision at start
        x = 0
        y = 1
        w = 2
        l = 3
        
        if rect1[x] >= rect2[x] and rect1[x] <= rect2[x] + rect2[w] and rect1[y] >= rect2[y] and rect1[y] <= rect2[y] + rect2[l]:###Creates boundaries for each point of a rectangle of fish in comparision for that of obstacles
            collision = True
        elif rect1[x] + rect1[w] >= rect2[x] and rect1[x] + rect1[w] <= rect2[x] + rect2[w] and rect1[y] >= rect2[y] and rect1[y] <= rect2[y] + rect2[l]:
            collision = True
        elif rect1[x] >= rect2[x] and rect1[x] <= rect2[x] + rect2[w] and rect1[y] + rect1[l] >= rect2[y] and rect1[y] + rect1[l] <= rect2[y] + rect2[l]:
            collision = True
        elif rect1[x] + rect1[w] >= rect2[x] and rect1[x] + rect1[w] <= rect2[x] + rect2[w] and rect1[y] + rect1[l] >= rect2[y] and rect1[y] + rect1[l] <= rect2[y] + rect2[l]:
            collision = True

        return collision

    def score_system(self, score, fish):
        
        for obstacle_number in  range(0,3):#Goes through all obstacles
            if self.flags[obstacle_number] != True:
                if self.obstacles[obstacle_number].position_x + self.obstacles[obstacle_number].image1_width <= fish.position_x:#Checks if fish passes obtacle
                    score += 1 #Add to score 1
                    self.flags[obstacle_number] = True
            if self.obstacles[obstacle_number].position_x > fish.position_x + fish.image_width:#After fish passes one obstacle, we reset boolean as we dont want every frame to add 1 to score
                self.flags[obstacle_number] = False
        return score
            

class TextDisplay():
    def __init__(self, score, colour, size):
        self.score = score
        self.colour = colour
        self.size = size

        
    def display(self, window):
        window.window.blit(self.text, (100, 100))

    def update_score_display(self, score):
        self.score = score
        
        font = pygame.font.SysFont("comicsansms" , self.size)
        self.text = font.render(str(self.score), True, self.colour)

        
        
        
        
            



    
        
        
window = Window()
OBSTACLE_SPACING = (window.width / 2)
myfish = Fish(window)
obstaclemanager = ObstacleManager(window.height, window.width)
score = 0
displaytext = TextDisplay(score, (255,0,0) , 100)
#Update text image when score changes.


dead = False
time_stamp = t.time()
while dead == False:
    time = t.time() - time_stamp
    

    # Drawing a single frame
    is_game_over = window.border(myfish)
    if is_game_over == None:
        is_game_over = obstaclemanager.obstacle_collision(myfish, window)
    myfish.movement(time)
    myfish.load_image()
    myfish.event(time)
    window.draw(myfish.position_x, myfish.position_y, myfish.image)
    obstaclemanager.movement(window)
    obstaclemanager.conveyor_belt(window)
    obstaclemanager.draw(window)
    score = obstaclemanager.score_system(score, myfish)
    displaytext.update_score_display(score)
    displaytext.display(window)
##    displaytext.display(window)
    #print(score)
        
    # Display the frame
    if is_game_over == False:
        window.flip()
    # -----------------------
    if is_game_over == True:
        window.draw_game_over()
        window.flip()
        t.sleep(2)
        pygame.quit()
        exit()






####TO DO
        #determine automatically how many obstacles can fit in a screen of x width
        #score system
        #better porpotrions of gap
        #better pictures
        #SQL database



###Refrences
        #https://nerdparadise.com/programming/pygame/part5
