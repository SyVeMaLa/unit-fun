from random import randrange
from collections import namedtuple
import msvcrt
import os
import sys


Pos = namedtuple('Pos', ['x', 'y'])


class Maze(object):
    offsets = {
        'up': Pos(0, -1),
        'right': Pos(1, 0),
        'down': Pos(0, 1),
        'left': Pos(-1, 0)
    }

    blow_direction = {'v': 'down', '^': 'up', '<': 'left', '>': 'right'}

    my_self = {'down': 'v', 'up': '^', 'left': '<', 'right': '>'}

    def __init__(self, maze_map, pos=None):
        self.grid = [list(line) for line in maze_map.split('\n')]
        if pos is not None:
            self.pos = pos
        else:
            self.pos = self.get_random_pos()
        self.self_image = '>'

    def can_move(self, direction):
        self.self_image = self.my_self[direction]

        new_x = self.pos.x + Maze.offsets[direction].x
        new_y = self.pos.y + Maze.offsets[direction].y

        try:
            target_cell = self.grid[new_y][new_x]
        except IndexError:
            return False
        if target_cell != ' ' and target_cell != 'X':
            return False
        return True

    def can_push(self, direction):
        new_x = self.pos.x + (Maze.offsets[direction].x * 2)
        new_y = self.pos.y + (Maze.offsets[direction].y * 2)

        if new_x <= 0 or new_x == len(self.grid[0])-1:
            print('don\'t push it!')
            return False
        if new_y <= 0 or new_y == len(self.grid)-1:
            print('don\'t push it!')
            return False
        try:
            target_cell = self.grid[new_y][new_x]
        except IndexError:
            return False
        if target_cell != ' ' and target_cell != 'X':
            return False
        return True

    def can_blow(self, direction):
        new_x = self.pos.x + Maze.offsets[direction].x
        new_y = self.pos.y + Maze.offsets[direction].y

        if new_x <= 0 or new_x >= len(self.grid[0]) - 1:
            print('don\'t blow it!')
            return False
        if new_y <= 0 or new_y >= len(self.grid) - 1:
            print('don\'t blow it!')
            return False
        return True

    def move(self, direction):
        if not self.can_move(direction):
            raise IndexError
        new_x = self.pos.x + Maze.offsets[direction].x
        new_y = self.pos.y + Maze.offsets[direction].y
        self.pos = Pos(new_x, new_y)
        # self.self_image = self.my_self[direction]

    def push(self, direction):
        stone_x = self.pos.x + Maze.offsets[direction].x
        stone_y = self.pos.y + Maze.offsets[direction].y
        new_x = self.pos.x + (Maze.offsets[direction].x*2)
        new_y = self.pos.y + (Maze.offsets[direction].y*2)

        self.grid[stone_y][stone_x] = ' '
        self.grid[new_y][new_x] = '#'
        self.pos = Pos(stone_x, stone_y)
        self.self_image = self.my_self[direction]

    def blow_up(self, direction):
        stone_x = self.pos.x + Maze.offsets[direction].x
        stone_y = self.pos.y + Maze.offsets[direction].y
        self.grid[stone_y][stone_x] = ' '

    def at_exit(self):
        return self.grid[self.pos.y][self.pos.x] == 'X'

    def get_random_pos(self):
        height = len(self.grid)
        width = len(self.grid[0])
        new_pos = Pos(randrange(width), randrange(height))
        while self.grid[new_pos.y][new_pos.x] != ' ':
            new_pos = Pos(randrange(width), randrange(height))
        return new_pos

    def display(self):
        os.system('cls')
        for ridx, row in enumerate(self.grid):
            line_chars = []
            for colidx, ch in enumerate(row):
                if Pos(colidx, ridx) == self.pos:
                    line_chars.append(self.self_image)
                else:
                    line_chars.append(ch)
            print(''.join(line_chars))


MAP = """#####################################
# #       #       #     #         # #
# # ##### # ### ##### ### ### ### # #
#       #   # #     #     # # #   # #
##### # ##### ##### ### # # # ##### #
#   # #       #     # # # # #     # #
# # ####### # # ##### ### # ##### # #
# #       # # #   #     #     #   # #
# ####### ### ### # ### ##### # ### #
#     #   # #   # #   #     # #     #
# ### ### # ### # ##### # # # #######
#   #   # # #   #   #   # # #   #   #
####### # # # ##### # ### # ### ### #
#     # #     #   # #   # #   #     #
# ### # ##### ### # ### ### ####### #
# #   #     #     #   # # #       # #
# # ##### # ### ##### # # ####### # #
# #     # # # # #     #       # #   #
# ##### # # # ### ##### ##### # #####
# #   # # #     #     # #   #       #
# # ### ### ### ##### ### # ##### # #
# #         #     #       #       # #
#X###################################"""


if __name__ == "__main__":
    # maze = Maze(MAP, Pos(1, 20))
    maze = Maze(MAP)

    possible_inputs = {
        'H': 'up',
        # 'up': 'up',
        'M': 'right',
        # 'right': 'right',
        'P': 'down',
        # 'down': 'down',
        'K': 'left'  # ,
        # 'left': 'left'
    }

    while not maze.at_exit():
        maze.display()
        print('Use arrows to move or (b) to blow up blocks \n(x) for exit')
        while True:  # Loop until we get correct input
            user_input = msvcrt.getwch()
            if user_input == 'x':
                print('Thank you and good night!')
                sys.exit(0)
            elif user_input == 'b':
                if maze.can_blow(maze.blow_direction[maze.self_image]):
                    maze.blow_up(maze.blow_direction[maze.self_image])
                break
            elif user_input in possible_inputs:
                user_direction = possible_inputs[user_input]
                if not maze.can_move(user_direction):
                    if maze.can_push(user_direction):
                        maze.push(user_direction)
                    else:
                        print('You can\'t move {}.'.format(user_input))
                else:
                    maze.move(user_direction)
                break
            else:
                if not not maze.at_exit():
                    print('You should not enter %s!' % user_input)

    print('You have found the exit!')
