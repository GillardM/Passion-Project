import pygame
from rooms import rooms  # Import room data

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
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
PLAYER_HIGHLIGHT = (0, 100, 255)

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

    def render(self, surface, offset_x, offset_y, discovered):
        if discovered:
            rect = pygame.Rect(
                self.x * CELL_SIZE + offset_x,
                self.y * CELL_SIZE + offset_y,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(surface, self.color, rect)

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

# Load room data based on room key
def load_room(room_key):
    room_data = rooms.get(room_key, {})
    objects = []
    for (x, y), cell in room_data.get("coordinates", {}).items():
        if cell["type"] == "wall":
            objects.append(Object(x, y, BLACK))  # Walls are black
        elif cell["type"] == "floor":
            objects.append(Object(x, y, GRAY))  # Floors are gray
        # Add more conditions for other types if needed
    return objects

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

# Game state variables
player_pos = [5, 5]  # Starting position on the grid
current_room_key = "starting_room"
walls = load_room(current_room_key)
discovered_tiles = set()

#menu stats
in_menu = False
game_running = True


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

    # Clear screen
    screen.fill(WHITE)

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
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)  # makes the actual grid lines

        # Draw walls
        for obj in walls:
            obj.render(screen, offset_x, offset_y, (obj.x, obj.y) in discovered_tiles)

        # Draw player
        player_rect = pygame.Rect(
            player_pos[0] * CELL_SIZE + offset_x,
            player_pos[1] * CELL_SIZE + offset_y,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, PLAYER_HIGHLIGHT, player_rect, 2)  # Highlight the player

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)

pygame.quit()
