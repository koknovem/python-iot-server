import time

from api import *
import matplotlib.pyplot as plt
import cv2


def main():
    while True:
        heatmapNumpy = getHeatmapNumpy()
        heatmapshow = None
        heatmapshow = cv2.normalize(heatmapNumpy, heatmapshow, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        heatmapshow = cv2.applyColorMap(heatmapshow, cv2.COLORMAP_JET)
        cv2.imshow("heatmap", heatmapshow)
        time.sleep(1)


if (__name__ == "__main__"):
    main()
