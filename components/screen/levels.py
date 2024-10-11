import random
from random import randint, choice

from components.instances.terrain import Terrain

''' This function takes care of drawing the map automatically, but manually making a
    grid in the same size as the game's display. '''
def create_map(game):
    game.terrain = []

    # Grid used to spawn terrain, 1 allows spawning and 0 makes it empty
    # IMPORTANT: The rotation of the grid is different from the rotation
    # of the screen by 90 degrees clockwise
    terrain_grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    terrain_counter = 1
    terrain_type = randint(1, 2)
    ter1_sprites = [1, 2, 3, 4, 5]
    ter2_sprites = [3, 4, 5, 6, 7, 8, 9, 10]

    for row_index, row in enumerate(terrain_grid):
        for col_index, column in enumerate(row):
            terrain_counter += 1

            if column != 0 and terrain_counter % randint(1, 12) == 0:
                large_sprites = [3, 7, 8]  # Index for large sprites in the terrain sprites folder
                random_index = 1

                if terrain_type == 1:
                    random_index = random.choice(ter1_sprites)
                elif terrain_type == 2:
                    random_index = random.choice(ter2_sprites)

                if randint(1, 777) == 1: random_index = 99  # Rare snake sprite for flavor

                if not large_sprites.count(random_index) != 0:  # Condition for larger sprites
                    terrain_size = 70
                else:
                    terrain_size = 140

                pos_x = row_index * 80
                pos_y = col_index * 80
                new_asset = Terrain([pos_x, pos_y], random_index, terrain_size)
                game.terrain.append(new_asset)
