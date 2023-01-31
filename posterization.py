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

class Posterization():
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        self.gray_img = cv2.GaussianBlur(self.gray_img, (5, 5), 4)
    
    def get_output(self, n=4, edge=2, shadow_upper=25, in_lower=20, in_upper=85, out_lower=150, color=0):
        colormap = [cv2.COLORMAP_DEEPGREEN, cv2.COLORMAP_OCEAN, cv2.COLORMAP_AUTUMN]
        _, _, sync_img = self.edge_shadow_extract(edge=edge, shadow_upper=shadow_upper)
        pos_img = self.posterization(n=n, in_lower=in_lower, in_upper=in_upper, out_lower=out_lower)
        fin_img = cv2.bitwise_and(pos_img, sync_img)
        fin_img = cv2.applyColorMap(fin_img, colormap[color])
        return fin_img

    def edge_shadow_extract(self, edge=3, shadow_upper=25):
        gray = self.gray_img
        edge_img = 255 * np.ones(gray.shape).astype(np.uint8)
        if edge > 0:
            kernel = np.ones((edge,edge),np.uint8)
            edge_img = cv2.Canny(gray, 100, 150)
            edge_img = 255 - cv2.dilate(edge_img, kernel, iterations=1)
        _, shadow_img = cv2.threshold(gray, shadow_upper, 255, cv2.THRESH_BINARY)
        shadow_img = cv2.GaussianBlur(shadow_img, (9, 9), 5)
        sync_img = cv2.bitwise_and(edge_img, shadow_img)
        return edge_img, shadow_img, sync_img

    def posterization(self, n=4, in_lower=20, in_upper=85, out_lower=150):
        img = self.gray_img
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