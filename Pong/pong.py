import pygame #helps us make GUI games in python
import random #help us define which direction the ball will start moving in

BALL_WIDTH = 6/2
BALL_HEIGHT = 6/2
PADDLE_SPEED = 6
BALL_X_SPEED = 8
BALL_Y_SPEED = 5
FPS = 600
PADDLE_WIDTH = 5/2
PADDLE_HEIGHT = 30/2
#distance from the edge of the window
PADDLE_BUFFER = 10/2
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def drawBall(ballXPos, ballYPos):
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)


def drawPaddle1(paddle1YPos):
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle1)


def drawPaddle2(paddle2YPos):
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle2)


def updateBall(paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection):

    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED
    score = 0

    if (
                        ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddle1YPos and ballYPos - BALL_HEIGHT <= paddle1YPos + PADDLE_HEIGHT):
        #switches directions
        ballXDirection = 1
    #past it
    elif (ballXPos <= 0):
        #negative score
        ballXDirection = 1
        score = -1
        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    if (
                        ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= paddle2YPos and ballYPos - BALL_HEIGHT <= paddle2YPos + PADDLE_HEIGHT):
        #switch directions
        ballXDirection = -1
    #past it
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        #positive score
        ballXDirection = -1
        score = 1
        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]


    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

def updatePaddle1(action, paddle1YPos):
    if (action[1] == 1):
        paddle1YPos = paddle1YPos - PADDLE_SPEED
    if (action[2] == 1):
        paddle1YPos = paddle1YPos + PADDLE_SPEED

    if (paddle1YPos < 0):
        paddle1YPos = 0
    if (paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle1YPos


def updatePaddle2(paddle2YPos, ballYPos):
    if (paddle2YPos + PADDLE_HEIGHT < ballYPos + BALL_HEIGHT):
        paddle2YPos = paddle2YPos + PADDLE_SPEED
    if (paddle2YPos + PADDLE_HEIGHT > ballYPos + BALL_HEIGHT):
        paddle2YPos = paddle2YPos - PADDLE_SPEED
    if (paddle2YPos < 0):
        paddle2YPos = 0
    if (paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle2YPos


class PongGame:
    def __init__(self):
        #random number for initial direction of ball
        num = random.randint(0,9)
        #keep score
        self.tally = 0
        #initialie positions of paddle
        self.paddle1YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        #and ball direction
        self.ballXDirection = 1
        self.ballYDirection = 1
        #starting point
        self.ballXPos = WINDOW_WIDTH - BALL_WIDTH

        if(0 < num < 3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if (3 <= num < 5):
            self.ballXDirection = -1
            self.ballYDirection = 1
        if (5 <= num < 8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if (8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1
        num = random.randint(0,9)
        self.ballYPos = num*(WINDOW_HEIGHT - BALL_HEIGHT)/9

    def getPresentFrame(self):
        #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        screen.fill(BLACK)
        drawPaddle1(self.paddle1YPos)
        drawPaddle2(self.paddle2YPos)
        drawBall(self.ballXPos, self.ballYPos)
        #copies the pixels from our surface to a 3D array. we'll use this for RL
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.flip()
        #return our surface data
        return image_data

    #update our screen
    def getNextFrame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.paddle1YPos = updatePaddle1(action, self.paddle1YPos)
        drawPaddle1(self.paddle1YPos)
        #update evil AI paddle
        self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos)
        drawPaddle2(self.paddle2YPos)
        #update our vars by updating ball position
        [score, self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection] = updateBall(self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection)
        #draw the ball
        drawBall(self.ballXPos, self.ballYPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score
        print "Tally is " + str(self.tally)
        #return the score and the surface data
        return [score, image_data]
