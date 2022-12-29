import cv2
import numpy as np

""" view """
SHADOW_UPPER = 25
IN_LOWER = 20
IN_UPPER = 85
OUT_LOWER = 150
EDGE = 0

""" portrait """
SHADOW_UPPER = 75   # large value leads to large shadow 
IN_LOWER = 50       # dismiss dark area (< SHADOW_UPPER)
IN_UPPER = 225      # large value makes large white area
OUT_LOWER = 200     # large value makes output brighter

def main():
    img = cv2.imread("input4.JPG")
    # img = cv2.imread("input5.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 4)
    sync = edge_shadow_extract(gray, edge=EDGE, shadow_upper=SHADOW_UPPER)
    pos = posterization(gray, in_lower=IN_LOWER, in_upper=IN_UPPER, out_lower=OUT_LOWER)
    cv2.imwrite("poster.jpg", pos)
    fin = cv2.bitwise_and(pos, sync)
    fin = cv2.applyColorMap(fin, cv2.COLORMAP_OCEAN)
    #fin = cv2.applyColorMap(fin, cv2.COLORMAP_DEEPGREEN)
    cv2.imwrite("final.jpg", fin)

def edge_shadow_extract(gray, edge=3, shadow_upper=25):
    cv2.imwrite("blur.jpg", gray)
    edge_img = 255 * np.ones(gray.shape).astype(np.uint8)
    if edge > 0:
        kernel = np.ones((edge,edge),np.uint8)
        edge_img = cv2.Canny(gray, 100, 150)
        edge_img = 255 - cv2.dilate(edge_img, kernel, iterations=1)
        cv2.imwrite("edge.jpg", edge_img)
    _, shadow_img = cv2.threshold(gray, shadow_upper, 255, cv2.THRESH_BINARY)
    cv2.imwrite("shadow.jpg", shadow_img)
    sync_img = cv2.bitwise_and(edge_img, shadow_img)
    cv2.imwrite("sync.jpg", sync_img)
    return sync_img

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