import pygame
import numpy as np
import random

import time

from generate_corners import check_grass_tile, check_sand_tile, check_stone_tile


def generate_terrain():
    arr = np.loadtxt('map.txt', dtype=object)  
    return arr

'''def blit_terrain(screen, window_size, tile_size, x, y, terrain_map, grass_img, terrain_images_size, terrain_images):
    screen.fill((0,0,0))
    blit_list = []
    for height in range(int(window_size[1]/tile_size) + 1):
        for width in range(int(window_size[0]/tile_size) + 1):
            tile_type = terrain_map[int(height + y/tile_size), int(width + x/tile_size)]
            if tile_type == 4:
                tile = grass_img.subsurface((random.randint(0,3)*terrain_images_size, random.randint(0,3) * terrain_images_size, 64, 64))
                #tile = grass_img.subsurface(0*terrain_images_size, 0 * terrain_images_size, 64, 64)
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 8:
                tile = check_grass_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 9:
                tile = check_stone_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 10:
                tile = check_sand_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            else:
                blit_list.append((terrain_images[max(tile_type - 2, 0)], (width*tile_size - x%tile_size, height*tile_size - y%tile_size))) # - 2 for proper item from list, max to account for different blues in tile map
    
    screen.blits(blit_list)

    return screen'''

def get_grass_tile(index, spritesheet, tile_size):
    x = index % 4
    y = index // 4

    tile = spritesheet.subsurface((x*tile_size, y*tile_size, tile_size, tile_size))
    return tile

def blit_terrain(screen, window_size, tile_size, x_pos, y_pos, terrain_map, grass_img, terrain_images_size, terrain_images, tile_surfaces):
    screen.fill((0,0,0))
    blit_list = []
    
    start = time.time()
    for y, row in enumerate(terrain_map):
        if int(y_pos/64) <= y <= int((y_pos + window_size[1])/64):
            for x, tile in enumerate(row):
                if int(x_pos/64) <= x <= int((x_pos + window_size[0])/64):

                    width = x-int(x_pos/64)
                    height = y-int(y_pos/64)
                    # Determine the surface to use based on the tile value
                    if tile == "gE":
                        tile = check_grass_tile(terrain_map, int(height + y_pos/tile_size), int(width + x_pos/tile_size))
                        blit_list.append((tile, (width*tile_size - x_pos%tile_size, height*tile_size - y_pos%tile_size)))
                    elif tile == "saE":
                        tile = check_sand_tile(terrain_map, int(height + y_pos/tile_size), int(width + x_pos/tile_size))
                        blit_list.append((tile, (width*tile_size - x_pos%tile_size, height*tile_size - y_pos%tile_size)))
                    elif tile == "stE":
                        tile = check_stone_tile(terrain_map, int(height + y_pos/tile_size), int(width + x_pos/tile_size))
                        blit_list.append((tile, (width*tile_size - x_pos%tile_size, height*tile_size - y_pos%tile_size)))
                    elif tile[0] == "g":
                        index = int(tile[1:])
                        test = tile_surfaces["g"][index]
                        blit_list.append((test, (width*tile_size - x_pos%tile_size, height*tile_size - y_pos%tile_size)))

                    else:
                        if tile in tile_surfaces:
                            tile_key = tile
                        else:
                            if tile[:2] in tile_surfaces:
                                tile_key = tile[:2]
                            else:
                                tile_key = tile[0]

                        #print(f"\'{tile_key}\'")
                        blit_list.append((tile_surfaces[tile_key], (width*tile_size - x_pos%tile_size, height*tile_size - y_pos%tile_size)))
    print(time.time() - start)
    screen.blits(blit_list)

    return screen