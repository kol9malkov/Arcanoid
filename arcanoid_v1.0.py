import pygame
pygame.init()

""" Создание объектов для фона и заливка фона """
BACKGROUND = (200, 255, 255) # цвет фона
mw = pygame.display.set_mode((500, 500))
mw.fill(BACKGROUND)

""" Создание игрового таймера """
clock = pygame.time.Clock()

""" Класс прямоугольника """
class Area():
    def __init__ (self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height) # создаем прямоугольник
        self.fill_color = BACKGROUND
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color
    
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    
    # проверка нажатия на прямоугольник
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

""" Класс картинки """
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

""" Создание спрайтов """
ball = Picture("ball.png", 160, 200, 50, 50)
platform = Picture("platform.png", 200, 330, 100, 30)

start_x = 5 #координаты первого монстра по x
start_y = 5 #координаты первого монстра по y
monsters = []
n = 9
for j in range(3):
    y = start_y + (55 * j) # смещаем следующего монстра на 55 пикселей по y
    x = start_x + (27.5 * j) # смещаем следующего монстра на 27.5 по x
    for i in range(n):
        monster = Picture("enemy.png", x, y, 50, 50)
        monsters.append(monster)
        x += 55
    n -= 1


""" Игровой цикл """
game_over = True # флаг окончания игры
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
    
    for m in monsters: # отрисовываем монстров
        m.draw()

    ball.fill() # отображаем прямоугольник вокруг мяча
    platform.fill() # отображаем прямоугольник вокруг платформы
    ball.draw() # отрисовываем мяч
    platform.draw() # отрисовываем платформу

    clock.tick(40)
    pygame.display.update()



