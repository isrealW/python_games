import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
BALL_SIZE = WIDTH//100
PLAYER_WIDTH = WIDTH // 40
PLAYER_HEIGHT = HEIGHT // 8
FONT = pygame.font.SysFont('comicsans', WIDTH//15)


class Player:

    def __init__(self, x, y, k1, k2):
        self.x = x
        self.y = y
        self.k1 = k1
        self.k2 = k2
        self.score = 0

    def move(self, keys):
        if keys[self.k1]:
            if self.y-4 > 0:
                self.y -= 4
            else:
                self.y = 0

        elif keys[self.k2]:
            if self.y + 4 + PLAYER_HEIGHT < HEIGHT:
                self.y += 4
            else:
                self.y = HEIGHT-PLAYER_HEIGHT

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))


class Ball:
    def __init__(self):
        self.pos = [WIDTH/2, HEIGHT/2]
        self.directions = [1, 0]
        self.speed = 2


def move(player1, player2, ball):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    ball.pos[1] += ball.directions[1]
    ball.pos[0] += ball.directions[0]*ball.speed
    keys = pygame.key.get_pressed()
    player1.move(keys)
    player2.move(keys)


def draw_game(win, player1, player2, ball):
    win.fill((0, 0, 0))
    player1.draw(win)
    player2.draw(win)
    pygame.draw.circle(win, (255, 255, 255), ball.pos, BALL_SIZE)
    text = FONT.render(str(player1.score), True, (255, 255, 255))
    win.blit(text, (WIDTH/4-text.get_width()/2, HEIGHT/4-text.get_height()/2))
    text = FONT.render(str(player2.score), True, (255, 255, 255))
    win.blit(text, (WIDTH - (WIDTH / 4 - text.get_width() / 2), HEIGHT / 4 - text.get_height() / 2))
    pygame.display.update()


def ball_y_collision(ball):
    if ball.pos[1] > HEIGHT:
        ball.directions[1] = - ball.directions[1]
        ball.pos[1] = HEIGHT-BALL_SIZE

    elif ball.pos[1] < 0:
        ball.directions[1] = - ball.directions[1]
        ball.pos[1] = 0


def ball_go_out(ball, player1, player2):
    if ball.pos[0]+BALL_SIZE > WIDTH:
        ball.pos[0] = WIDTH/2
        ball.pos[1] = HEIGHT / 2
        ball.directions[0] = - ball.directions[0]
        ball.directions[1] = 0
        player1.score += 1
        ball.speed = 2

    elif ball.pos[0]-BALL_SIZE < 0:
        ball.pos[0] = WIDTH/2
        ball.pos[1] = HEIGHT / 2
        ball.directions[0] = - ball.directions[0]
        ball.directions[1] = 0
        player2.score += 1
        ball.speed = 2


def calculate_angle(ball, player):
    return -(player.y + PLAYER_HEIGHT // 2 - ball.pos[1]) / 15


def check_collision_player(ball, player):
    return player.x+PLAYER_WIDTH//2 < ball.pos[0] < player.x + PLAYER_WIDTH \
                and player.y < ball.pos[1] + BALL_SIZE and ball.pos[1] - BALL_SIZE < player.y + PLAYER_HEIGHT


def player_collision(player1, player2, ball):
    if ball.directions[0] == -1:
        if check_collision_player(ball, player1):
            ball.directions[0] = -ball.directions[0]
            ball.directions[1] = calculate_angle(ball, player1)
            ball.speed = 4

    if ball.directions[0] == 1:
        if check_collision_player(ball, player2):
            ball.directions[0] = -ball.directions[0]
            ball.directions[1] = calculate_angle(ball, player2)
            ball.speed = 4


def collision(player1, player2, ball):
    ball_go_out(ball, player1, player2)
    ball_y_collision(ball)
    player_collision(player1, player2, ball)


def set_players():
    space = WIDTH/PLAYER_WIDTH
    player1 = Player(space, HEIGHT/2, pygame.K_w, pygame.K_s)
    player2 = Player(WIDTH-PLAYER_WIDTH-space, HEIGHT/2, pygame.K_UP, pygame.K_DOWN)
    return player1, player2


def draw_end(win, name):
    win.fill((0, 0, 0))
    text = FONT.render(f"{name} is the winner", True, (255, 255, 255))
    win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2))
    pygame.display.update()


def end_screen(win, name):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        draw_end(win, name)


if __name__ == '__main__':
    player1, player2 = set_players()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    ball = Ball()

    clock = pygame.time.Clock()
    while True:
        clock.tick(150)
        move(player1, player2, ball)
        draw_game(win, player1, player2, ball)
        collision(player1, player2, ball)
        if player1.score > 10:
            end_screen(win, "player 1")
            break
        elif player2.score > 10:
            end_screen(win, "player 2")
            break