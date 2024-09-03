import subprocess

def extract_audio(input_video_path, output_audio_path):
    # Command to extract audio using ffmpeg
    command = ['ffmpeg', '-i', input_video_path, '-q:a', '0', '-map', 'a', output_audio_path]
    
    try:
        # Run the command
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully. Output saved as {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Ensure that ffmpeg is installed and the input file path is correct.")

# Example usage
input_video = r'C:\Users\User\Desktop\Blessing_AI\MACAT\uploads\test_video.mp4'
output_audio = 'extracted_audio.mp3'
# Extract the audio
extract_audio(input_video, output_audio)

