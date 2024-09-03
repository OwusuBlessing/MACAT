import assemblyai as aai
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

#set api key
aai_api = os.getenv("ASSEMBLY_AI_API")
aai.settings.api_key = aai_api

class Transcriber:
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
                return {"status": "error", "message": str(e)}
        elif file_type == "video":
            try:
                extracted_audio_path = self.extract_audio_with_ffmpeg(path)
                text = self.__transcribe_audio(extracted_audio_path)
                if text:
                    return {"status": "success", "text": text}
                else:
                    return {"status": "error", "message": "Failed to transcribe audio"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": "Unsupported file type"}

    def extract_audio_with_ffmpeg(self, video_path):
        # Check if the input file has a valid extension
        if not any(video_path.lower().endswith(ext) for ext in self.POSSIBLE_VIDEO_EXTENSIONS):
            raise ValueError(f"Unsupported file extension. Supported extensions are: {', '.join(self.POSSIBLE_VIDEO_EXTENSIONS)}")

        # Create the 'results' directory if it doesn't exist
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        # Extract audio using ffmpeg and save to a constant name
        audio_output_path = os.path.join(results_dir, "extracted_audio_from_video.mp3")
        command = ['ffmpeg', '-y', '-i', video_path, '-q:a', '0', '-map', 'a', audio_output_path]
        
        try:
            subprocess.run(command, check=True)
            print(f"Audio extracted successfully. Output saved as {audio_output_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract audio: {str(e)}")

        return audio_output_path
