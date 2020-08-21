import textwrap
import pygame

pygame.init()


class Player(object):
    walkRight = [pygame.image.load('Images\R1.png'), pygame.image.load('Images\R2.png'), pygame.image.load('Images\R3.png'),
                 pygame.image.load('Images\R4.png'), pygame.image.load('Images\R5.png'), pygame.image.load('Images\R6.png'),
                 pygame.image.load('Images\R7.png'), pygame.image.load('Images\R8.png'), pygame.image.load('Images\R9.png')]
    walkLeft = [pygame.image.load('Images\L1.png'), pygame.image.load('Images\L2.png'), pygame.image.load('Images\L3.png'),
                pygame.image.load('Images\L4.png'), pygame.image.load('Images\L5.png'), pygame.image.load('Images\L6.png'),
                pygame.image.load('Images\L7.png'), pygame.image.load('Images\L8.png'), pygame.image.load('Images\L9.png')]

    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.initial_pos = (self.x, self.y)
        self.width = Player.walkRight[0].get_width()  # all images are same size
        self.height = Player.walkRight[0].get_height()
        self.vel = vel
        self.jump = False
        self.max_jump_value = 8  # determines height of the jump (see do_jump for actual jump code)
        self.jump_value = self.max_jump_value
        self.right = False  # use to draw image and determine direction of bullet
        self.walkcount = 0  # helps cycle back to starting image once all 9 images have been shown
        self.hitbox = (self.x + 20, self.y + 15, 23, 45)  # helps determine collision
        self.max_health = 20
        self.health = self.max_health
        self.restart = False
        self.has_shield = True  # shield protects player from one (moderately fast) collision
        self.money = 0  # use to buy upgrades in pause/ shop screen
        self.money_increment_hit = 5  # inc money by this much when hitting goblin
        self.money_increment_new_level = 100  # inc money by this much for a new level
        self.score = 0
        self.score_decrement = 2  # dec score by this when colliding with goblin
        self.score_increment = 1
        self.score_increment_new_level = 5
        self.level = 1
        self.max_level = 30

    def move(self):
        if self.x + self.vel > 0 and (self.x + self.width + self.vel) < win_width:
            self.x += self.vel

    def do_jump(self):
        # models jumping as a quadratic function, jump_value = x, height = y: so goes from x = 8 to -8 while doing y^-2
        if self.jump_value >= -self.max_jump_value:
            if self.jump_value > 0:  # makes sures char goes up then comes back down
                self.y -= (self.jump_value ** 2)
            if self.jump_value < 0:
                if self.y + (self.jump_value ** 2) < self.initial_pos[1]:
                    self.y += (self.jump_value ** 2)
                else:
                    self.y = self.initial_pos[1]
                    self.jump_value = self.max_jump_value
                    self.jump = False
            self.jump_value -= 1
        else:
            self.jump = False
            self.jump_value = self.max_jump_value

    def draw(self, showing_timer=False):
        # displays each image for 3 frames/iterations of while loop
        # cycles back to first image to avoid index error
        image_duration = 3  # frames
        if self.walkcount + 1 >= len(Player.walkRight) * image_duration:
            self.walkcount = 0

        if self.right:
            if self.jump:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkRight[self.walkcount // image_duration], (self.x, self.y))
                if not showing_timer:  # image doesn't change when timer is showing
                    self.walkcount += 1
        else:
            if self.jump:
                win.blit(self.walkLeft[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[self.walkcount // image_duration], (self.x, self.y))
                if not showing_timer:
                    self.walkcount += 1

        self.draw_health_bar()

    def draw_health_bar(self):
        # draws a black health bar and then a red health bar on top
        self.hitbox = (self.x + 20, self.y + 15, 23, 45)
        offset = 10
        width = 40
        height = 10
        pygame.draw.rect(win, colours["black"], (self.hitbox[0] - offset, self.hitbox[1] - offset, width, height))
        pygame.draw.rect(win, colours["red"], (self.hitbox[0] - offset, self.hitbox[1] - offset, width -
                                               (width / self.max_health) * (self.max_health - self.health), height))

    def display_hit_text(self):
        if self.health > 0:
            create_text(*texts["hit"])
        else:
            gamewindow(win)  # blits over previous text
            create_text(*texts["lost"])
        pygame.display.update()
        freeze_screen(2)

    def reset_position(self):
        self.x = 0.5 * win_width  # teleports character ( and goblins) to prevent continuous collisions
        self.y = y_factor_all * win_height

    def hit(self):
        self.walkcount = 0
        self.has_shield = True

        if self.health > 0:
            self.health -= 1
        if self.health == 0:
            self.display_hit_text()  # displays end text
            retry()
        new_score = self.score - self.score_decrement
        self.score = new_score if new_score >= 0 else 0

        self.x, self.y = self.initial_pos
        Goblins.set_initial_goblin_pos()


class Projectile(object):
    bullets = []
    max_bullets = 1
    shoot_sleep = 0  # ensures bullets don't bunch up due to fast iterations of comp, see mainloop for shoot code

    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.hitbox = (self.x - self.radius // 2, self.y - self.radius // 2, self.radius, self.radius)
        self.colour = colour
        self.vel = 18 * facing  # facing = direction faced by char to ensure bullet travels in that directions
        Projectile.bullets.append(self)

    def move(self):
        if 0 < self.x < win_width:  # doesn't go off screen
            self.x += self.vel
        else:
            Projectile.bullets.pop(Projectile.bullets.index(self))
        self.hitbox = (self.x - self.radius // 2, self.y - self.radius // 2, self.radius, self.radius)

    def draw(self):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y)), self.radius)


class Goblins(object):
    walkRight = [pygame.image.load('Images\R1E.png'), pygame.image.load('Images\R2E.png'), pygame.image.load('Images\R3E.png'),
                 pygame.image.load('Images\R4E.png'), pygame.image.load('Images\R5E.png'), pygame.image.load('Images\R6E.png'),
                 pygame.image.load('Images\R7E.png'), pygame.image.load('Images\R8E.png'), pygame.image.load('Images\R9E.png'),
                 pygame.image.load('Images\R10E.png'), pygame.image.load('Images\R11E.png')]
    walkLeft = [pygame.image.load('Images\L1E.png'), pygame.image.load('Images\L2E.png'), pygame.image.load('Images\L3E.png'),
                pygame.image.load('Images\L4E.png'), pygame.image.load('Images\L5E.png'), pygame.image.load('Images\L6E.png'),
                pygame.image.load('Images\L7E.png'), pygame.image.load('Images\L8E.png'), pygame.image.load('Images\L9E.png'),
                pygame.image.load('Images\L10E.png'), pygame.image.load('Images\L11E.png')]
    goblin_list = []
    max_vel = 0  # initialised below

    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.initial_pos = (self.x, self.y)
        self.width = Goblins.walkRight[0].get_width()
        self.height = Goblins.walkRight[0].get_height()
        self.vel = vel
        if self.vel > Goblins.max_vel:
            self.vel = Goblins.max_vel
        self.walkcount = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.max_health = 10
        self.health = self.max_health
        Goblins.goblin_list.append(self)

    @classmethod
    def create_goblin(cls):
        # creates 1 extra goblin after every 5 levels
        spacing = 0.06  # spawn goblins on opposite ends of screen, with a spacing of 0.05 * win_width
        for i in range(1, (veronian.level - 1) // 5 + 2):
            velocity = 1.5 * veronian.level * ((-1) ** (i + 1))
            if i % 2 != 0:
                Goblins((i * spacing) * win_width, y_factor_all * win_height, velocity)
            else:
                Goblins((1 - (i * spacing)) * win_width, y_factor_all * win_height, velocity)

    @classmethod
    def set_initial_goblin_pos(cls):
        for goblin in cls.goblin_list:
            goblin.x, goblin.y = goblin.initial_pos
            goblin.hitbox = (goblin.x + 17, goblin.y + 2, 31, 57)

    def draw(self, showing_timer=False):
        image_duration = 3  # frames
        if self.walkcount + 1 >= len(Goblins.walkLeft) * image_duration:
            self.walkcount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkcount // image_duration], (self.x, self.y))
            if not showing_timer and not frozen:
                self.walkcount += 1
        elif self.vel < 0:
            win.blit(self.walkLeft[self.walkcount // image_duration], (self.x, self.y))
            if not showing_timer and not frozen:
                self.walkcount += 1

        self.draw_health_bar()

    def draw_health_bar(self):
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        offset = 10
        width = 40
        height = 10
        pygame.draw.rect(win, colours["black"], (self.hitbox[0] - offset, self.hitbox[1] - offset, width, height))
        pygame.draw.rect(win, colours["red"], (self.hitbox[0] - offset, self.hitbox[1] - offset, width -
                                               (width / self.max_health) * (self.max_health - self.health), height))

    def move(self):
        if 0 <= self.x + self.vel <= win_width - self.width:
            self.x += self.vel
        else:
            self.vel *= -1
            self.walkcount = 0

    def hit(self):
        # makes it turn towards player if hit
        self.walkcount = 0

        if (veronian.x > self.x and self.vel < 0) or (veronian.x < self.x and self.vel > 0):
            self.vel = self.vel * -1
        if self.health > 1:
            self.health -= 1
        else:
            Goblins.goblin_list.pop(Goblins.goblin_list.index(self))


class Buttons(object):
    def __init__(self, x, y, width, height, colour1, text='', func=None, arg=None):  # pink buttons
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour1 = colour1
        self.text = text
        self.func = func
        self.arg = arg

    def draw(self, win):  # draws centralised buttons and text
        font = pygame.font.SysFont('comicsans', 30, True)
        text = font.render(self.text, 1, colours["black"])
        pygame.draw.rect(win, (self.colour1),
                         (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        win.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def isover(self, pos):  # detects if mouse positions is above buttons'
        if self.x < pos[0] < (self.x + self.width) and self.y < pos[1] < (self.y + self.height):
            return True
        return False

    def isclicked(self, pos):
        if self.arg is not None:
            if self.isover(pos):
                if self.func(*self.arg):
                    create_text(*texts["successful purchase"])
                else:
                    create_text(*texts["failed purchase"])
        else:
            if self.isover(pos):
                if self.func():
                    create_text(*texts["successful purchase"])
                else:
                    create_text(*texts["failed purchase"])


def fix_position():
    veronian.initial_pos = (0.5 * (win_width - Player.walkRight[0].get_width()), y_factor_all * win_height)
    veronian.x, veronian.y = veronian.initial_pos
    veronian.walkcount = 0
    spacing = 0.06  # spawn goblins on opposite ends of screen, with a spacing of 0.05 * win_width
    for i in range(1, len(Goblins.goblin_list) + 1):
        goblin = Goblins.goblin_list[i - 1]
        if i % 2 != 0:
            goblin.initial_pos = ((i * spacing) * win_width, y_factor_all * win_height)
        else:
            goblin.initial_pos = ((1 - (i * spacing)) * win_width, y_factor_all * win_height)
        goblin.x, goblin.y = goblin.initial_pos
        goblin.walk_count = 0

    Projectile.bullets = []
    display_timer(3)


def ending():
    while True:
        end_text = f'You won!! You finished with {veronian.score} points and £{veronian.money}! Press r to retry.'
        font_size = 55
        colour = colours["orange"]
        create_text(end_text, font_size, colour, 0.5, 0.5, centralisex=True, centralisey=True)
        if check_input(check_quit=True, check_retry=True, check_resize=True) == "retry":
            break
        pygame.display.update()
        pygame.time.delay(1)


def freeze_screen(time, bg_func=None, bg_args=None, text_func=None, text_args=None):
    # freezes screen while checking if user wants to retry/ pause/ quit
    global countdown_time_start, freeze_time_start
    time *= 1000  # convert to milliseconds
    timer = 0
    while timer < time:
        if frozen and countdown_time_start == 0:
            countdown_time_start = pygame.time.get_ticks()
        timer += 1
        val = check_input(check_all=True, check_enter=True)
        if paused:
            timer -= 1
            pausewindow()
            continue
        if val == "return":
            if frozen:
                freeze_time_start += pygame.time.get_ticks() - countdown_time_start
                countdown_time_start = 0
            return val
        elif val == "resize" and text_func:
            if bg_func:
                if bg_args:
                    bg_func(bg_args)
                else:
                    bg_func()
            text_func(*text_args)
            pygame.display.update()
        pygame.time.delay(1)
    if frozen:
        freeze_time_start += pygame.time.get_ticks() - countdown_time_start
        countdown_time_start = 0


def freeze_screen_when_paused(time, bg_func=None, bg_args=None, text_func=None, text_args=None):
    # same as above but prevents infinite loop when freeze_screen calls pause_window & pause_window calls freeze_screen
    time *= 1000  # convert to milliseconds
    timer = 0
    while timer < time:
        timer += 1
        val = check_input(check_all=True, check_enter=True)
        if val == "return":
            return val
        elif val == "resize" and text_func:
            if bg_func:
                if bg_args:
                    bg_func(bg_args)
                else:
                    bg_func()
            text_func(*text_args)
            pygame.display.update()
        pygame.time.delay(1)


def display_timer(time):
    for i in range(time):
        gamewindow(showing_timer=True)  # reset texts
        create_text(f"{time - i}", 50, colours["orange"], -1, -1)
        pygame.display.update()
        if freeze_screen(1) == "return":
            break


def check_input(check_quit=False, check_pause=False, check_retry=False, check_resize=False, check_enter=False,
                check_all=False):
    # check for retry/ pause/ quit/ video resize
    global previous_win_height, previous_win_height, win_width, win_height, running, paused, pause_ticker, win, pause_clicked
    keys = pygame.key.get_pressed()
    if check_all:  # only checks for enter on the starting screen
        check_quit, check_pause, check_retry, check_resize = True, True, True, True
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE and check_resize:
            previous_win_height, previous_win_height = win.get_width(), win.get_height() # use to scale
            win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
            win_width, win_height = win.get_width(), win.get_height()
            rescale()
            if paused and not pause_clicked:
                pause_clicked = True  # will make mainloop redraw buttons with new sizes and locations
            return "resize"
        if event.type == pygame.QUIT and check_quit:
            running = False
            paused = False
            pygame.quit()
        if event.type == pygame.KEYDOWN and check_enter:
            if event.key == pygame.K_RETURN:
                return "return"
        if event.type == pygame.MOUSEBUTTONDOWN:
            return "clicked"
    if keys[pygame.K_r] and check_retry:
        retry()
        return "retry"
    if keys[pygame.K_p] and pause_ticker == 0 and check_pause:
        pause_ticker = 10  # p only registers once every 10 frames
        paused = not paused
        pause_clicked = True
        adjust_freeze_time()
        return "pause"


def adjust_freeze_time():
    global pause_time_start, freeze_time_start
    if frozen:
        if paused:
            pause_time_start = pygame.time.get_ticks()
        if not paused:
            freeze_time_start += pygame.time.get_ticks() - pause_time_start
            pause_time_start = 0


def retry():
    global veronian
    veronian = Player(0.5 * (win_width - Player.walkRight[0].get_width()), y_factor_all * win_height, original_veronian_vel)
    veronian.level = 1
    veronian.score = 0
    Goblins.goblin_list = []
    Goblins.create_goblin()
    Projectile.bullets = []
    Projectile.max_bullets = 1
    load_background()


def start():
    global show_game
    win.fill(colours["white"])
    create_text(*texts["start"])
    pygame.display.update()

    freeze_screen(20, win.fill, colours["white"], create_text, texts["start"])
    show_game = True


def wrap_text(text, font, colour, pos, centralisex=False, centralisey=False, width=70):
    # blits a given text in wrapped format
    # by default, blits it onto centre, unless a position is specified
    setup = textwrap.TextWrapper(width=width)
    text = setup.wrap(text)  # returns a list of lines
    if centralisey:  # pushes a block of text up, if it needs to be centralised vertically
        pos = (pos[0], pos[1] - font.size('a')[1] * len(text) / 2)
    line_count = 0  # provides spaces between lines
    for line in text:
        text2 = font.render(line, 1, colour)
        win.blit(text2, (pos[0] if not centralisex else (win_width - text2.get_width()) // 2,
                         pos[1] + font.size('a')[1] * line_count))
        line_count += 1


def create_text(text, font_size, colour, x_factor, y_factor, centralisex=False, centralisey=False):
    # create the various text objects for gamewindow and pausewindow, see below
    centralisex, centralisey = True if x_factor == -1 else centralisex, True if y_factor == -1 else centralisey
    colour = colours["yellow"] if colour is None else colour
    font = pygame.font.SysFont('comicsans', font_size, True)
    make_text = font.render(text, 1, colour)
    pos = (x_factor * win_width if not centralisex else (win_width - make_text.get_width()) // 2,
           y_factor * win_height if not centralisey else win_height // 2 - make_text.get_height())
    if pos[0] + make_text.get_width() >= win_width:
        width = int(win_width / font.size('a')[0]) if centralisex else int((win_width - pos[0]) / font.size('a')[0])
        wrap_text(text, font, colour, pos, centralisex=centralisex, centralisey=centralisey, width=width)
        return
    win.blit(make_text, pos)


def draw_characters(showing_timer=False):
    veronian.draw(showing_timer=showing_timer)
    for goblin in Goblins.goblin_list:
        goblin.draw(showing_timer=showing_timer)
    for bullet in Projectile.bullets:
        bullet.draw()


def draw_texts(score=False, level=False, shield=False, bullets=False, money=False, pause=False):
    # draws specified texts
    if pause: create_text(*texts["pause"])
    if score: create_text(*texts["score"])
    if level: create_text(*texts["level"])
    if shield: create_text(*texts["shield"])
    if bullets: create_text(*texts["bullets"])
    if money: create_text(*texts["money"])


def gamewindow(showing_timer=False):
    global pause_ticker
    win.blit(bg, (0, 0))
    if not showing_timer:
        veronian.move()
        if not frozen:
            for goblin in Goblins.goblin_list:
                goblin.move()
    fix_button = Buttons(1.2 * x_factor_end * win_width, (y_factor_top + y_factor_spacing * 4) * win_height, 60, 30, colours["red"], "Fix")
    fix_button.draw(win)
    load_texts(default_font_size, title_font_size, x_factor_end, x_factor_start, y_factor_top, y_factor_spacing)
    draw_texts(score=True, level=True, shield=True, bullets=True, money=True)
    draw_characters(showing_timer=showing_timer)

    pos = pygame.mouse.get_pos()
    if check_input(check_all=True) == "clicked":
        if fix_button.isover(pos):
            fix_position()
    if pause_ticker > 0:
        pause_ticker -= 1
    pygame.display.update()


def pausewindow():
    global pause_clicked, pause_ticker
    win.blit(bg, (0, 0))  # always load and draw  everything first
    load_texts(default_font_size, title_font_size, x_factor_end, x_factor_start, y_factor_top, y_factor_spacing)
    draw_texts(pause=True, shield=True, bullets=True, money=True)
    buy_bullets_button.draw(win)
    buy_shield_button.draw(win)
    if veronian.level >= 16:
        buy_freeze_button.draw(win)
    if veronian.level >= 21:
        buy_health_button.draw(win)

    if pause_clicked:
        load_pause_buttons()
        pause_clicked = False
    pos = pygame.mouse.get_pos()
    if check_input(check_all=True) == "clicked":
        buy_bullets_button.isclicked(pos)
        buy_shield_button.isclicked(pos)
        if veronian.level >= 16:
            buy_freeze_button.isclicked(pos)
        if veronian.level >= 21:
            buy_health_button.isclicked(pos)
        pygame.display.update()
        freeze_screen_when_paused(1)
    else:
        pygame.display.update()

    if pause_ticker > 0:
        pause_ticker -= 1


def buy_bullets():
    global bullet_price, pause_clicked
    if veronian.money >= bullet_price:
        veronian.money -= bullet_price
        Projectile.max_bullets += 1
        bullet_price += bullet_price_inc
        pause_clicked = True  # resets button texts
        return True
    else:
        return False


def buy_shield():
    global shield_price, pause_clicked
    if veronian.money >= shield_price and not veronian.has_shield:
        veronian.money -= shield_price
        veronian.has_shield = True
        shield_price += shield_price_inc
        pause_clicked = True  # resets button texts
        return True
    else:
        return False


def buy_health():
    if veronian.money >= health_price and veronian.health + buy_health_value <= veronian.max_health:
        veronian.money -= health_price
        veronian.health += buy_health_value
        return True
    else:
        return False


def buy_freeze():
    global frozen, freeze_time_start, pause_time_start
    if veronian.money > freeze_price and not frozen:
        veronian.money -= freeze_price
        frozen = True
        freeze_time_start = pygame.time.get_ticks()
        pause_time_start = freeze_time_start
        return True
    else:
        return False


def load_background():  # loads background depending on level
    global bg
    if veronian.level % 20 < 6:  # % allows same 4 backgrounds to be cycled through every 20 levels
        bg = pygame.image.load('Images\\bg1.jpg')
    if 5 < veronian.level % 20 < 11:
        bg = pygame.image.load('Images\\bg2.jpg')
    if 10 < veronian.level % 20 < 16:
        bg = pygame.image.load('Images\\bg3.jpg')
    if 15 < veronian.level % 20 < 20 or veronian.level % 20 == 0:
        bg = pygame.image.load('Images\\bg4.jpg')
    # do not remove this
    bg = pygame.transform.scale(bg, (win_width, win_height))


def rescale():
    global bg, original_veronian_vel, default_font_size, title_font_size
    diffx = win_width - previous_win_width
    diffy = win_height - previous_win_height

    bg = pygame.transform.scale(bg, (win_width, win_height))
    default_font_size += int((default_font_size / previous_win_height) * diffy)
    title_font_size += int((title_font_size / previous_win_height) * diffy)

    all_changey = y_factor_all * diffy
    ver_changex = (veronian.x / previous_win_width) * diffx
    ver_initial_changex = (veronian.initial_pos[0] / previous_win_width) * diffx
    ver_change_vel = (original_veronian_vel / previous_win_width) * diffx

    veronian.initial_pos = (veronian.initial_pos[0] + ver_initial_changex, veronian.initial_pos[1] + all_changey)
    veronian.x, veronian.y = veronian.x + ver_changex, veronian.y + all_changey
    original_veronian_vel += ver_change_vel  # can't change current velocity which may be positive/ negative

    for goblin in Goblins.goblin_list:
        gob_changex = (goblin.x / previous_win_width) * diffx
        gob_initial_changex = (goblin.initial_pos[0] / previous_win_width) * diffx
        gob_change_vel = (goblin.vel / previous_win_width) * diffx

        goblin.initial_pos = (goblin.initial_pos[0] + gob_initial_changex, goblin.initial_pos[1] + all_changey)
        goblin.x, goblin.y = goblin.x + gob_changex, goblin.y + all_changey
        goblin.vel += gob_change_vel

    for bullet in Projectile.bullets:
        bullet.vel += (bullet.vel / previous_win_width) * diffx


def check_collision(obj1, obj2, bullet=False):
    if not bullet:
        return obj1.hitbox[1] + obj1.hitbox[3] > obj2.hitbox[1] and obj1.hitbox[1] < obj2.hitbox[1] + obj2.hitbox[3] \
               and obj1.hitbox[0] + obj1.hitbox[2] > obj2.hitbox[0] and obj1.hitbox[0] < obj2.hitbox[0] + obj2.hitbox[2]
    else:
        return pygame.math.Vector2(obj1.x, obj1.y).distance_to(pygame.math.Vector2(obj2.x, obj2.y)) <= obj2.width


def next_level():
    veronian.level += 1
    veronian.money += veronian.money_increment_new_level
    veronian.score += veronian.score_increment_new_level
    if veronian.level == veronian.max_level + 1:
        return
    veronian.has_shield = True
    veronian.jump = False
    Projectile.bullets = []
    if veronian.level % 5 == 1:
        Projectile.max_bullets += 1
    load_background()
    Goblins.create_goblin()
    (veronian.x, veronian.y) = veronian.initial_pos


def check_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and Projectile.shoot_sleep == 0:
        facing = 1 if veronian.right else -1  # checks directions char faces so bullet can move in correct direction
        if len(Projectile.bullets) < Projectile.max_bullets:
            Projectile(veronian.x + veronian.width // 2, veronian.y + veronian.height // 2, 3, colours["white"], facing)
            bulletsound.play()
        Projectile.shoot_sleep = 1
    if keys[pygame.K_UP]:  # basic controls
        veronian.jump, veronian.walk_count = True, 0
    if keys[pygame.K_LEFT]:
        veronian.vel, veronian.right = -1 * original_veronian_vel, False
    elif keys[pygame.K_RIGHT]:
        veronian.vel, veronian.right = original_veronian_vel, True
    else:
        veronian.walkcount = 0
        veronian.vel = 0
    if veronian.jump:
        veronian.do_jump()


def load_texts(default_font_size, title_font_size, x_factor_end, x_factor_start, y_factor_top, y_factor_spacing):
    global texts
    shield_status = 'on' if veronian.has_shield else 'off'
    texts = {"pause": ('PAUSED', title_font_size, colours["red"], -1, y_factor_top),
             "shield": (
                 f'Shield status: {shield_status}', default_font_size, colours["yellow"], x_factor_end, y_factor_top),
             "bullets": (f'Max bullets: {Projectile.max_bullets}', default_font_size, colours["yellow"], x_factor_end,
                         y_factor_top + y_factor_spacing),
             "money": (f'Money: £{veronian.money}', default_font_size, colours["yellow"], x_factor_end,
                       y_factor_top + y_factor_spacing * 2),
             "score": (f'Score: {veronian.score}', default_font_size, colours["yellow"], x_factor_start, y_factor_top),
             "level": (f'Level: {veronian.level}', default_font_size, colours["yellow"], x_factor_start,
                       y_factor_top + y_factor_spacing),
             "successful purchase": ('Purchased!', default_font_size, colours["red"], -1, 0.75),
             "failed purchase": ('Sorry, you have insufficient money, too much health or is power already activated',
                                 title_font_size, colours["red"], -1,
                 0.75),
             "hit": ('HIT! -2 point', title_font_size, colours["red"], -1, -1),
             "lost": (
                 f'Sorry, you lost with {veronian.score} points at level {veronian.level}', title_font_size,
                 colours["red"],
                 -1, -1),
             "start": ('Use arrow keys to move and jump, press space to shoot. P = pause/ shop. R = retry. Goblins '
                       'become faster every level. Every 5 levels, Goblins increase in number and your max bullets  inc'
                       f' by 1. Finish level {veronian.max_level} to win. Press enter to continue.\n '
                       'Developed by Vijay Damodharan',
                       title_font_size, colours["black"], -1, -1)
             }


def load_pause_buttons():
    global buy_bullets_button, buy_shield_button, buy_health_button, buy_freeze_button
    width, height = 380, 60
    buy_bullets_button = Buttons(0.25 * win_width, 0.5 * win_height * 0.95, width, height, colours["pink"],
                                 text=f'Inc max bullets by 1 - £{bullet_price}', func=buy_bullets)
    buy_shield_button = Buttons(0.75 * win_width, 0.5 * win_height * 0.95, width, height, colours["pink"],
                                text=f'Activate shield - £{shield_price}', func=buy_shield)
    buy_freeze_button = Buttons(0.25 * win_width, 0.5 * win_height * 1.25, width, height, colours["pink"],
                                text=f'Freeze goblins for {freeze_time_total} secs - £{freeze_price}', func=buy_freeze)
    buy_health_button = Buttons(0.75 * win_width, 0.5 * win_height * 1.25, width, height, colours["pink"],
                                text=f'Buy {buy_health_value} health - £{health_price}', func=buy_health)



clock = pygame.time.Clock()  # sets fps
win = pygame.display.set_mode((852, 480), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)  # game window
previous_win_width, previous_win_height = win.get_width(), win.get_height()
win_width, win_height = win.get_width(), win.get_height()
pygame.display.set_caption('Beat the goblins!')
music = pygame.mixer.music.load('Music\music.mp3')
pygame.mixer.music.play(-1)
bulletsound = pygame.mixer.Sound('Music\\bullet.wav')
hitsound = pygame.mixer.Sound('Music\hit.wav')

running = True
show_game = False  # change from start screen
paused = False
y_factor_all = 0.85  # all objects should be at 0.85 * win_height to match the background
pause_ticker = 0
pause_clicked = False  # use to only create the shop buttons once in pause window
hit_timer = 0  # prevent multiple hits during same collision
bullet_price = 300
bullet_price_inc = 100
shield_price = 200
shield_price_inc = 100
health_price = 1000
buy_health_value = 5
freeze_price = 800
frozen = False
freeze_time_total = 3  # total number of seconds goblins will be frozen
freeze_time_start = 0  # stores pygame.time.get_tickers() when frozen is bought
pause_time_start = 0  # see how long pause was activated to remove from freeze_time
countdown_time_start = 0  # see how long countdown was activated to remove from freeze_time

original_veronian_vel = 9
veronian = Player(0.5 * (win_width - Player.walkRight[0].get_width()), y_factor_all * win_height, original_veronian_vel)
Goblins.max_vel = 2 * veronian.vel
Projectile.max_bullets = (veronian.level - 1) // 5 + 1
Goblins.create_goblin()

colours = {"black": (0, 0, 0),
           "red": (255, 0, 0),
           "green": (0, 255, 0),
           "blue": (0, 0, 255),
           "yellow": (225, 225, 0),
           "orange": (225, 100, 10),
           "pink": (225, 100, 180),
           "white": (225, 225, 225)
           }

# text sizes and positions to use for rescaling
default_font_size = 40
title_font_size = 50
x_factor_end = 0.67
x_factor_start = 0.06
y_factor_top = 0.1
y_factor_spacing = pygame.font.SysFont('comicsans', default_font_size, True).size('a')[1] / win_height
load_texts(default_font_size, title_font_size, x_factor_end, x_factor_start, y_factor_top, y_factor_spacing)
load_pause_buttons()

load_background()

# mainloop
while running:
    if not show_game:
        start()
    if len(Goblins.goblin_list) == 0:
        next_level()
        load_texts(default_font_size, title_font_size, x_factor_end, x_factor_start, y_factor_top, y_factor_spacing)
        if veronian.level != veronian.max_level + 1:
            display_timer(3)
    if veronian.level == veronian.max_level + 1:
        ending()

    if paused:
        pausewindow()
    if not paused:
        if frozen:
            if pygame.time.get_ticks() - freeze_time_start >= freeze_time_total * 1000:
                frozen = False
                freeze_time_start = 0
        check_movement()

        if hit_timer == 0:
            for goblin in Goblins.goblin_list:
                if check_collision(veronian, goblin):
                    if not veronian.has_shield:
                        veronian.display_hit_text()
                        veronian.hit()
                        veronian.vel = 0  # stops him from moving during timer
                        Projectile.bullets = []

                        gamewindow(win)  # blits new positions
                        display_timer(2)
                        hit_timer = 10
                    else:
                        veronian.has_shield = False
                        hit_timer = 10
                        break

        for goblin in Goblins.goblin_list:
            for bullet in Projectile.bullets:
                if check_collision(bullet, goblin,
                                   bullet=True):  # checks if bullet is next to goblin - note: this allows for hitting when bullet is slightly above goblin's head, but this is actually very rare to happen, so can be ignored
                    hitsound.play()
                    goblin.hit()
                    veronian.score += veronian.score_increment
                    veronian.money += veronian.money_increment_hit
                    Projectile.bullets.pop(Projectile.bullets.index(bullet))
                else:
                    bullet.move()
        gamewindow()

    if Projectile.shoot_sleep > 0:
        Projectile.shoot_sleep += 1
    if Projectile.shoot_sleep > 3:
        Projectile.shoot_sleep = 0

    if hit_timer > 0:
        hit_timer -= 1

    check_input(check_all=True)
    clock.tick(
        27)  # if you display each image for 3 frames, and there are 9 images, that allows for 27 frames in total, which is displayed each second.

pygame.quit()
