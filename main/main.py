import cv2
import os
import numpy as np

images = []
folder = '/home/bluewaffle/hii/test2/another_test'
for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, filename))
    if img is not None:
        height, width, _ = img.shape
        max_dimension = 500
        scaling_factor = max_dimension / max(height, width)
        new_height, new_width = int(height * scaling_factor), int(width * scaling_factor)
        img = cv2.resize(img, (new_width, new_height))
        img_with_black_borders = np.zeros((max_dimension, max_dimension, 3), dtype=np.uint8)
        x_offset = (max_dimension - new_width) // 2
        y_offset = (max_dimension - new_height) // 2
        img_with_black_borders[y_offset:y_offset + new_height, x_offset:x_offset + new_width, :] = img
        images.append(img_with_black_borders)

fourcc = cv2.VideoWriter_fourcc(*"MJPG")
fps = 25  # Increased the fps to 60
video = cv2.VideoWriter("slideshow.avi", fourcc, fps, (max_dimension, max_dimension))

display_duration = fps * 5  # 5 seconds
transition_duration = fps * 3  # 3 seconds
for i in range(len(images)):
    for j in range(display_duration):
        video.write(images[i])
    for j in range(transition_duration):
        t = j / transition_duration
        img = (1 - t) * images[i].astype(float) + t * images[(i + 1) % len(images)].astype(float)
        video.write(np.uint8(img))

video.release()
cv2.destroyAllWindows()
