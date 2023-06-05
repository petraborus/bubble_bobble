# uses different letters to represent teh different kinds of tiles and the player
# this is what the level will look like
level_map = [
    "                           ",
    "                           ",
    "z                         z",
    "z                         z",
    "z  yxxxxxxx    xxxxxxxy   z",
    "z  y                  y   z",
    "z  y     p            y   z",
    "z  yxxxxxxx    xxxxxxxy   z",
    "z  y                  y   z",
    "z  y                  y   z",
    "z  yxxxxxxx    xxxxxxxy   z",
    "z                         z",
    "z                         z",
    "yxxxxxxx    xxxx    xxxxxxy"]

# basic variables that will stay constant: used througout difefrent parts of the code
tile_size = 52
screen_width = 1400
screen_height = len(level_map) * tile_size
fps = 60

gravity = 0.8


