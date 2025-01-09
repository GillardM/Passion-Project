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

###player class, same as object class but movable
##class Player:
##    def __init__(self, x, y, color, passable=False):
##        self.x = x
##        self.y = y
##        self.color = color
##        self.passable = passable
##
##    def render(self, surface, offset_x, offset_y, discovered):
##        if discovered:
##            rect = pygame.Rect(
##                self.x * CELL_SIZE + offset_x,
##                self.y * CELL_SIZE + offset_y,
##                CELL_SIZE,
##                CELL_SIZE,
##            )
##            pygame.draw.rect(surface, self.color, rect)
##
#object class for walls and stuff

class Object:
    def __init__(self, x, y, color, passable=False):
        self.x = x
        self.y = y
        self.color = color
        self.passable = passable

    def render(self, surface, offset_x, offset_y):
        #if discovered:
        rect = pygame.Rect(
            self.x * CELL_SIZE + offset_x,
            self.y * CELL_SIZE + offset_y,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)



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

# Check collision with impassable objects
def is_passable(x, y):
    for wall in walls:
        if wall.x == x and wall.y == y and not wall.passable:
            return False
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


#menu stats
in_menu = False
game_running = True

player_pos = [5, 5]

current_room_key = "starting_room"
walls = load_room(current_room_key)


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False

    screen.fill(WHITE)

    
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
    #pygame.draw.rect(screen, PLAYER_HIGHLIGHT, player_rect, 2)



    pygame.display.flip()

pygame.quit()
