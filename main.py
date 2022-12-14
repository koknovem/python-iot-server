import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapImage = getHeatmapHeatmapImage()
        heatmapImage = cv2.resize(heatmapImage,(500,500) ,interpolation=cv2.INTER_CUBIC)
        cv2.imshow("heatmap", heatmapImage)
        cv2.waitKey(1)


if (__name__ == "__main__"):
    main()
