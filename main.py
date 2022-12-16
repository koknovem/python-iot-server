import datetime
import time

from api import *
import numpy as np
import copy
import cv2
import matplotlib.pyplot as plt
import time
import logging
import os
import sys
sys.path.insert(1, './yolov7')

from models.experimental import attempt_load
from utils.datasets import letterbox

import torch
from torchvision import transforms

from bytetrack.mc_bytetrack import MultiClassByteTrack


def load_yolov7_model(ckpt_path="./best.pt", class_conf=0.3, iou=0.50):
    model_path = os.getcwd() + '/yolov7'
    device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

    model = torch.hub.load(
        model_path,
        'custom',
        path_or_model=ckpt_path,
        source='local',
        force_reload=True)

    model.conf = class_conf
    model.iou = iou
    model.classes = None
    model.multi_label = False
    model.max_det = 1000

    return model


def set_color(index):
    temp_index = abs(int(index)) * 3
    color = ((37 * temp_index) % 255, (17 * temp_index) % 255,
             (29 * temp_index) % 255)
    return color


def draw_bboxes(img, tracker_ids, bboxes, scores, class_ids, track_id_dict, class_names):
    for tracker_id, bbox, score, class_id in zip(tracker_ids, bboxes, scores, track_id_dict):
        # bbox
        xmin, ymin, xmax, ymax = bbox

        # Color
        color = set_color(int(track_id_dict[tracker_id]))

        # Draw Bounding boxes
        c1, c2 = (int(xmin), int(ymin)), (int(xmax), int(ymax))
        cv2.rectangle(img, c1, c2, color, 2)

        # Put Text
        # line thickness
        tl = 1.5

        # font thickness
        tf = max(tl - 1, 1)

        # Text to be put
        text = str(track_id_dict[tracker_id])

        # Find text size
        t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tf)[0]

        # Bounding box coordination for text
        c3 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

        # Put bounding boxes for text and put text
        cv2.rectangle(img, c1, c3, color, -1)
        cv2.putText(img, text, (c1[0], c1[1] - 2), 0, tl / 3, [0, 0, 255], thickness=tf)

        # Put count of people
        num_of_ppls = str(len(track_id_dict))
        cv2.putText(img, num_of_ppls, (10, 30), 1, 0.8, [0, 255, 0], thickness=tf)

    return img


def main():
    # print(setLightLevel(group=31, level=20))

    # vvvvvvvvv show heatmap vvvvvvvvv #

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

    # ^^^^^^^ show heatmap ^^^^^^^^ #
    # RTSP streaming
    cap = rtspStream()
    cap_fps = cap.get(cv2.CAP_PROP_FPS)

    model = load_yolov7_model('./yolov7/yolov7.pt')

    # Check whether path is ok
    assert cap.isOpened != True, 'Please check the path again'

    # Get image width and height
    image_width, image_height = int(cap.get(3)), int(cap.get(4))

    # Video Write
    out = cv2.VideoWriter(f"./WSP_video_processed.mp4",
                          cv2.VideoWriter_fourcc(*'mp4v'), 30,
                          (image_width, image_height))

    # Initialize ByteTracker parameters
    tracker = MultiClassByteTrack(
        fps= cap_fps,
        track_thresh = 0.5,#0.5
        track_buffer = 120, #30
        match_thresh = 0.8, # 0.8
        min_box_area = 10,
        mot20 = None,
    )

    # Save track ID
    track_id_dict = {}

    while cap.isOpened():
        ret, img = cap.read()

        if not ret:
            break

        img_copy = copy.deepcopy(img)

        # Predictions
        results = model(img, augment = False)

        # Extract the result
        preds = results.pandas().xyxy[0]
        preds = preds[preds['class']==0]

        # Separate all values into different categories
        bboxes = preds[['xmin', 'ymin', 'xmax', 'ymax']].values
        scores = preds[['confidence']].values.flatten()
        class_ids = preds[['class']].values.flatten()
        class_names = preds[['name']].values.flatten()

        # Multi-object tracking
        t_ids, t_bboxes, t_scores, t_class_ids = tracker(
            img,
            bboxes,
            scores,
            class_ids,
        )

        # check whether object exists
        for tracker_id, bbox in zip(t_ids, bboxes):
            if tracker_id not in track_id_dict:
                new_id = len(track_id_dict)
                track_id_dict[tracker_id] = new_id

        # Draw bboxes and extract videos
        img_bboxes = draw_bboxes(
            img_copy,
            t_ids,
            t_bboxes,
            t_scores,
            t_class_ids,
            track_id_dict,
            class_names
        )
        out.write(img_bboxes)

    return None


if __name__ == "__main__":
    main()
