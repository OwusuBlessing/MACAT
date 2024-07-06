import assemblyai as aai
import os
from dotenv import load_dotenv
from queue import Queue
import os
from moviepy.editor import VideoFileClip
load_dotenv()

#set api key
aai_api = os.getenv("ASSEMBLY_AI_API")
aai.settings.api_key = aai_api


class Transcriber():
    POSSIBLE_VIDEO_EXTENSIONS = ["avi", "mp4", "mov"]

    def __init__(self, speak_identifier=False):
        self.speak_identifiers = speak_identifier

    def __transcribe_audio(self, path):
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(path)
        if transcript.error:
            return None
        else:
            return transcript.text

    def transcribe_file(self, path, file_type):
        if file_type == "audio":
            try:
                text = self.__transcribe_audio(path)
                if text:
                    return {"status": "success", "text": text}
                else:
                    return {"status": "success", "text": None}
            except Exception as e:
                return {"status": "error"}
        elif file_type == "video":
            extracted_audio_path = self.remove_audio(path)
            return self.__transcribe_audio(extracted_audio_path)
        else:
            return None

    def remove_audio(self, video_path):
        # Check if the input file has a valid extension
        if not any(video_path.lower().endswith(ext) for ext in self.POSSIBLE_VIDEO_EXTENSIONS):
            raise ValueError(f"Unsupported file extension. Supported extensions are: {', '.join(self.POSSIBLE_VIDEO_EXTENSIONS)}")

        # Load the video file
        video = VideoFileClip(video_path)

        # Remove the audio
        video_without_audio = video.without_audio()

        # Create the 'results' directory if it doesn't exist
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

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
        

