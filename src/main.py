import cv2
import os
import sys
import json
import numpy as np
import tkinter as tk
import argparse


def get_annotation(path):
    if not os.path.exists(path):
        return None
    data = None
    with open(path, "r") as f:
        data = json.load(f)
    return data


def annotate_image(img, annot, color_dict):
    for idx in annot:
        if idx not in color_dict:
            color_dict[idx] = list(np.random.random(size=3) * 256)
        color = color_dict[idx]
        coords = annot[idx]
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, idx, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))
    return img


def start_annotator(imgs_path, anot_path, img_count, ant_count, color_dict):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", 1920, 1080)
    idx = 0
    imfiles = sorted(os.listdir(imgs_path), key=lambda x: int(x.split('.')[0]))
    while idx < img_count:
        imfile = imfiles[idx]
        if not imfile.endswith(".png"):
            sys.exit(1)

        img = cv2.imread(os.path.join(imgs_path, imfile))
        anfile = imfile.split(".")[0] + ".json"
        anot = get_annotation(os.path.join(anot_path, anfile))
        annotated_image = annotate_image(img.copy(), anot, color_dict)
        cv2.putText(annotated_image, imfile, (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
        cv2.imshow("image", annotated_image)
        print(anot)
        print(imfile)
        key = cv2.waitKey()
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('r') or key == ord('R'):
            continue
        elif (key == ord('n') or key == ord('N')) and idx < img_count:
            idx += 1
        elif (key == ord('p') or key == ord('P')) and idx > 0:
            idx -= 1
    cv2.destroyAllWindows()


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

    color_dict = {}
    start_annotator(imgs_path, anot_path, img_count, ant_count, color_dict)


if __name__ == "__main__":
    main()
