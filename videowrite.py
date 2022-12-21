import cv2
from api import rtspStream

cap = rtspStream()
# Get image width and height
image_width, image_height = int(cap.get(3)), int(cap.get(4))

# Video Write
out = cv2.VideoWriter(f"./WSP_raw_video_2.mp4",
                      cv2.VideoWriter_fourcc(*'mp4v'), 30,
                      (image_width, image_height))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    out.write(frame)

