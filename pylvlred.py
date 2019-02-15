import os
import pygame
import random
from PIL import Image
import pygame.image as pim
cell_X = int(input())
if cell_X < 16:
    cell_X = 16
cell_Y = int(input()) + 12
cell_size = 16
pygame.init()
size = int(cell_X) * cell_size, int(cell_Y) * cell_size
print(size)
screen_size = int(cell_X) * cell_size, int(cell_Y) * cell_size
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


def load_image(texture_x, texture_y, cid):
        image = Image.open('blocks/tiles{}.png'.format(cid))
        x, y = texture_x * 16, texture_y * 16
        image = image.crop((x, y, x + 16, y + 16))
        img = pim.fromstring(image.tobytes('raw', 'RGBA'), (16, 16), 'RGBA')
        return img


blocks = []
for i in range(3):
    for j in range(16):
        blocks.append(load_image(j, i, 0))
items = []
for i in range(16):
    for j in range(8):
        items.append(load_image(j, i, 1))

class Field:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        print(self.height)
        self.brush = 0
        self.item_brush = 0

        self.board = [[-1] * width for _ in range(height)]
        self.item_board = [[-1] * width for _ in range(height)]
        a = -16
        for j in range(height - 12, height - 8):
            a += 16
            self.board[j] = [i + a for i in range(16)]
        a = -16
        for z in range(height - 8, height):
            a += 16
            self.item_board[z] = [i + a for i in range(16)]
        self.left = 0
        self.top = 0

        self.cell_size = 16

    def give(self):
        return self.board

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height - 12):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    pygame.draw.rect(screen, pygame.Color('green'),
                                     (
                                         x * self.cell_size + self.left,
                                         y * self.cell_size + self.top,
                                         self.cell_size,
                                         self.cell_size
                                     ), 1
                                     )
        for y in range(self.height - 9):
            for x in range(16):

                if self.board[y][x] > -1 and self.board[y][x] < 64:
                    screen.blit(blocks[self.board[y][x]], (x * self.cell_size + self.left, y * self.cell_size + self.top))
        for y in range(self.height - 12):
            for x in range(16):
                if self.item_board[y][x] > -1 and self.item_board[y][x] < 128:
                    screen.blit(items[self.item_board[y][x]],(x * self.cell_size + self.left, y * self.cell_size + self.top))
        for y in range(self.height - 9, self.height):
            for x in range(16):
                if self.item_board[y][x] > -1 and self.item_board[y][x] < 128:
                    screen.blit(items[self.item_board[y][x]], (x * self.cell_size + self.left, y * self.cell_size + self.top))


    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or \
            cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell, button):
        if not cell:
            return
        if button:
            if cell[1] in range(self.height - 12, self.height - 9):
                self.brush = self.board[cell[1]][cell[0]]
            else:
                self.board[cell[1]][cell[0]] = self.brush
        else:
            if cell[1] in range(self.height - 9, self.height):
                self.item_brush = self.item_board[cell[1]][cell[0]]
            if cell[1] in range(0, self.height - 12):
                self.item_board[cell[1]][cell[0]] = self.item_brush

    def get_click(self, mouse_pos, button):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, button)


class Levelmaker(Field):
    def __init__(self, width, height):
        super().__init__(width, height)


board = Field(int(cell_X), cell_Y)

time_on = False
ticks = 0
board.render()
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos, 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            board.get_click(event.pos, 0)
    board.render()
    pygame.display.flip()

    clock.tick(50)
    ticks += 1
pygame.quit()
plate = board.give()
codificator  = {'-1': None, '0': None, '1': 'brick_floor', '2': 'scnd_brick_floor', '3': 'hole', '4': 'brick_wall', '5': 'wood_door', '6': 'opened_door', '7': 'stair_up', '8': 'stair_down',
                '9': 'redstone', '10': 'locked_wood_door', '11': 'monolit', '12': 'tube', '13':'bamboo', '14': 'wood_floor', '15': 'thrd_brick_floor', '16': 'brick_wall',
                '17': 'green_plate', '18': 'brick_floor', '19': 'red_plate', '20': 'brick_floor', '21': 'orange_plate', '22': 'brick_floor', '23': 'used_spikes', '24': 'moody_floor',
                '25': 'steel_door', '26': 'steel_locked_door', '27': 'purpure_plate', '28': 'brick_floor', '29': 'tip', '30': 'red_plate', '31': 'brick_floor', '32': 'blue_plate',
                '33': 'brick_floor', '34': 'scnd_hole', '35': 'brick_monument', '36': 'wood_monument', '37': 'moody_plate', '38': 'brick_floor', '39': 'white_plate', '40': 'brick_floor',
                '41': 'book_shelf', '42': 'kolodecz', '43': 'pit', '44': 'pillar', '45': 'moody_wall', '46': 'moody_mono_wall', '47': 'brick_floor'}
ark = {'next level': input(), 'start_position': {}, "width": cell_X, "height": cell_Y, "board": []}









