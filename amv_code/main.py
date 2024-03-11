#This dumb idiot contains the zoom in to normal - normal to zoom in effect i know this is a piece of garbage


from moviepy.editor import VideoFileClip
import numpy as np
import cv2

# Load the video
clip = VideoFileClip("solo2.mp4")

# Start and end frames for the zoom effect
start_frame = 5
end_frame = clip.duration * clip.fps - 5

# Maximum zoom factor
max_zoom_factor = 3

# Function to apply the zoom effect and motion blur
def zoom(get_frame, t):
    frame = get_frame(t)
    h, w = frame.shape[:2]
    frame_number = t * clip.fps

    if frame_number <= start_frame:
        zoom_factor = 1 + (start_frame - frame_number) / start_frame * (max_zoom_factor - 1)
    elif frame_number >= end_frame:
        zoom_factor = 1 + (frame_number - end_frame) / (clip.duration * clip.fps - end_frame) * (max_zoom_factor - 1)
    else:
        zoom_factor = 1

    frame = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)

    # Crop the frame to maintain the original size
    h_zoom, w_zoom = frame.shape[:2]
    y1 = int((h_zoom - h) / 2)
    y2 = y1 + h
    x1 = int((w_zoom - w) / 2)
    x2 = x1 + w

    frame = frame[y1:y2, x1:x2]

    # Apply motion blur
    size = int(5 * zoom_factor)  # Size of the kernel used for blurring
    size = size if size % 2 == 1 else size + 1  # Ensure size is odd
    frame = cv2.GaussianBlur(frame, (size, size), 0)

    return frame

# Apply the zoom effect and motion blur
zoomed_clip = clip.fl(zoom)

# Write the result to a file
zoomed_clip.write_videofile("zoomoutput2.mp4")