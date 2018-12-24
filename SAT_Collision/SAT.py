import pygame
import random
import time
import sys

from SAT_Collision import Square

class SAT_coll:
    pygame.init()

    def __init__(self):
        # colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # properties
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("monospace", 32)

        # setup
        self.size = self.width, self.height = 1080, 720
        self.screen = pygame.display.set_mode(self.size)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        pygame.display.set_caption("SAT")
        self.running = True

        # squares
        self.sqr_1 = Square.Square((50, 50), (self.screen_width * .25, self.screen_height * .5))
        self.sqr_2 = Square.Square((50, 50), (self.screen_width * .75, self.screen_height * .5))

        # extras
        self.click_down = False

        # start the game loop
        self.start_loop()

    def start_loop(self):
        while (self.running):
            self.update()

            self.clock.tick(0)
            self.handle_exit()


    def draw(self):
        # draws axis for square 1
        sqr_1_x_axis, sqr_1_y_axis = self.sqr_1.get_axes()
        pygame.draw.line(self.screen, self.WHITE, sqr_1_x_axis[0], sqr_1_x_axis[1])
        pygame.draw.line(self.screen, self.WHITE, sqr_1_y_axis[0], sqr_1_y_axis[1])

        # draws axis for square 2
        sqr_2_x_axis, sqr_2_y_axis = self.sqr_2.get_axes()
        pygame.draw.line(self.screen, self.WHITE, sqr_2_x_axis[0], sqr_2_x_axis[1])
        pygame.draw.line(self.screen, self.WHITE, sqr_2_y_axis[0], sqr_2_y_axis[1])

        # draws the squares
        pygame.draw.polygon(self.screen, self.RED, self.sqr_1.square_vertices)
        pygame.draw.polygon(self.screen, self.BLUE, self.sqr_2.square_vertices)

        if self.sqr_1.normals: # checks to see if the normals exist
            for a in range(1, len(self.sqr_1.normals)):
                print(self.sqr_1.normals[a - 1], self.sqr_1.normals[a])
                pygame.draw.line(self.screen, self.WHITE, self.sqr_1.normals[a - 1], self.sqr_1.normals[a])
            pygame.draw.line(self.screen, self.WHITE, self.sqr_1.normals[len(self.sqr_1.normals) - 1], self.sqr_1.normals[0])

    def input_event_handler(self):

        events = pygame.event.get()
        for event in events:
            pass

        if pygame.mouse.get_focused() != 0:
            if pygame.mouse.get_pressed()[0]:
                if self.mouse_over(self.sqr_1) and self.click_down == False:
                    self.sqr_1.move_square((pygame.mouse.get_pos()))
                    self.click_down = True
                if self.mouse_over(self.sqr_2) and self.click_down == False:
                    self.sqr_2.move_square((pygame.mouse.get_pos()))
                    self.click_down = True
            self.click_down = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            if keys[pygame.K_1]:
                self.sqr_1.rotate_square(0.2)
            if keys[pygame.K_2]:
                self.sqr_2.rotate_square(0.2)


    def mouse_over(self, square):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x > square.POSITION[0] - square.WIDTH * .5 and
            mouse_x < square.POSITION[0] + square.WIDTH * .5 and
            mouse_y > square.POSITION[1] - square.HEIGHT * .5 and
            mouse_y < square.POSITION[1] + square.HEIGHT * .5):
            return True
        return False

    def update(self):
        self.screen.fill(self.BLACK)

        self.input_event_handler()

        self.sqr_1.check_coll(self.sqr_2)
        self.sqr_2.check_coll(self.sqr_1)
        self.draw()

        pygame.display.update()


    def handle_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

sat = SAT_coll() # create the class object