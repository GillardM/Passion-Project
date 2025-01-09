# Room data for the game

# Each room is defined by its coordinates, allowing for specific customization of each cell
rooms = {
    "starting_room": {
        "room_name": "Starting Room",
        "coordinates": {
            # Define each cell by its (x, y) coordinate
            (0, 0): {"type": "wall"}, (1, 0): {"type": "wall"}, (2, 0): {"type": "wall"},
            # Add all top-row walls
            **{(x, 0): {"type": "wall"} for x in range(20)},
            # Add all bottom-row walls
            **{(x, 14): {"type": "wall"} for x in range(20)},
            # Add left and right walls
            **{(0, y): {"type": "wall"} for y in range(15)},
            **{(19, y): {"type": "wall"} for y in range(15)},
            # Example: Adding a wall in the middle of the room
            (10, 7): {"type": "wall"},
            # Add floor tiles for all other spaces (optional, can be left empty if default is floor)
            **{(x, y): {"type": "floor"} for x in range(1, 19) for y in range(1, 14) if (x, y) not in [(10, 7)]},
        },
    },
    "another_room": {
        "room_name": "Another Room",
        "coordinates": {
            # Example: Walls around the edges and a specific internal layout
            **{(x, 0): {"type": "wall"} for x in range(20)},
            **{(x, 14): {"type": "wall"} for x in range(20)},
            **{(0, y): {"type": "wall"} for y in range(15)},
            **{(19, y): {"type": "wall"} for y in range(15)},
            (5, 5): {"type": "enemy"},  # Example of an enemy placement
            (10, 10): {"type": "item", "name": "treasure"},  # Example of an item placement
        },
    },
}
