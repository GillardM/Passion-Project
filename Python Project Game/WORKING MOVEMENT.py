import pygame
from rooms import rooms


# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 32  # Size of each grid cell
GRID_WIDTH = 20
GRID_HEIGHT = 15
PLAYABLE_WIDTH = GRID_WIDTH * CELL_SIZE
PLAYABLE_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Screen Setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Calculate offsets to center the grid
offset_x = (SCREEN_WIDTH - PLAYABLE_WIDTH) // 2
offset_y = (SCREEN_HEIGHT - PLAYABLE_HEIGHT) // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

class player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def render(self, surface, offset_x, offset_y):
        rect = pygame.Rect(
            self.x * CELL_SIZE + offset_x,
            self.y * CELL_SIZE + offset_y,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)

class Object:
    def __init__(self, x, y, color, passable=False):
        self.x = x
        self.y = y
        self.color = color
        self.passable = passable

    def render(self, surface, offset_x, offset_y):
        rect = pygame.Rect(
            self.x * CELL_SIZE + offset_x,
            self.y * CELL_SIZE + offset_y,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)

# Check collision with impassable objects
def is_passable(x, y):
    for wall in walls:
        if wall.x == x and wall.y == y and not wall.passable:
            return False
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

player_pos = [5, 5]
walls = []

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False


    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos
    if keys[pygame.K_UP]:
        new_y -= 1
    if keys[pygame.K_DOWN]:
        new_y += 1
    if keys[pygame.K_LEFT]:
        new_x -= 1
    if keys[pygame.K_RIGHT]:
        new_x += 1

    if is_passable(new_x, new_y):
            player_pos = [new_x, new_y]


    screen.fill(WHITE)

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(
                x * CELL_SIZE + offset_x,
                y * CELL_SIZE + offset_y,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)
    
    
    for wall in walls:
        wall.render(screen, offset_x, offset_y)

    # Draw player
    player_rect = pygame.Rect(
        player_pos[0] * CELL_SIZE + offset_x,
        player_pos[1] * CELL_SIZE + offset_y,
        CELL_SIZE,
        CELL_SIZE,
    )
    pygame.draw.rect(screen, BLUE, player_rect)

    pygame.display.flip()

    clock.tick(10)

pygame.quit()

        
