import pygame
import random
import time
pygame.init()
from pygame import mixer
mixer.init()

#RGB COLORS
black = (0,0,0)
green = (10,150,0)
camogreen = (100, 150, 100)
#This creates a pygame window the size of 1280 by 800 pixels
screen = pygame.display.set_mode((1280,800))
#SOUNDS
#Background music
#This plays the music file and puts it on loop
musico = mixer.music.load("background music.wav")
pygame.mixer.music.set_volume(0.1)
mixer.music.play(-1)
#Eat food sound
eat = mixer.Sound("eat.wav")
eat.set_volume(0.8)
#Gameover sound
#then I lower the volume of the sound a bit
jameover = mixer.Sound("game over.wav")
jameover.set_volume(0.1)
#This sets the title of the window to Snake
pygame.display.set_caption("Snake")


#this contains all the x and y information, for the snake to be able to move
#it is set at the middle of the window with these values
#The snake y and x change is basically a value that we will add to the x and y coordinates so the snake can move
#The direction will be set later
SnakeX = 640
SnakeY = 400
SnakeX_change = 0
SnakeY_change = 0
Direction = ""
length = 10
snakespeed = 4


#The food
foodx = round(random.randrange(50, 1175))
foody = round(random.randrange(50, 700))


#Snake body list that stores all the (x,y) coordinates of each length
snakebody = []
def Drawbody():
    global bodypart
    # here we are inserting the coordinates of the first snake part in the list
    snakebody.insert(0, (SnakeX, SnakeY))
    # here this makes it so that the body cannot exceed the length that I want it to be so it removes the tail of the snake when its bigger than the length
    if len(snakebody)>=length:
        snakebody.pop()
        # here we make it so that for every single coordinate values in the list we draw a rectangle at the coordingates of the moving head
    for bodypart in snakebody:
        pygame.draw.rect(screen, (10,111,102), (bodypart[0],bodypart[1], 25, 25))


#SCORE
#Here I create a variable for the score value
#I choose my font and put it in the font variable
#I also choose the x and y coordinates and its roughly placed in the middle
Score1 = 0
font = pygame.font.Font('Pixeland.ttf',36)
bfont = pygame.font.Font('LLPIXEL3.ttf',100)
ScoreX = 618
ScoreY = 10
scoretime = 0.1
scoretimeX = 50
scoretimeY = 10
#This function basically renders the score on the screen, and you choose the colors of the font in rgb
def score(x,y):
    score = font.render("Score: " + str(Score1), True, (0,0,0))
    screen.blit(score,(x,y))
#This renders another type of score every second which is 1/100 because the game is running at 100 fps
#the score is then rounded and stored in another variable which is then displayed on the screen
def scoret(x,y):
    global scoretime
    if scoretime > 0:
        if Direction != "":
            scoretime+=(1/100)
        scoretimestr = round(scoretime)
        scoret = font.render("Time: " + str(scoretimestr), True, (0, 0, 0))
        screen.blit(scoret, (x, y))
# This will display GAME OVER after the player loses
#Same thing as above with the fonts and coordinates
#This pulls up a big game over text and plays the gameover sound
gameoverX = 350
gameoverY = 300
def gameovertxt(x,y):
    global playsound
    playsound = True
    if gamestate == "over":
        if playsound:
            jameover.play()
            playsound = False
        gameovertxt = bfont.render("GAME OVER", True, (0, 0, 0))
        screen.blit(gameovertxt, (x,y))

#This makes the text pop up explaining to the user what to do
plx = 475
ply =400
def playagainf(x,y):
    if gamestate == "over":
        playagain = font.render("Press Enter To Play again", True, (0, 0, 0))
        screen.blit(playagain, (x,y))


def gameover(x,y):
    global SnakeX_change,SnakeY_change, bodypart, gamestate, Direction
    # This makes it so that if the snake hits the maximum amount of pixels displayed - the size of the snake
    # So that we can still see the snake
    # The snake change values will be 0 and the snake wont be able to move again
    if SnakeX <= 50 or SnakeX >= 1175+25:
        SnakeX_change = 0
        SnakeY_change = 0
        gamestate = "over"
        Direction = ""
    if SnakeY <= 50 or SnakeY >= 700+25:
        SnakeY_change = 0
        SnakeX_change = 0
        gamestate = "over"
        Direction = ""
    #If the snake head coordinates are near the body it will stop movving
    #I use the enumerate function to make it so that we can skip the first 9 squares since they are always touching the head
    for index,bodypart in enumerate(snakebody):
            if index <10:
                continue
            #here is if the snake head is equal to the body it will stop moving, change direction variable for score
            if SnakeX <= bodypart[0]+(25/2) <= SnakeX +10:
                if SnakeY <=  bodypart[1]+(25/2) <= SnakeY+10:
                    SnakeY_change = 0
                    SnakeX_change = 0
                    gamestate = "over"
                    Direction = ""


#this variable will be used later when the game is over and the player wants to stop playing
gamestate = "running"
#This makes sure the window doesnt crash until you press the X/quit button on the top right
run =  True

while run:
    # This sets the screen color in RGB format and refreshes the screen to show the new background color
    #Also draws a border around the screen
    screen.fill((camogreen))
    pygame.draw.rect(screen, black, [50, 50, 1175, 700], 10)
    #EVENT CHANGES
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #If the user clicks on a button it will make the x and y change values either increase or decrease depending on which button is pressed
        # Then the direction changes, so that we cant move backwards at any time so that the snake doesntt hit itself
        # this is done by making the if statement see if the direction is opposite or not,
        # if its opposite the snake will continue moving in the same direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and Direction != "right":
                SnakeX_change = -snakespeed
                SnakeY_change = 0
                Direction = "left"
            if event.key == pygame.K_RIGHT and Direction != "left":
                SnakeX_change = snakespeed
                SnakeY_change = 0
                Direction = "right"
            if event.key == pygame.K_UP and Direction != "down":
                SnakeY_change = -snakespeed
                SnakeX_change = 0
                Direction = "up"
            if event.key == pygame.K_DOWN and Direction != "up":
                SnakeY_change = snakespeed
                SnakeX_change = 0
                Direction = "down"

    #This makes it so that the the x and y coordinates of the snake change according to the key clicked
    SnakeX += SnakeX_change
    SnakeY += SnakeY_change

    #This will call the draw body function which will put the values of SnakeX and SnakeY and create a block behind it which will follow it
    Drawbody()
    # this draws the snake head in the middle of the window
    pygame.draw.rect(screen, black, [SnakeX, SnakeY, 25, 25])

    # FOOD
    food = pygame.draw.rect(screen, green, [foodx, foody, 25, 25])


    #This makes it so that when the snake hits the food it moves to another place
    if SnakeX <= foodx+(25/2) <= SnakeX + 30 and SnakeY <= foody+(25/2) <= SnakeY+ 30:
        #this makes the sound play
        eat.play()
        foodx = round(random.randrange(50, 1175))
        foody = round(random.randrange(50, 700))#so that it doesnt appear behind score
        #This will increase length size by ten which will increase the limit of the body
        #the score also increases when the snake eats the food
        length += 10
        Score1 += 1


    #Here I call all my functions and display the screen after that
    gameover(gameoverX,gameoverY)
    gameovertxt(gameoverX,gameoverY)
    playagainf(plx, ply)
    scoret(scoretimeX,scoretimeY)
    score(ScoreX,ScoreY)
    pygame.display.update()
    #time sleeps so the game will use less resources and the game will run at 100fps
    time.sleep(1 / 100)
    #This will ask the player to play again and if they click enter it will restart the game
    if gamestate == "over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #This resets all the important variables back to the values they were before so you can restart the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    time.sleep(1)
                    gamestate = "running"
                    SnakeX = 640
                    SnakeY = 400
                    foodx = round(random.randrange(50, 1175))
                    foody = round(random.randrange(50, 700))
                    Score1 = 0
                    scoretime = 0.1
                    length = 10
                    snakebody = []
                    Direction = ""
                    pygame.display.update()
                    continue