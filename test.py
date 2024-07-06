from src.macat.transcriber import Transcriber
from src.macat.video_to_text import remove_audio

url = r"uploads\test_audio.mp3"

transcriber = Transcriber()

#text = transcriber.transcribe(url)



# Example usage
#video_path = r"uploads\test_video.mp4"
#audio_output_path = remove_audio(video_path)

#print(f"Audio saved to: {audio_output_path}")


path = r"static\uploads\audio.wav"
text = transcriber.transcribe_file(path,"audio")
print(text)





