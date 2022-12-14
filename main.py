import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    # print(getHeatmapNumpy())
    while True:
        multiplier = 4
        heatmapImage, heatmapResolution = getHeatmapHeatmapImage()
        heatmapImage = cv2.resize(heatmapImage, (heatmapResolution[0]*multiplier, heatmapResolution[0]*multiplier), interpolation=cv2.INTER_CUBIC)
        plt.imshow(heatmapImage)
        plt.show()
        # cv2.imshow("heatmap", heatmapImage)
        # cv2.waitKey(1)


if (__name__ == "__main__"):
    main()
