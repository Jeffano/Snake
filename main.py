import pygame
from pygame.locals import *
import random
import time

# pixel of the picture
SIZE = 40

# Background color
BACKGROUND_COLOR = (100, 168, 67)


# Creates an apple class
class Apple:

    # constructor for the apple class
    def __init__(self, background):
        self.background = background
        # loads the apple picture
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    # displays the apple on the window
    def draw(self):
        self.background.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # randomly move the apple to a different location on the window
    def move(self):
        # 1000 (X - Dimension) / 40 (Apple Pixel Dimension) = 25 * SIZE to be on the window; then 1 less
        self.x = random.randint(1, 24) * SIZE
        # 800 (X - Dimension) / 40 (Apple Pixel Dimension) = 20 * SIZE to be on the window; then 1 less
        self.y = random.randint(1, 19) * SIZE


# Snake class
class Snake:

    # constructor of the object
    def __init__(self, surface, length):
        self.length = length
        self.background = surface

        # method to load images into block variable
        self.block = pygame.image.load("resources/block.jpg").convert()

        # direction of which the snake starts
        self.direction = 'down'

        # a value inside the bracket is repeated by the length value
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    # function to increase teh length of the snake
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # draw block function
    def draw(self):
        # changes the color of the window, rgb values, can be found on Google
        # also applies the color and clears the screen
        self.background.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            # places the block image on the window(surface) blit(image name,(x position, y position))
            self.background.blit(self.block, (self.x[i], self.y[i]))

        # updates the window
        pygame.display.flip()

    # methods to move the snake in different directions
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    # method to automate the movement of the snake
    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        #
        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()


# Game class with its syntax
class Game:

    # Constructor of the Game object and initializes the game with the window
    def __init__(self):

        # initialize pygame
        pygame.init()

        # application name
        pygame.display.set_caption("Python Snake Game")

        # initializing the sound module
        pygame.mixer.init()

        # starts playing background music
        self.background_music()

        # size of the window
        self.surface = pygame.display.set_mode((1000, 800))

        # Creates an object for the snake class with the given parameters (surface and length)
        self.snake = Snake(self.surface, 1)

        # uses the draw method within the snake class
        self.snake.draw()

        self.apple = Apple(self.surface)

        self.apple.draw()

    # sound effect method
    def sound_effect(self, sound):
        # use sound for shorter audio
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def background_music(self):
        # use music for longer audio
        pygame.mixer.music.load("resources/bgmusic.mp3")
        pygame.mixer.music.play()

    def play(self):
        # calling the walk function
        self.snake.walk()

        # calling the apple draw function
        self.apple.draw()

        # displays the game score
        self.score()
        pygame.display.flip()

        # checks if snake is colliding with the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # calling the sound effect method
            self.sound_effect("eat")

            # calling to increase teh snake length
            self.snake.increase_length()

            # changing the snake location
            self.apple.move()

        # checks if snake is colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.sound_effect("boom")
                raise "Game Over"

    def exit_screen(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render("GAME OVER!", True, (255, 255, 255))
        self.surface.blit(line1, (350, 300))

        line2 = font.render(f"SCORE: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line2, (350, 350))

        line3 = font.render("Press ENTER To Play Again", True, (255, 255, 255))
        self.surface.blit(line3, (350, 400))

        line4 = font.render("Press ESCAPE To Exit", True, (255, 255, 255))
        self.surface.blit(line4, (350, 450))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    # function to run the game
    def move(self):

        # running is set to true
        running = True
        pause = False

        # running is always true, if false (when close is pressed), it quits the application
        while running:
            for event in pygame.event.get():

                # checks what keys are pressed
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        # creates a method for each button press, then it is taken to that button function, now it only
                        # changes the direction
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.exit_screen()
                pause = True
                self.reset()

            # every 0.2 seconds, snake moves, creates a delay
            time.sleep(0.2)

    def is_collision(self, x1, y1, x2, y2):
        if (x1 >= x2) and (x1 < x2 + SIZE):
            if (y1 >= y2) and (y1 < y2 + SIZE):
                return True
        return False

    def score(self):

        # picking the font
        font = pygame.font.SysFont('arial', 30)

        # Displaying the score which is basically teh length of the snake, last 3 numbers are the color choice
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))

        # blit is used to display information on the window
        self.surface.blit(score, (450, 10))


# main program
if __name__ == "__main__":
    # creates an object to call the Game class
    game = Game()

    # uses the object to call the run function
    game.move()
