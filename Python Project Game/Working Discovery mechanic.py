import pygame

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
PLAYABLE_WIDTH = GRID_WIDTH * CELL_SIZE
PLAYABLE_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# Screen Setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
offset_x = (SCREEN_WIDTH - PLAYABLE_WIDTH) // 2
offset_y = (SCREEN_HEIGHT - PLAYABLE_HEIGHT) // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Object class for walls and other entities
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

# Game state variables
player_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2]  # Start at the center
discovered_tiles = set()
game_running = True
in_menu = False

# Define rooms
rooms = {
    "room1": {
        "walls": [
            Object(x, 0, BLACK) for x in range(GRID_WIDTH)
        ] + [
            Object(x, GRID_HEIGHT - 1, BLACK) for x in range(GRID_WIDTH)
        ] + [
            Object(0, y, BLACK) for y in range(GRID_HEIGHT)
        ] + [
            Object(GRID_WIDTH - 1, y, BLACK) for y in range(GRID_HEIGHT)
        ],
        "exits": {"top": "room2", "bottom": None, "left": None, "right": None},
    },
    "room2": {
        "walls": [
            Object(x, 0, BLACK) for x in range(GRID_WIDTH)
        ] + [
            Object(x, GRID_HEIGHT - 1, BLACK) for x in range(GRID_WIDTH)
        ] + [
            Object(0, y, BLACK) for y in range(GRID_HEIGHT)
        ] + [
            Object(GRID_WIDTH - 1, y, BLACK) for y in range(GRID_HEIGHT)
        ],
        "exits": {"top": None, "bottom": "room1", "left": None, "right": None},
    },
}

current_room = "room1"

# Discover tiles within a radius
def discover_tiles(x, y, radius):
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                discovered_tiles.add((nx, ny))

# Check collision with impassable objects
def is_passable(x, y):
    for wall in rooms[current_room]["walls"]:
        if wall.x == x and wall.y == y and not wall.passable:
            return False
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

# Handle room transitions
def check_room_transition(x, y):
    global current_room, player_pos
    exits = rooms[current_room]["exits"]
    if y == 0 and exits["top"]:
        current_room = exits["top"]
        player_pos = [GRID_WIDTH // 2, GRID_HEIGHT - 2]  # Enter from the bottom
    elif y == GRID_HEIGHT - 1 and exits["bottom"]:
        current_room = exits["bottom"]
        player_pos = [GRID_WIDTH // 2, 1]  # Enter from the top
    elif x == 0 and exits["left"]:
        current_room = exits["left"]
        player_pos = [GRID_WIDTH - 2, GRID_HEIGHT // 2]  # Enter from the right
    elif x == GRID_WIDTH - 1 and exits["right"]:
        current_room = exits["right"]
        player_pos = [1, GRID_HEIGHT // 2]  # Enter from the left

# Game loop
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = not in_menu

    if not in_menu:
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
            check_room_transition(new_x, new_y)

        discover_tiles(player_pos[0], player_pos[1], 2)

        screen.fill(WHITE)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(
                    x * CELL_SIZE + offset_x,
                    y * CELL_SIZE + offset_y,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                if (x, y) in discovered_tiles:
                    pygame.draw.rect(screen, WHITE, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)

        for wall in rooms[current_room]["walls"]:
            wall.render(screen, offset_x, offset_y)

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

