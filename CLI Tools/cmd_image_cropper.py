# Commandline Image Cropper

from PIL import Image
from argparse import ArgumentParser
import os
import glob


def find_images(img_path):
    # Find all images given folder and return list of filenames/paths
    os.chdir(img_path)
    types = ('*.png', '*.jpg', '*.jpeg')
    image_names = []
    for file_type in types:
        image_names.extend(glob.glob(file_type))
    
    return image_names


parser = ArgumentParser()
parser.add_argument("--mode", choices=["file", "folder"], help="Crop a single [file] or all images from a [folder]", required=True)
parser.add_argument("--path", help="Path to image file or folder", required=True)
parser.add_argument("--area", nargs="+", help="Area to keep (TopLeft X, TopLeft Y, BottomRight X, BottomRight Y)", required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.mode == "file":
        img = Image.open(args.path)
        cropped_image = img.crop(tuple([int(c) for c in args.area]))
        # cropped_image.show()
        cropped_image.save(img.filename + "-cropped" + ".png")
    elif args.mode == "folder":
        for img_name in find_images(args.path):
            img = Image.open(img_name)
            cropped_image = img.crop(tuple([int(c) for c in args.area]))
            print(f"[ Cropping -> {img.filename} ]")
            # cropped_image.show()
            cropped_image.save(img.filename + "-cropped" + ".png")
    print("[ Cropping complete ]")
