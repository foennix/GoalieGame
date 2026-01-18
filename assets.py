import pygame

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKIN = (255, 224, 189)
GRASS_GREEN = (34, 139, 34)

# Text based pixel art
# '.' is transparent
# R: Red, G: Green, B: Blue, Y: Yellow, S: Skin, W: White, K: Black

PLAYER_IDLE = [
    "......KK......",
    "......KK......",
    ".....SSSS.....",
    ".....SSSS.....",
    "....GGGGGG....",
    "....GGGGGG....",
    "....GGGGGG....",
    "....GGGGGG....",
    ".....KKKK.....",
    ".....KKKK.....",
    ".....KKKK.....",
    "....KK..KK....",
    "....KK..KK....",
]

PLAYER_DIVE_LEFT = [
    "..............",
    "..............",
    "..............",
    "..SSSS.GGGGGG.",
    ".KKSSSSGGGGGG.",
    "..SSSS.GGGGGG.",
    ".......GGGGGG.",
    ".......KKKK...",
    ".......KKKK...",
    "......KK..KK..",
]

PLAYER_DIVE_RIGHT = [
    "..............",
    "..............",
    "..............",
    ".GGGGGG.SSSS..",
    ".GGGGGGSSSSKK.",
    ".GGGGGG.SSSS..",
    ".GGGGGG.......",
    "...KKKK.......",
    "...KKKK.......",
    "..KK..KK......",
]

PLAYER_JUMP = [
    "....WW..WW....", # Hands up
    "....WW..WW....",
    ".....SSSS.....",
    ".....SSSS.....",
    "....GGGGGG....",
    "....GGGGGG....",
    "....GGGGGG....",
    "....GGGGGG....",
    ".....KKKK.....",
    ".....KKKK.....",
    "....KK..KK....",
    "...KK....KK...",
    "..KK......KK..",
]

BALL = [
    "..WWWW..",
    ".WKKKKW.",
    "WKKWWKKW",
    "WKWKKWKW",
    "WKKWWKKW",
    ".WKKKKW.",
    "..WWWW..",
]

COLOR_MAP = {
    'R': RED,
    'G': GREEN,
    'B': BLUE,
    'Y': YELLOW,
    'S': SKIN,
    'W': WHITE,
    'K': BLACK,
    '.': None  # Transparent
}

def create_surface_from_art(art_data, scale=4):
    """
    Creates a pygame Surface from a list of strings representing pixel art.
    """
    height = len(art_data)
    width = len(art_data[0])

    surface = pygame.Surface((width * scale, height * scale), pygame.SRCALPHA)

    for y, row in enumerate(art_data):
        for x, char in enumerate(row):
            color = COLOR_MAP.get(char)
            if color:
                pygame.draw.rect(
                    surface,
                    color,
                    (x * scale, y * scale, scale, scale)
                )

    return surface
