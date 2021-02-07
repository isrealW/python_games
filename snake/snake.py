import random
import pygame
import time
pygame.init()


WIDTH, HEIGHT = 800, 600
CUBE_SIZE = 40
FONT = pygame.font.SysFont('comicsans', WIDTH//25)
FONT2 = pygame.font.SysFont('comicsans', WIDTH//20)
BOARD_WIDTH, BOARD_HEIGHT = WIDTH // CUBE_SIZE, HEIGHT // CUBE_SIZE


class Player:
    def __init__(self):
        pos = (BOARD_WIDTH//2, BOARD_HEIGHT//2)
        self.lst = [pos]
        self.ate = False
        self.direction = -1
        self.score = 0


def Input(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player.direction != 1:
            player.direction = 0
        return True
    elif keys[pygame.K_RIGHT]:
        if player.direction != 0:
            player.direction = 1
        return True
    elif keys[pygame.K_UP]:
        if player.direction != 3:
            player.direction = 2
        return True
    elif keys[pygame.K_DOWN]:
        if player.direction != 2:
            player.direction = 3
        return True
    return False


def spown_food(lst):
    lst[0] = random.randint(1, BOARD_WIDTH)
    lst[1] = random.randint(1, BOARD_HEIGHT)


def draw(win ,player, food):
    win.fill((0, 0, 0))

    for i in range(0, WIDTH, CUBE_SIZE):
        pygame.draw.line(win, (30, 30, 30), (i, 0), (i, HEIGHT))

    for i in range(0, HEIGHT, CUBE_SIZE):
        pygame.draw.line(win, (30, 30, 30), (0, i), (WIDTH, i))

    pygame.draw.rect(win, (0, 255, 0),
        ((BOARD_WIDTH-food[0])*CUBE_SIZE+CUBE_SIZE//4, (BOARD_HEIGHT-food[1])*CUBE_SIZE+CUBE_SIZE//4
         , CUBE_SIZE//2, CUBE_SIZE//2))

    for cube in player.lst:
        pygame.draw.rect(win, (255, 0, 0), (
            (BOARD_WIDTH-cube[0])*CUBE_SIZE, (BOARD_HEIGHT-cube[1])*CUBE_SIZE,CUBE_SIZE, CUBE_SIZE))

        pygame.draw.rect(win, (255, 255, 255), (
            (BOARD_WIDTH - cube[0]) * CUBE_SIZE, (BOARD_HEIGHT - cube[1]) * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), 1)

    score = FONT.render("score: "+str(player.score), True, (255, 255, 255))
    win.blit(score, (0, 0))

    pygame.display.update()


def draw_start(win ,player, food):
    win.fill((0, 0, 0))
    text = FONT2.render("press any arrow key to start", True, (255, 255, 255))
    win.blit(text, (WIDTH//2-text.get_width() // 2, HEIGHT//2-text.get_height()//2))

    pygame.display.update()


def collision(player, food):
    head = player.lst[len(player.lst) - 1]
    if food[0] == head[0] and food[1] == head[1]:
        player.eat = True
        player.score += 1
    else:
        player.eat = False

    for cube in player.lst:
        if head == cube and not head is cube and not head is cube :
            return True

    if BOARD_WIDTH < head[0] or head[0] < 1 or BOARD_HEIGHT < head[1] or head[1] < 1:
        return True
    return False


def move(player, food):
    last_pos = player.lst[len(player.lst)-1]
    if player.direction == 0:
        player.lst.append((last_pos[0]+1, last_pos[1]))
    if player.direction == 1:
        player.lst.append((last_pos[0]-1, last_pos[1]))
    if player.direction == 2:
        player.lst.append((last_pos[0], last_pos[1]+1))
    if player.direction == 3:
        player.lst.append((last_pos[0], last_pos[1]-1))
    result = collision(player, food)
    if not player.eat:
        player.lst.remove(player.lst[0])
    else:
        spown_food(food)
    return result


def update_score_board(score_board, score):
    i = 0
    while i < len(score_board):
        if score > score_board[i]:
            num = score
            num2 = score_board[i]
            while i < len(score_board):
                score_board[i] = num
                num = num2
                i += 1
                try:
                    num2 = score_board[i]
                except:
                    pass
            break
        i += 1


def read_score_board():
    score_board = []
    with open("score_board.txt", "r") as f:
        for s in f.readlines():
            s = s.replace("\n", "")
            s = int(s)
            score_board.append(s)
    return score_board


def draw_score_board(score_board, score, win):
    win.fill((0, 0, 0))
    text = FONT.render("score_board :", True, (255, 255, 255))
    win.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//4-text.get_height()//2))
    i = 0
    while i<len(score_board):
        text = f"{i+1}. {str(score_board[i])}"
        text = FONT.render(text, True, (255, 255, 255))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + (i+1)*text.get_height()))
        i += 1

    text = FONT.render(f"your score is {score}", True, (255, 255, 255))
    win.blit(text, (0, HEIGHT-text.get_height()))

    pygame.display.update()


def write_score_board(score_board):
    with open("score_board.txt", "w") as f:
        text = ""
        for s in score_board[0:9]:
            text += str(s)+"\n"
        text += str(score_board[len(score_board)-1])
        f.write(text)


def run_score_board(win, score, second):
    score_board = read_score_board()
    update_score_board(score_board, score)
    run = True
    write_score_board(score_board)
    start_time = time.time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_score_board(score_board, score, win)
        if time.time() - start_time > second:
            break


def start(win, player, food):
    run = False
    while not run:
        run = Input(player)
        draw_start(win, player, food)


if __name__ == "__main__":
    clock = pygame.time.Clock()
    player = Player()
    food = [0, 0]
    spown_food(food)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("snake")
    start(win, player, food)

    while True:
        clock.tick(10)
        Input(player)
        result = move(player, food)
        if result:
            run_score_board(win, player.score, 3)
            break
        draw(win, player, food)