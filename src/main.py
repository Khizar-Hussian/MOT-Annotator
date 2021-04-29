import cv2
import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Simple MOT Annotator")
    parser.add_argument("--images", type=str,
                        help="path to images folder", default="./images")
    parser.add_argument("--annots", type=str,
                        help="path to annotations folder", default="./annotations")
    args = parser.parse_args()

    imgs_path = args.images
    anot_path = args.annots

    if not os.path.isdir(imgs_path):
        sys.exit(f"[!] Error: path '{imgs_path}' for --images is invalid.")
    if not os.path.isdir(anot_path):
        sys.exit(f"[!] Error: path '{anot_path}' for --annots is invalid.")
    print("It works till here.")


if __name__ == "__main__":
    main()
