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

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


""" Класс картинки """
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

""" Класс надписи """
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

""" Создание спрайтов """
ball = Picture("ball.png", 160, 200, 50, 50)
platform = Picture("platform.png", 200, 350, 100, 30)

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
move_right = False # флаг движения вправо
move_left = False # флаг движения влево
speed_x = 3 # направления перемещения мяча по x
speed_y = 3 # направления перемещения мяча по y
while game_over:
    ball.fill() # отображаем прямоугольник вокруг мяча
    platform.fill() # отображаем прямоугольник вокруг платформы

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # нажата клавиша 'a' (K_LEFT - нажата стрелка влево)
                move_left = True
            if event.key == pygame.K_d: # нажата клавиша 'd' (K_RIGHT - нажата стрелка вправо)
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a: # не нажата клавиша 'a' (K_LEFT - нажата стрелка влево)
                move_left = False
            if event.key == pygame.K_d: # не нажата клавиша 'd' (K_RIGHT - нажата стрелка вправо)
                move_right = False
        

    if move_right and platform.rect.x < 400:
        platform.rect.x += 3
    if move_left and platform.rect.x > 0:
        platform.rect.x -= 3

    """ автоматическое движение мяча """
    ball.rect.x += speed_x
    ball.rect.y += speed_y

    """ отскоки мяча"""
    if ball.colliderect(platform.rect):
        speed_y *= -1
    if ball.rect.y < 0:
        speed_y *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1

    """ Поражение """
    if ball.rect.y > (platform.rect.y):
        time_text = Label(150, 150, 50, 50, BACKGROUND)
        time_text.set_text("YOU LOSE", 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = False
    """ Победа """
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, BACKGROUND)
        time_text.set_text("YOU WIN", 60, (0, 200, 0))
        time_text.draw(10, 10)
        game_over = False

    
    for m in monsters: # отрисовываем монстров
        m.draw()
        if m.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            speed_y *= -1

    ball.draw() # отрисовываем мяч
    platform.draw() # отрисовываем платформу

    pygame.display.update()
    clock.tick(40)
