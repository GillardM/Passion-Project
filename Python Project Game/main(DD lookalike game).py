import pygame

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

#Button class for menu
# Button class for menu
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = LIGHT_GRAY

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2)  # Border
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Game state variables
player_pos = [5, 5]  # Starting position on the grid
walls = []

# Fill the outermost parts of the grid with walls
for x in range(GRID_WIDTH):
    walls.append(Object(x, 0, BLACK))  # Top row
    walls.append(Object(x, GRID_HEIGHT - 1, BLACK))  # Bottom row

for y in range(GRID_HEIGHT):
    walls.append(Object(0, y, BLACK))  # Left column
    walls.append(Object(GRID_WIDTH - 1, y, BLACK))  # Right column

# Discovered tiles
discovered_tiles = set()

# Menu state
game_running = True
in_menu = False

# Menu actions
def resume_game():
    global in_menu
    in_menu = False

def exit_game():
    global game_running
    game_running = False

# Create menu buttons
menu_buttons = [
    Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Resume", resume_game),
    Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50, "Empty", None),
    Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50, "Exit", exit_game),
]

# Discover tiles within a radius
def discover_tiles(x, y, radius):
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                discovered_tiles.add((nx, ny))

# Check collision with impassable objects
def is_passable(x, y):
    for wall in walls:
        if wall.x == x and wall.y == y and not wall.passable:
            return False
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

# Game loop
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = not in_menu
        elif event.type == pygame.MOUSEBUTTONDOWN and in_menu:
            for button in menu_buttons:
                button.check_click(event.pos)

    if in_menu:
        # Render menu
        screen.fill(DARK_GRAY)
        for button in menu_buttons:
            button.render(screen)
    else:
        # Handle keys for game movement
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

        # Check collision
        if is_passable(new_x, new_y):
            player_pos = [new_x, new_y]

        # Discover tiles around the player
        discover_tiles(player_pos[0], player_pos[1], 2)

        # Clear screen
        screen.fill(WHITE)

        # Draw grid and discovered areas
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
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)  # Grid lines

        # Draw walls
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

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(10)

pygame.quit()
