import pygame
pygame.init()


from random import randint
import time


class Blocks:
    block_list = []
    width = 20
    
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.vel = snake.vel
        self.colour = colour
        if not Blocks.block_list:
            self.dirn = (snake.dirnx, snake.dirny)
            Snake.turns = {}  # removes any turn values stored before snake lengthens
        else:
            self.dirn = (Blocks.block_list[-1].dirn)

    def move(self):
        self.x += self.vel*self.dirn[0]
        self.y += self.vel*self.dirn[1]
        try:
            for pos, dirn in Snake.turns.items():
                for block in Blocks.block_list:
                    if (block.x, block.y) == pos:
                        block.dirn = dirn
                        if (block.x, block.y) == (Blocks.block_list[-1].x, Blocks.block_list[-1].y):
                            Snake.turns.pop(pos)
        except:
            pass

    def draw(self, win):
        self.move()
        pygame.draw.rect(win, self.colour, (self.x, self.y, Blocks.width, Blocks.width))


class Snake(object):
    turns = {}
    width = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dirnx = 0
        self.dirny = -1
        self.score = 0
        self.vel = 5

    def draw(self, win):
        self.move()
        pygame.draw.rect(win, (225, 0, 0), (self.x, self.y, Snake.width, Snake.width))

    def move(self):
        global win_width, win_height
        self.x += self.vel*self.dirnx
        self.y += self.vel*self.dirny
        if self.x < 0 or self.x + Snake.width > win_width or self.y < 0 or self.y + Snake.width > win_height:
            self.hit()
        snake_pos = pygame.math.Vector2(self.x + Snake.width //2, self.y + Snake.width//2)
        for block in Blocks.block_list:
            block_pos = pygame.math.Vector2(block.x + Blocks.width//2, block.y + Blocks.width//2)
            if snake_pos.distance_to(block_pos) < 0.8*Snake.width:
                self.hit()

    def hit(self):
        global running
        font = pygame.font.SysFont('comicsans', 60, True)
        hit_text = font.render('You lost!', 1, (100, 100, 0))
        count = 0
        while count < 2000:
            win.blit(hit_text, ((win_width - hit_text.get_width())/2, (win_height - hit_text.get_height())/2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    count = 2001
                    pygame.quit()
            pygame.display.update()
            pygame.time.delay(1)
            count += 1
        retry()


class Fruits(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = 10

    def draw(self, win):
        pygame.draw.circle(win, (0, 200, 0), (self.x, self.y), self.radius)

    def eaten(self):
        global block, counter
        snake_pos = pygame.math.Vector2(snake.x + Snake.width//2, snake.y + Snake.width//2)
        fruit_pos = pygame.math.Vector2(self.x, self.y)
        if snake_pos.distance_to(fruit_pos) <= self.radius and counter == 0:
            snake.score += 1
            xy = get_xy()
            colour = get_colour()
            Blocks.block_list.append(Blocks(xy[0], xy[1], colour))
            counter = 10
            eatsound.play()
            return True
        if counter > 0:
            counter -= 1
        return False


def get_colour():
    global red_rate, green_rate, blue_rate, red_trend, green_trend, blue_trend
    red_rate += red_trend * 20
    green_rate += green_trend * 30
    blue_rate += blue_trend * 40

    if red_rate >= 255 or red_rate <= 0:
        if red_trend == 1: red_trend = -1
        else: red_trend = 1
        red_rate += red_trend*20

    if green_rate >= 255 or green_rate <= 0:
        if green_trend == 1: green_trend = -1
        else: green_trend = 1
        green_rate += green_trend*30

    if blue_rate >= 255 or blue_rate <= 0:
        if blue_trend == 1: blue_trend = -1
        else: blue_trend = 1
        blue_rate += blue_trend*40

    colour = (red_rate, green_rate, blue_rate)
    return colour


def get_xy():
    if Blocks.block_list:
        tail_pos = (Blocks.block_list[-1].x, Blocks.block_list[-1].y)
        tail_dirn = Blocks.block_list[-1].dirn
        x = tail_pos[0] - Blocks.width*tail_dirn[0]
        y = tail_pos[1] - Blocks.width*tail_dirn[1]
    else:
        snake_pos = (snake.x, snake.y)
        x = snake_pos[0] - Blocks.width*snake.dirnx
        y = snake_pos[1] - Blocks.width*snake.dirny
    return (x, y)


def timer():  # checks how long fruit has been in screen for and changes x, y of fruit every fruit.duration seconds
    global start, win_width, win_height, apple
    current = time.time()
    x = randint(10, win_width - apple.radius)
    y = randint(10, win_height - apple.radius)
    if current - start >= 10 or apple.eaten():
        start = time.time()
        return (x, y)
    return round(10 - (current - start))


def create_grid(win):
    x = Snake.width
    y = Snake.width
    for i in range(win_width // Snake.width):
        pygame.draw.line(win, (240, 0, 255), (x*i, 0), (x*i, win_height))
        pygame.draw.line(win, (240, 0, 255), (0, y*i), (win_width, y*i))


def gamewindow(win, snake):
    global apple
    pos = timer()

    font = pygame.font.SysFont('comicsans', 20, True)
    score_text = font.render(f'You have: {int(snake.score)} points', 1, (0,0,0))
    time_text = font.render(f'{str(timer())} seconds', 1, (0,0,0))

    win.fill((225, 225, 0))
    create_grid(win)
    win.blit(score_text, (10, 10))
    win.blit(time_text, (10, 30))

    if not isinstance(pos, int):
        apple = Fruits(pos[0], pos[1], 10)
    apple.draw(win)
    snake.draw(win)
    for block in Blocks.block_list:
        block.draw(win)
    pygame.display.update()


def retry():
    global snake, apple, start, red_rate, green_rate, blue_rate, red_trend, blue_trend, green_trend, counter
    snake = Snake(250, 250)
    Blocks.block_list = []
    apple = Fruits(100, 100, 10)
    red_rate = 0
    green_rate = 0
    blue_rate = 0
    red_trend = 1
    blue_trend = 1
    green_trend = 1
    counter = 0
    start = time.time()


win = pygame.display.set_mode((500, 500))
win_width, win_height = win.get_width(), win.get_height()
music = pygame.mixer.music.load('Netherplace.mp3')
pygame.mixer.music.play(-1)

eatsound = pygame.mixer.Sound('eating.wav')

counter = 0
snake = Snake(250, 250)
apple = Fruits(100, 100, 10)
start = time.time()
running = True

red_rate = 0
green_rate = 0
blue_rate = 0
red_trend = 1
blue_trend = 1
green_trend = 1

# mainloop
while running:
    gamewindow(win, snake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if (snake.dirnx, snake.dirny) != (0, 1):
            snake.dirnx, snake.dirny = 0, -1
            Snake.turns[(snake.x, snake.y)] = (snake.dirnx, snake.dirny)
    elif keys[pygame.K_DOWN]:
        if (snake.dirnx, snake.dirny) != (0, -1):
            snake.dirnx, snake.dirny = 0, 1
            Snake.turns[(snake.x, snake.y)] = (snake.dirnx, snake.dirny)
    elif keys[pygame.K_LEFT]:
        if (snake.dirnx, snake.dirny) != (1, 0):
            snake.dirnx, snake.dirny = -1, 0
            Snake.turns[(snake.x, snake.y)] = (snake.dirnx, snake.dirny)
    elif keys[pygame.K_RIGHT]:
        if (snake.dirnx, snake.dirny) != (-1, 0):
            snake.dirnx, snake.dirny = 1, 0
            Snake.turns[(snake.x, snake.y)] = (snake.dirnx, snake.dirny)

    pygame.time.delay(30)