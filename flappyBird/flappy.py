import pygame
from sys import exit
import random


#game variable
GAME_WIDTH = 280
GAME_HEIGHT = 510

# Bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 60
bird_height = 60

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

# Pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 180
pipe_height = 300
class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

# game image
background_image = pygame.image.load("flappy_bird/bgBird.jpg")
bird_image = pygame.image.load("flappy_bird/bird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("flappy_bird/pipeTop.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("flappy_bird/pipeBottom.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

# Game logic
bird = Bird(bird_image)
pipes = []
velocity_x = -2 # Kecepatan gerak pipa ke kiri
velocity_y = 0 # Kecepatan gerak burung atas/bawah
gravity = 0.4
score = 0
game_over = False

# Margin untuk mengecilkan hitbox burung dibanding gambar aslinya
BIRD_HITBOX_MARGIN = 8

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)
        # pygame.draw.rect(window, "red", pipe, 2)  # aktifkan kalau mau lihat hitbox pipa

    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y + bird.height > GAME_HEIGHT:
        bird.y = GAME_HEIGHT - bird.height
        game_over = True
        return

    # Hitbox burung yang sedikit lebih kecil dari gambar aslinya,
    # supaya area transparan di sekitar sprite tidak dihitung tabrakan
    bird_hitbox = pygame.Rect(
        bird.x + BIRD_HITBOX_MARGIN,
        bird.y + BIRD_HITBOX_MARGIN,
        bird.width - BIRD_HITBOX_MARGIN * 2,
        bird.height - BIRD_HITBOX_MARGIN * 2,
    )

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5 # Karena ada 2 pipa yang di mana 0.5*2 = 1
            pipe.passed = True

        collision_rect = pygame.Rect(pipe.x + 40, pipe.y, 100, pipe.height)

        if bird_hitbox.colliderect(collision_rect):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0) # Remove first element form the list

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2) # 0-h/2
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

def reset_game():
    global bird, pipes, velocity_y, score, game_over
    bird = Bird(bird_image)
    pipes = []
    velocity_y = 0
    score = 0
    game_over = False

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) # Tanda setiap 1.5 detik

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer and not game_over:
            create_pipes()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                if game_over:
                    reset_game()
                else:
                    velocity_y = -6

    if not game_over:
        move()

    draw()
    pygame.display.update()
    clock.tick(60) # 60 fps
