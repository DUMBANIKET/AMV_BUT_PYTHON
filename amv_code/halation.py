import cv2
import numpy as np
from PIL import Image, ImageFilter

# Open the video
cap = cv2.VideoCapture('output2.mp4')

# Get the video's width, height, and frames per second
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create a VideoWriter object to write the output video
out = cv2.VideoWriter('halationoutput2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the frame to isolate the bright areas
    _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Convert the threshold frame to a PIL Image
    threshold = Image.fromarray(threshold)

    # Apply a blur filter to the threshold frame to create the glow effect
    glow = threshold.filter(ImageFilter.GaussianBlur(radius=5))

    # Convert the glow frame back to a numpy array
    glow = np.array(glow)

    # Convert the glow image to a three channel image
    glow = cv2.cvtColor(glow, cv2.COLOR_GRAY2BGR)

    # Create the halation effect by adding the glow to the original frame
    halation = cv2.addWeighted(frame, 1, glow, 0.5, 0)

    # Write the frame to the output video
    out.write(halation)

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()