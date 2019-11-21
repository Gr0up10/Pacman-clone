import pygame
from objects.base import DrawObject
from objects.base_cell import Wall
from objects.base_cell import Floor

# Класс Поля, единственный на сцену, хранит Cell(Клетки)
class Field(DrawObject):

    # background_path - путь до картинки на фоне
    background_path = './images/background.png'

    # size - размер клетки, аргумент для создания клеток
    def __init__(self, game, size):

        self.game = game
        self.size = size
        self.image = pygame.image.load(self.background_path)

        #Матрица - текстовое представление игрового поля, карты хранятся в /maps
        self.matrix = []

        #Карта поля, в ней хранятся Cell(Клетки)
        self.map = []

        #Приведение текстовой карты к двумерному массиву
        with open('./maps/map1.txt', 'r') as file:
            lines = file.readlines()
            for row in lines:
                row = list(row)
                self.matrix.append(row[:len(row)-1])

        #Создание двумерного массива
        for i in range(len(self.matrix)):
            self.map.append([])

        #Заполнение map Cell(Клетками) в зависимости от буквы(символа) в матрице
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                # Каждая новая клетка "смещается" от предыдущей на size
                if self.matrix[row][col] == 'G':
                    self.map[row].append(Floor(self.game, col * self.size, row * self.size, True, self.size))
                elif self.matrix[row][col] == 'W':
                    self.map[row].append(Wall(self.game, col * self.size, row * self.size, False, self.size))

    #Отрисовка фона и каждой Cell(Клетки)
    def process_draw(self):
        self.game.screen.blit(self.image,(0,0))
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                self.map[row][col].process_draw()

    #Функция, возвращающаяя клетку по строке и столбцу
    def get_cell_iter(self, col, row):
        return self.map[row][col]

    #Функция, возвращающая клетку по координатам
    def get_cell_coord(self, x, y):
        for row in self.map:
            for col in row:
                if col.x == x and col.y == y:
                    return col