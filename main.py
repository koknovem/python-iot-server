import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        heatmapNumpy = heatmapNumpy.astype('uint8')
        cv2.imshow("heatmap", heatmapNumpy)
        time.sleep(1)


if (__name__ == "__main__"):
    main()
