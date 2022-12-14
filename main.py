import datetime
import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        multiplier = 4
        heatmapImage, heatmapResolution = getHeatmapHeatmapImage()
        heatmapImage = cv2.resize(heatmapImage, (heatmapResolution[1]*multiplier, heatmapResolution[0]*multiplier), interpolation=cv2.INTER_CUBIC)
        # plt.imshow(heatmapImage)
        # plt.title(datetime.datetime.now().strftime("%H:%M:%S"))
        # plt.show()

        cv2.imshow("heatmap", heatmapImage)
        cv2.waitKey(10)


if (__name__ == "__main__"):
    main()
