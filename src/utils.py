import os

FONT_SIZES = (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52) # Max index = 12

def get_asset_path(type, asset_name): # Platform neutral
    return os.path.join("../assets", type, asset_name)


#TODO pixel perfect collision
# https://stackoverflow.com/questions/48025283/pixel-perfect-collision-detection-for-sprites-with-a-transparent-background