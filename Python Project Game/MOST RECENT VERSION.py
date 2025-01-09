import pygame
from rooms2 import rooms  # Import the room data from rooms2

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
BROWN = (139, 69, 19)  # Color for the doors
YELLOW = (255, 255, 0)  # Color for the treasure
GREEN = (0, 255, 0)  # Color for the key

# Screen Setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Calculate offsets to center the grid
offset_x = (SCREEN_WIDTH - PLAYABLE_WIDTH) // 2
offset_y = (SCREEN_HEIGHT - PLAYABLE_HEIGHT) // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Player:
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
    def __init__(self, x, y, color, passable=False, type=""):
        self.x = x
        self.y = y
        self.color = color
        self.passable = passable
        self.type = type

    def render(self, surface, offset_x, offset_y):
        rect = pygame.Rect(
            self.x * CELL_SIZE + offset_x,
            self.y * CELL_SIZE + offset_y,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)

#button class
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


# Load room data and convert it into objects
def load_room(room_key):
    room_data = rooms.get(room_key, {})
    objects = []

    for y, row in enumerate(room_data["coordinates"]):
        for x, cell in enumerate(row):
            if cell == "wall":
                objects.append(Object(x, y, BLACK, passable=False))  # Black walls
            elif cell == "floor":
                objects.append(Object(x, y, GRAY, passable=True))  # Gray floors
            elif cell == "door":
                objects.append(Object(x, y, BROWN, passable=False, type="door"))  # Brown doors
            elif cell == "treasure":
                objects.append(Object(x, y, YELLOW, passable=True, type="treasure"))  # Yellow treasure
            elif cell == "key":
                objects.append(Object(x, y, GREEN, passable=True, type="key"))  # Green key
    return objects

# Check collision with impassable objects (excluding doors)
def is_passable(x, y, key_collected):
    for obj in walls:
        if obj.x == x and obj.y == y:
            if obj.type == "door" and not key_collected:
                return False  # If it's a door and the key hasn't been collected, it's not passable
            if not obj.passable:
                return False  # Any other impassable objects
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

# Create player and load room objects
player_pos = [5, 5]
key_collected = False  # Initially, the player hasn't collected the key
walls = load_room("starting_room")
game_won = False
in_menu = False

#menu actions
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


#main game loop
game_running = True
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
            

    elif game_won:
        # Display the "YOU WIN!" message
        font = pygame.font.Font(None, 74)
        win_text = font.render("YOU WIN!", True, (255, 255, 255))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        continue  # Skip the normal game loop until player quits

    else:
        keys = pygame.key.get_pressed()
        new_x, new_y = player_pos
        if keys[pygame.K_LEFT]:
            new_x -= 1
        elif keys[pygame.K_RIGHT]:
            new_x += 1
        elif keys[pygame.K_UP]:
            new_y -= 1
        elif keys[pygame.K_DOWN]:
            new_y += 1

        # Check for passable space (excluding walls and boundaries)
        if is_passable(new_x, new_y, key_collected):
            player_pos = [new_x, new_y]

            # Check if the player reaches the treasure
            for obj in walls:
                if obj.type == "treasure" and obj.x == player_pos[0] and obj.y == player_pos[1]:
                    game_won = True

                # Check if the player picks up the key
                if obj.type == "key" and obj.x == player_pos[0] and obj.y == player_pos[1]:
                    key_collected = True
                    # Remove the key and change its color to grey (or make it disappear)
                    obj.color = GRAY
                    obj.passable = True  # Make the key a passable object now
                    walls.remove(obj)  # Remove the key from the room once collected

                # After collecting the key, unlock the door (change its passable status)
                if obj.type == "door" and key_collected and obj.passable == False:
                    obj.passable = True  # Unlock the door

        # Render the room
        screen.fill(WHITE)
        for obj in walls:
            obj.render(screen, offset_x, offset_y)

        # Render player
        player = Player(player_pos[0], player_pos[1], BLUE)
        player.render(screen, offset_x, offset_y)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
