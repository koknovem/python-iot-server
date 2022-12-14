import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        cv2.imshow("heatmap", getHeatmapHeatmapImage())
        cv2.waitKey(30)


if (__name__ == "__main__"):
    main()
