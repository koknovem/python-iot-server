import datetime
import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    startTime = time.time()
    print(setLightLevel(level=50), time.time() - startTime)
    time.sleep(5)
    startTime = time.time()
    print(setLightLevel(level=20), time.time() - startTime)
    # while True:
    #     multiplier = 4
    #     heatmapImage, heatmapResolution = getHeatmapHeatmapImage()
    #     heatmapImage = cv2.resize(heatmapImage, (heatmapResolution[1]*multiplier, heatmapResolution[0]*multiplier), interpolation=cv2.INTER_CUBIC)
    #     # plt.imshow(heatmapImage)
    #     # plt.title(datetime.datetime.now().strftime("%H:%M:%S"))
    #     # plt.show()
    #
    #     cv2.imshow("heatmap", heatmapImage)
    #     cv2.waitKey(10)
    #     time.sleep(10)


if (__name__ == "__main__"):
    main()
