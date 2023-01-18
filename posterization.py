import cv2
import os
import numpy as np
import argparse
import json

""" view """
SHADOW_UPPER = 25
IN_LOWER = 20
IN_UPPER = 85
OUT_LOWER = 150
EDGE = 2

""" portrait """
# SHADOW_UPPER = 75   # large value leads to large shadow 
# IN_LOWER = 50       # dismiss dark area (< SHADOW_UPPER)
# IN_UPPER = 225      # large value makes large white area
# OUT_LOWER = 200     # large value makes output brighter

def main():
    args = get_parser()
    out_dir = args.input.split(".")[0]
    img = cv2.imread(args.input)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 4)
    edge_img, shadow_img, sync_img = edge_shadow_extract(gray_img, edge=args.edge, shadow_upper=args.shadow)
    cv2.imwrite("{}/edge.jpg".format(out_dir), edge_img)
    cv2.imwrite("{}/shadow.jpg".format(out_dir), shadow_img)
    cv2.imwrite("{}/sync.jpg".format(out_dir), sync_img)
    pos_img = posterization(gray_img, n=args.n, in_lower=args.in_lower, in_upper=args.in_upper, out_lower=args.out_lower)
    cv2.imwrite("{}/poster.jpg".format(out_dir), pos_img)
    fin_img = cv2.bitwise_and(pos_img, sync_img)
    #fin_img = cv2.applyColorMap(fin_img, cv2.COLORMAP_OCEAN)
    fin_img = cv2.applyColorMap(fin_img, cv2.COLORMAP_DEEPGREEN)
    cv2.imwrite("{}/final.jpg".format(out_dir), fin_img)

def get_parser():
    parser = argparse.ArgumentParser(description="posterization")
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-n", type=int, default=4)
    parser.add_argument("-shadow", type=int, default=25)
    parser.add_argument("-in_lower", type=int, default=20)
    parser.add_argument("-in_upper", type=int, default=85)
    parser.add_argument("-out_lower", type=int, default=150)
    parser.add_argument("-edge", type=int, default=2)
    args = parser.parse_args()

    for k, v in vars(args).items():
        print("{:12s}: {}".format(k, v))

    config = vars(args)
    out_dir = args.input.split(".")[0]
    os.makedirs(out_dir, exist_ok=True)
    with open("{}/config.json".format(out_dir), "w") as f:
        json.dump(config, f)
    return args

def edge_shadow_extract(gray, edge=3, shadow_upper=25):
    cv2.imwrite("blur.jpg", gray)
    edge_img = 255 * np.ones(gray.shape).astype(np.uint8)
    if edge > 0:
        kernel = np.ones((edge,edge),np.uint8)
        edge_img = cv2.Canny(gray, 100, 150)
        edge_img = 255 - cv2.dilate(edge_img, kernel, iterations=1)
    _, shadow_img = cv2.threshold(gray, shadow_upper, 255, cv2.THRESH_BINARY)
    shadow_img = cv2.GaussianBlur(shadow_img, (9, 9), 5)
    sync_img = cv2.bitwise_and(edge_img, shadow_img)
    return edge_img, shadow_img, sync_img

def posterization(img, n=4, in_lower=20, in_upper=85, out_lower=150):
    x = np.arange(256)
    ibins = np.linspace(0, 255, n+1)
    ibins_mid = np.linspace(in_lower, in_upper, n-1)
    ibins[1:-1] = ibins_mid
    obins = np.linspace(0, 255, n)
    obins_mid = np.linspace(out_lower, 255, n-1)
    obins[1:] = obins_mid
    digit = np.digitize(x, ibins)-1
    digit[:int(ibins[1])] = n-1
    digit[255] = n-1
    y = obins[digit]
    pos = cv2.LUT(img, y)
    return pos.astype(np.uint8)

if __name__ == "__main__":
    main()