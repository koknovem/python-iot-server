from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        cv2.imshow("heatmap", heatmapNumpy)


if (__name__ == "__main__"):
    main()
