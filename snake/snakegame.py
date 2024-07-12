import pygame
import sys
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
White = (255, 255, 255)

snake_x = 350
snake_y = 250
speed_x = 0
speed_y = 0

score = 0

font = pygame.font.Font("PressStart2P.ttf", 20)

clock = pygame.time.Clock()

food_x = random.randint(0, 950)
food_y = random.randint(0, 750)

snake_list = []
length = 1
game_over = False
highscore = 0
direction = "RIGHT"

blink_interval = 500  # milliseconds
last_blink_time = pygame.time.get_ticks()
text_visible = True


def snake_head():
    global snake_x, snake_y, game_over
    head = []
    head.append(snake_x)
    head.append(snake_y)
    snake_list.append(head)
    if len(snake_list) > length:
        del snake_list[0]
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, (x[0], x[1], 20, 20))
        pygame.draw.rect(screen, BLACK, (x[0] - 1, x[1] - 1, 22, 22), 1)

        # print(snake_x, snake_y)
    if head in snake_list[:-1]:
        game_over = True


def snake_food():
    pygame.draw.rect(screen, RED, (food_x, food_y, 20, 20))


def Text(text, color, x, y):
    if text_visible:
        text = font.render(text, True, color)
        screen.blit(text, [x, y])


def score_board():
    global score, food_x, food_y, length, highscore

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
        score += 2
        if score > int(highscore):
            highscore = score

        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

        length = length + 2
        # print("Score:", score)
        food_x = random.randint(0, 950)
        food_y = random.randint(0, 750)
        # print("Food position", food_x, food_y)
    # Text("Score:" + str(score) + "   High Score:" + str(highscore), White, 10, 760)
    text = font.render("Score:" + str(score) + "   High Score:" + str(highscore), True, White)
    screen.blit(text, [10,760])

def Game_over():
    global game_over, snake_x, snake_y, speed_x, speed_y, snake_list, length, score, food_x, food_y,last_blink_time,current_time,blink_interval,text_visible

    waiting = True
    while waiting:
        screen.fill(White)
        background_image = pygame.image.load("snake2.webp")
        background_image = pygame.transform.scale(background_image, (1000, 800))
        screen.blit(background_image, (0, 0))
        Text("Game Over!!! ", RED, 400, 600)
        Text("Press Enter To Continue", RED, 280, 630)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    game_over = False
                    snake_x = 350
                    snake_y = 250
                    speed_x = 0
                    speed_y = 0
                    snake_list = []
                    length = 1
                    score = 0
                    food_x = random.randint(0, 950)
                    food_y = random.randint(0, 750)
                    main()

        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time >= blink_interval:
            text_visible = not text_visible
            last_blink_time = current_time

        pygame.display.update()
        clock.tick(60)


def welcome():
    global current_time, last_blink_time, blink_interval, text_visible
    while True:
        screen.fill(White)

        background_image = pygame.image.load("snake.jpg")
        background_image = pygame.transform.scale(background_image, (1000, 800))
        screen.blit(background_image, (0, 0))
        Text("Welcome to Snake Game", RED, 290, 130)
        Text("Press Space Bar To Play", RED, 262, 740)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time >= blink_interval:
            text_visible = not text_visible
            last_blink_time = current_time

        pygame.display.update()
        clock.tick(60)


def screen_border():
    global snake_x, snake_y
    if snake_x >= 1000:
        snake_x = 0
    elif snake_x < 0:
        snake_x = 1000
    if snake_y >= 800:
        snake_y = 0
    elif snake_y < 0:
        snake_y = 800


def main():
    global snake_x, snake_y, speed_x, speed_y, paused, snake_list, game_over, direction
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    # print("You have pressed the right key")
                    speed_x = 5
                    speed_y = 0
                    direction = "RIGHT"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    # print("You have pressed the left key")
                    speed_x = -5
                    speed_y = 0
                    direction = "LEFT"
                if event.key == pygame.K_UP and direction != "DOWN":
                    # print("You have pressed the up key")
                    speed_y = -5
                    speed_x = 0
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    # print("You have pressed the down key")
                    speed_y = 5
                    speed_x = 0
                    direction = "DOWN"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        print("Game paused")
                    else:
                        print("Game resumed")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not paused and not game_over:
            snake_x += speed_x
            snake_y += speed_y

            screen.fill(BLACK)
            snake_head()
            snake_food()
            score_board()
            screen_border()

        if game_over:
            Game_over()

        pygame.display.flip()
        clock.tick(60)


welcome()
