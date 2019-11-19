import pygame
from objects.base import DrawObject
from objects.base_cell import UnWalkableCell
from objects.base_cell import WalcableCell
class Field(DrawObject):
    def __init__(self, game, size, background_path):
        self.game = game
        self.size = size
        self.matrix = [['B','B','B','B','B'],
                       ['B','B','W','B','B'],
                       ['B','B','W','B','B'],
                       ['B','B','B','B','B']]
        self.image = pygame.image.load(background_path)
        self.map = []
        for i in range(len(self.matrix)):
            self.map.append([])
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if self.matrix[row][col] == 'W':
                    self.map[row].append(WalcableCell(self.game, row*row, col*col, True, self.size))
                elif self.matrix[row][col] == 'B':
                    self.map[row].append(UnWalkableCell(self.game, row*row, col*col, False, self.size))
    def process_draw(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                self.map[row][col].process_draw()
    #
    # def ReadMatrix(self, path_to_matrix):
    #     file = open(path_to_matrix, 'r+')
    #     lines = file.readlines()
    #     for i in lines:
    #         self.matrix.append(i)


