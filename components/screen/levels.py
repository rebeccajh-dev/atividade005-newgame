from random import randint, choices

from components.instances.terrain import Terrain

''' This function takes care of drawing the map automatically, but manually making a
    grid in the same size as the game's display. '''
def create_map(level):
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
    terrain_list = []
    terrain_counter = 1

    for row_index, row in enumerate(terrain_grid):
        for col_index, column in enumerate(row):
            terrain_counter += 1

            if column != 0 and terrain_counter % randint(1, level.terrain_spacing) == 0:
                # Get a random bandit to spawn depending on chance
                spawns = []
                chances = []

                for terrain_type in level.enviroment:
                    spawns.append(terrain_type)
                    chances.append(terrain_type[3])

                random_terrain = choices(population=spawns, weights=chances)[0]

                pos_x = row_index * 80
                pos_y = col_index * 80
                new_asset = Terrain([pos_x, pos_y], random_terrain, terrain_counter, level)
                terrain_list.append(new_asset)

    return terrain_list


class Level:
    def __init__(self, name, config, game):
        self.name = name
        self.enviroment = config['enviroment']
        self.spawn_types = config['spawn_types']
        self.background_color = config['background']
        self.terrain_spacing = config['terrain_spacing']
        self.terrain_area_reduction = config['terrain_area_reduction']

        self.map = create_map(self)

        for terrain in self.map:
            terrain.distance_check(self)

        if self.name == 'desert':
            game.round_time = 240
            game.base_max_bandits = 2
            game.max_spawned = 2
            game.base_bandit_spawnrate = 300
            game.bandit_spawn_multi = [1, 2]

            game.ambush_time = randint(140, 160)
            game.difficulty_time = 15
        elif self.name == 'saloon':
            game.round_time = 240
            game.base_max_bandits = 3
            game.max_spawned = 2
            game.base_bandit_spawnrate = 220
            game.bandit_spawn_multi = [1, 2]
            game.can_spawn_bandits = True

            game.ambush_time = randint(140, 160)
            game.difficulty_time = 15
        elif self.name == 'barren':
            game.round_time = 180
            game.base_max_bandits = 4
            game.max_spawned = 3
            game.base_bandit_spawnrate = 200
            game.bandit_spawn_multi = [1, 3]
            game.can_spawn_bandits = True

            game.ambush_time = randint(80, 100)
            game.difficulty_time = 15
        else:
            game.round_time = 240
            game.base_max_bandits = 2
            game.max_spawned = 1
            game.base_bandit_spawnrate = 300
            game.bandit_spawn_multi = [1, 2]

            game.ambush_time = randint(140, 160)
            game.difficulty_time = 15