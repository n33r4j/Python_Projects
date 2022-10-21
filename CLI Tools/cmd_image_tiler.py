# Commandline Image Tiler
# Assumes all images are of same dimensions

from PIL import Image
from argparse import ArgumentParser
import os
import glob


def find_images(img_path):
    # Find all images given folder and return list of filenames/paths.
    os.chdir(img_path)
    types = ('*.png', '*.jpg', '*.jpeg')
    image_names = []
    for file_type in types:
        image_names.extend(glob.glob(file_type))
    
    return image_names


parser = ArgumentParser()
parser.add_argument("--path", help="Path to the folder of images", required=True)
parser.add_argument("--dims", nargs="+", help="Dimensions to generate tile (rows, cols)", required=True)
parser.add_argument("--rowSpace", default=5, help="Space between rows", required=False)
parser.add_argument("--colSpace", default=5, help="Space between columns", required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    
    rows, cols = tuple([int(d) for d in args.dims])
    tiles = find_images(args.path)
    if rows*cols < len(tiles):
        raise Exception("Tiling dimensions too small to include all images. Please increase the no. of rows or columns.")
    else:
        tile_W, tile_H = Image.open(tiles[0]).size
        final_image = Image.new('RGBA', ((cols*(args.colSpace+tile_W) - args.colSpace), (rows*(args.rowSpace+tile_H) - args.rowSpace)))

        paste_X = 0
        paste_Y = 0
        currRow = 0
        currCol = 0

        for img_name in tiles:
            tile_img = Image.open(img_name)
            final_image.paste(tile_img, (paste_X, paste_Y))
            currCol += 1
            paste_X += (args.rowSpace+tile_W)
            if currCol >= cols:
                currCol = 0
                paste_X = 0
                currRow += 1
                paste_Y += (args.rowSpace+tile_H)

        final_image.save("Tiled-Image"+".png")

        print("[ Tiling complete ]")
