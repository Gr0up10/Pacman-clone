import pygame
from objects.base import DrawObject
from objects.base_cell import Wall
from objects.base_cell import Floor
from objects.base_cell import Meta


# Класс Поля, единственный на сцену, хранит Cell(Клетки)
class Field(DrawObject):

    # background_path - путь до картинки на фоне
    background_path = './assets/images/background.png'

    # size - размер клетки, аргумент для создания клеток
    def __init__(self, game, size):
        super().__init__(game)
        self.game = game
        self.size = size

        # Матрица - текстовое представление игрового поля, карты хранятся в assets/maps
        self.matrix = []

        # Карта поля, в ней хранятся Cell(Клетки)
        self.map = []

        # Приведение текстовой карты к двумерному массиву
        with open('./assets/maps/real_map.txt', 'r') as file:
            lines = file.readlines()
            for row in lines:
                row = list(row)
                self.matrix.append(row)

        # Создание двумерного массива
        for i in range(len(self.matrix)):
            self.map.append([])

        # Заполнение map Cell(Клетками) в зависимости от буквы(символа) в матрице
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                cell_pos = col * self.size, row * self.size
                # Каждая новая клетка "смещается" от предыдущей на size
                if self.matrix[row][col] == 'G':
                    self.map[row].append(Floor(self.game, *cell_pos, True, self.size))
                if self.matrix[row][col] == 'P':
                    self.map[row].append(Floor(self.game, *cell_pos, True, self.size, meta=Meta.pacman_spawn))
                elif self.matrix[row][col] == 'W':
                    self.map[row].append(Wall(self.game, *cell_pos, False, self.size))
                elif self.matrix[row][col] == 'S':
                    self.map[row].append(Floor(self.game, *cell_pos, True, self.size, meta=Meta.grain_small))
                elif self.matrix[row][col] == 'B':
                    self.map[row].append(Floor(self.game, *cell_pos, True, self.size, meta=Meta.grain_big))
                elif self.matrix[row][col] == 't':
                    self.map[row].append(
                        Floor(self.game, *cell_pos, True, self.size, meta=[Meta.teleport2]))
                elif self.matrix[row][col] == 'p':
                    self.map[row].append(
                        Floor(self.game, *cell_pos, True, self.size, meta=[Meta.teleport1]))

        self.find_turns()

    def find_turns(self):
        turn_patterns = [((0, 1), (1, 0)),
                         ((0, 1), (-1, 0)),
                         ((0, -1), (1, 0)),
                         ((0, -1), (-1, 0))]
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                for pat in turn_patterns:
                    accepted = True
                    for dir in pat:
                        if isinstance(self.get_cell_iter(col+dir[0], row+dir[1]), Wall):
                            accepted = False
                            break
                    if accepted:
                        self.get_cell_iter(col, row).meta.append(Meta.ghost_turn)

    # Отрисовка фона и каждой Cell(Клетки)
    def process_draw(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                self.map[row][col].process_draw()

    # Функция, возвращающаяя клетку по строке и столбцу
    def get_cell_iter(self, col, row):
        # If col or row is out range return wall
        if len(self.map) <= row or len(self.map[0]) <= col:
            return Wall(self.game, col * self.size, row * self.size, False, self.size)
        return self.map[row][col]

    # Return cell that exists in specified position
    def get_cell(self, pos):
        return self.get_cell_iter(int(pos.x//self.size), int(pos.y//self.size))

    def get_cells_by_type(self, cell_type, meta=None):
        cells = []
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                cell = self.get_cell_iter(col, row)
                if isinstance(cell, cell_type) and (meta is None or (meta in cell.meta)):
                    cells.append(cell)
        return cells

    # Return cells around some position
    def get_cells_around(self, pos):
        pos = (int(pos.x//self.size), int(pos.y//self.size))
        dirs = [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        return [self.get_cell_iter(pos[0] + direct[0], pos[1] + direct[1]) for direct in dirs]

    # Функция, возвращающая клетку по координатам
    def get_cell_coord(self, x, y):
        for row in self.map:
            for col in row:
                if col.x == x and col.y == y:
                    return col
