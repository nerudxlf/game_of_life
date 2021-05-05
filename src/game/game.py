import pygame

from src.data.config import white, name, black, green


class Game:
    def __init__(self, width: int = 360, height: int = 360, cell_size: int = 10, speed: int = 10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_line(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, white, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, white, (0, y), (self.width, y))

    def create_grid(self) -> list:
        grid = []
        for i in range(self.width // self.cell_size):
            line = []
            for j in range(self.height // self.cell_size):
                line.append(0)
            grid.append(line)
        return grid

    def draw_first_grid(self) -> list:
        draw = True
        grid = self.create_grid()
        while draw:
            for i in pygame.event.get():
                if i.type == pygame.KEYUP and i.key == pygame.K_SPACE:
                    draw = False
                if i.type == pygame.MOUSEBUTTONUP and i.button == 1:
                    x, y = i.pos[0] // self.cell_size, i.pos[1] // self.cell_size
                    grid[x][y] = 1 if grid[x][y] == 0 else 0
                    if grid[x][y] == 1:
                        pygame.draw.rect(self.screen, green,
                                         (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                    else:
                        pygame.draw.rect(self.screen, white,
                                         (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                    pygame.display.flip()
        return grid

    def draw_grid(self, grid: list) -> None:
        for x in range(0, self.width, self.cell_size):
            for y in range(0, self.height, self.cell_size):
                if grid[x // self.cell_size][y // self.cell_size] == 1:
                    pygame.draw.rect(self.screen, green, (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, black, (x, y, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple):
        x, y = cell
        cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]
        for i in cells:
            if x + i[0] == self.width // self.cell_size and y + i[1] == self.height // self.cell_size:
                yield 0, 0
            elif x + i[0] == -1 and y + i[1] == -1:
                yield self.width // self.cell_size - 1, self.height // self.cell_size - 1
            elif x + i[0] == -1 and y + i[1] == self.height // self.cell_size:
                yield self.width // self.cell_size - 1, 0
            elif x + i[0] == self.width // self.cell_size and y + i[1] == -1:
                yield 0, self.height // self.cell_size - 1
            elif y + i[1] == -1:
                yield x + i[0], self.height // self.cell_size - 1
            elif x + i[0] == -1:
                yield self.width // self.cell_size - 1, y + i[1]
            elif y + i[1] == self.height // self.cell_size:
                yield x + i[0], 0
            elif x + i[0] == self.width // self.cell_size:
                yield 0, y + i[1]
            else:
                yield x + i[0], y + i[1]

    def get_next_generation(self, grid):
        new_grid = []
        for x in range(0, self.width, self.cell_size):
            line = []
            for y in range(0, self.height, self.cell_size):
                count = 0
                for elem in self.get_neighbours((x // self.cell_size, y // self.cell_size)):
                    if grid[elem[0]][elem[1]] == 1:
                        count += 1
                if (count == 2 or count == 3) and grid[x // self.cell_size][y // self.cell_size] == 1:
                    line.append(1)
                elif count == 3 and grid[x // self.cell_size][y // self.cell_size] == 0:
                    line.append(1)
                else:
                    line.append(0)
            new_grid.append(line)
        return new_grid

    def run(self):
        running = True
        pygame.init()
        pygame.display.set_caption(name)
        clock = pygame.time.Clock()

        self.screen.fill(black)
        self.draw_line()
        pygame.display.flip()
        grid = self.draw_first_grid()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            old_grid = grid
            grid = self.get_next_generation(grid)
            if old_grid == grid:
                running = False
            self.draw_grid(grid)
            self.draw_line()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
