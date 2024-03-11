import cv2
import numpy as np
from moviepy.editor import VideoFileClip

def apply_motion_blur(frame1, frame2):
    # Convert the frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate the optical flow between the two frames
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Calculate the magnitude and angle of the 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # Normalize the magnitude
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Create a mask image with the magnitude as the intensity and the angle as the hue
    mask = np.zeros((frame1.shape[0], frame1.shape[1], 3), dtype=np.uint8)
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 1] = 255
    mask[..., 2] = magnitude

    # Convert the mask image from HSV to BGR
    mask = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

    # Blur the mask image
    mask = cv2.GaussianBlur(mask, (35, 35), 0)

    # Blend the original frame with the mask image
    frame = cv2.addWeighted(frame1, 0.8, mask, 0.2, 0)

    return frame

# Load the video
clip = VideoFileClip("output2.mp4")

# Apply the motion blur
blurred_clip = clip.fl(lambda gf, t: apply_motion_blur(gf(t-1/clip.fps), gf(t)) if t > 0 else gf(t))

# Write the result to a file
blurred_clip.write_videofile("blurred_output.mp4")