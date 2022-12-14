from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        cv2.imshow(heatmapNumpy, cv2.COLORMAP_JET)


if (__name__ == "__main__"):
    main()
