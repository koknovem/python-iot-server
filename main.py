import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        heatmapNumpy = heatmapNumpy.astype('uint8')
        grayImage = cv2.cvtColor(heatmapNumpy, cv2.COLOR_GRAY2BGR)
        cv2.imshow("heatmap", grayImage)
        time.sleep(1)


if (__name__ == "__main__"):
    main()
