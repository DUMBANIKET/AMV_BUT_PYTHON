from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load the videos
clip1 = VideoFileClip("fadeoutput1.mp4")
clip2 = VideoFileClip("zoomoutput2.mp4")

# Concatenate the videos
final_clip = concatenate_videoclips([clip1, clip2])

# Write the result to a file
final_clip.write_videofile("outputfinal.mp4")