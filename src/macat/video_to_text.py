
import os
from moviepy.editor import VideoFileClip

POSSIBLE_EXTENSIONS = ["avi", "mp4", "mov"]
def remove_audio(video_path):
    # Check if the input file has a valid extension
    if not any(video_path.lower().endswith(ext) for ext in POSSIBLE_EXTENSIONS):
        raise ValueError(f"Unsupported file extension. Supported extensions are: {', '.join(POSSIBLE_EXTENSIONS)}")

    # Load the video file
    video = VideoFileClip(video_path)
    
    # Remove the audio
    video_without_audio = video.without_audio()

    # Create the 'results' directory if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Create the output video file path
    base_name = os.path.basename(video_path)
    name, ext = os.path.splitext(base_name)
    output_video_path = os.path.join(results_dir, f"{name}_no_audio{ext}")
    
    # Save the result
    video_without_audio.write_videofile(output_video_path, codec="libx264")

    # Extract audio and save to a constant name
    audio_output_path = os.path.join(results_dir, "extracted_audio_from_video.mp3")
    video.audio.write_audiofile(audio_output_path)

    return audio_output_path



