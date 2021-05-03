import cv2
import os
import sys
import json
import tkinter as tk
import argparse


def get_annotation(path):
    if not os.path.exists(path):
        return None
    data = None
    with open(path, "r") as f:
        data = json.load(f)
    return data


def annotate_image(img, annot):
    for ids, coords in annot.items():
        color = list(np.random.random(size=3) * 256)
        cv2.rectangle(img, (coords[0], coords[1]),
                      (coords[2], coords[3]), color, 2)


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

    img_count = len(os.listdir(imgs_path))
    ant_count = len(os.listdir(anot_path))
    assert img_count != anot_path, f"[!] Error: Number if images ({img_count}) does not match number of annotation files ({ant_count})."

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", 1920, 1080)
    for imfile in sorted(os.listdir(imgs_path), key=lambda x: int(x.split('.')[0])):
        if not imfile.endswith(".png"):
            sys.exit(1)
        img = cv2.imread(os.path.join(imgs_path, imfile))
        anfile = imfile.split(".")[0] + ".json"
        anot = get_annotation(os.path.join(anot_path, anfile))
        annotated_image = annotate_image(img.copy(), anot)
        cv2.imshow("image", annotated_image)
        print(imfile)
        key = cv2.waitKey()
        if key == ord(" "):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
