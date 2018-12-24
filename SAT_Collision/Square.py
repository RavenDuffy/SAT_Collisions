import math
import pygame

class Square:
    pygame.init()

    def __init__(self, DIMENSIONS = (50, 50), POSITION = (0, 0), ROTATION = 0):
        self.normals = []
        self.DIMENSIONS = self.WIDTH, self.HEIGHT = DIMENSIONS[0], DIMENSIONS[1]
        self.POSITION = self.x, self.y = POSITION[0], POSITION[1] # also acts as the centre
        self.ROTATION = ROTATION

        self.square_vertices = [[POSITION[0] - DIMENSIONS[0] * .5, POSITION[1] - DIMENSIONS[1] * .5],
                                [POSITION[0] + DIMENSIONS[0] * .5, POSITION[1] - DIMENSIONS[1] * .5],
                                [POSITION[0] + DIMENSIONS[0] * .5, POSITION[1] + DIMENSIONS[1] * .5],
                                [POSITION[0] - DIMENSIONS[0] * .5, POSITION[1] + DIMENSIONS[1] * .5]]

        self.axes = Axis(self.POSITION, self.ROTATION)

    def rotate_square(self, ROTATION): # POINTS is square_vertices
        angle = math.radians(ROTATION)
        self.ROTATION += angle
        if self.ROTATION >= math.pi * 2:
            self.ROTATION = 0

        s = math.sin(angle)
        c = math.cos(angle)
        cx, cy = self.POSITION

        count = 0
        for p in self.square_vertices:
            # centres points
            x, y = p
            x -= cx
            y -= cy

            # rotate points
            nx = x * c - y * s
            ny = x * s + y * c

            # move points out
            x = nx + cx
            y = ny + cy
            self.square_vertices[count] = [x, y]
            count += 1

        self.axes.rotate_axes(ROTATION)

    def move_square(self, POSITION):
        old_pos = self.POSITION
        self.POSITION = POSITION

        # calculates differences between corner points and centre
        cur_vertices = []
        index = 0
        for v in self.square_vertices:
            cur_vertices.append(v)
            cur_vertices[index][0] = old_pos[0] - cur_vertices[index][0]
            cur_vertices[index][1] = old_pos[1] - cur_vertices[index][1]
            index += 1

        # adds differences to current corners
        self.square_vertices = [[POSITION[0] + cur_vertices[0][0], POSITION[1] + cur_vertices[0][1]],
                                [POSITION[0] + cur_vertices[1][0], POSITION[1] + cur_vertices[1][1]],
                                [POSITION[0] + cur_vertices[2][0], POSITION[1] + cur_vertices[2][1]],
                                [POSITION[0] + cur_vertices[3][0], POSITION[1] + cur_vertices[3][1]]]

        self.update_axis()

    def check_coll(self, other_sqr):
        if (abs(self.POSITION[0] - other_sqr.POSITION[0]) <= self.WIDTH * 2 and
            abs(self.POSITION[1] - other_sqr.POSITION[1]) <= self.HEIGHT * 2):
            self.normals = self.calc_normals()
        else:
            self.normals = []

    # the normals will be used as the separating/projection axes
    def calc_normals(self):
        normals = []

        for a in range(len(self.square_vertices)):
            normals.append(self.square_vertices[a].copy())
            # calculate the normals of each point
            # these can now be used as normal lines
            normals[a][1], normals[a][0] = normals[a][0], normals[a][1]
            normals[a][0] *= -1

        return normals

    def update_axis(self):
        self.axes.update(self.POSITION, self.ROTATION)

    def get_axes(self):
        return self.axes.get_axes()


class Axis:
    pygame.init()

    def __init__(self, POSITION = (0, 0), ROTATION = 0):
        self.POSITION = self.x, self.y = POSITION[0], POSITION[1]
        self.ROTATION = ROTATION

        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.x_axis = [[POSITION[0] - self.screen_width, POSITION[1]],
                       [POSITION[0] + self.screen_width, POSITION[1]]]
        self.y_axis = [[POSITION[0], POSITION[1] - self.screen_height],
                       [POSITION[0], POSITION[1] + self.screen_height]]
        self.axis = [self.x_axis, self.y_axis]

    def update(self, POSITION = (0, 0), ROTATION = 0):
        self.ROTATION = ROTATION
        self.POSITION = POSITION

        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.x_axis = [[POSITION[0] - self.screen_width, POSITION[1]],
                       [POSITION[0] + self.screen_width, POSITION[1]]]
        self.y_axis = [[POSITION[0], POSITION[1] - self.screen_width],
                       [POSITION[0], POSITION[1] + self.screen_width]]
        self.axis = [self.x_axis, self.y_axis]
        self.rotate_axes(math.degrees(self.ROTATION)) # needs to be degrees since its converted later

    def rotate_axes(self, ROTATION):
        for a in self.axis:
            angle = math.radians(ROTATION)
            self.ROTATION += angle
            if self.ROTATION >= math.pi * 2:
                self.ROTATION = 0

            s = math.sin(angle)
            c = math.cos(angle)
            cx, cy = self.POSITION

            count = 0
            for p in a:
                # centres points
                x, y = p
                x -= cx
                y -= cy

                # rotate points
                nx = x * c - y * s
                ny = x * s + y * c

                # move points out
                x = nx + cx
                y = ny + cy
                a[count] = [x, y]
                count += 1

    def get_axes(self):
        return self.axis