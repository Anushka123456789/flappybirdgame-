import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRAVITY = 0.5
JUMP = -8
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
GAP = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Bird class
class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.x = 100
        self.velocity = 0
        self.radius = 20

    def jump(self):
        self.velocity += JUMP

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - GAP - 50)

    def move(self):
        self.x -= 5

    def offscreen(self):
        return self.x < -PIPE_WIDTH

    def hits(self, bird):
        return bird.x > self.x and bird.x < self.x + PIPE_WIDTH and (bird.y < self.height or bird.y > self.height + GAP)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Initialize clock
clock = pygame.time.Clock()

# Initialize bird and pipes
bird = Bird()
pipes = [Pipe(WIDTH + i * 300) for i in range(2)]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    bird.move()

    # Check for collisions
    for pipe in pipes:
        pipe.move()
        if pipe.offscreen():
            pipes.remove(pipe)
            pipes.append(Pipe(WIDTH))

        if pipe.hits(bird):
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Add new pipe
    if random.uniform(0, 1) < 0.01:
        pipes.append(Pipe(WIDTH))

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (bird.x, int(bird.y)), bird.radius)
    
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe.x, 0, PIPE_WIDTH, pipe.height))
        pygame.draw.rect(screen, GREEN, (pipe.x, pipe.height + GAP, PIPE_WIDTH, HEIGHT - pipe.height - GAP))

    pygame.display.flip()
    clock.tick(30)
