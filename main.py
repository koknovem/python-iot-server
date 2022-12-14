import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        heatmapNumpy = np.kron(heatmapNumpy, np.ones((6)))
        for row in heatmapNumpy:
            print(row)
        grayImage = cv2.cvtColor(heatmapNumpy, cv2.COLOR_GRAY2BGR)
        cv2.imshow("heatmap", grayImage)
        time.sleep(1)


if (__name__ == "__main__"):
    main()
