import moviepy
import whisper
import ffmpeg
import subprocess

# ---
# вытащили звук из видоса
# ---

def ExtractAudio(video_path):
    video = moviepy.VideoFileClip(video_path)
    audio = video.audio
    duration =  audio.duration
    fps = audio.fps
    audio.write_audiofile("extracted_audio.mp3", fps=fps)
    print(f'Audio extracted: duration={duration}, fps={fps}')
    return duration, fps

if __name__ == "__main__":
    video_path = "video_test.mp4"
    duration, fps = ExtractAudio(video_path)
    print(f'Audio extracted with duration: {duration} second and {fps}') 

# ---
# теперь как-то с помощью OpenAIs Whisper делаем транскрибацию
# ---

# загружаем модель
model = whisper.load_model("medium")
# загружаем аудио
audio = whisper.load_audio("/home/sergey/sp-rec-subtitle/extracted_audio.mp3")
# делаем спекторграмму
mel = whisper.log_mel_spectrogram(audio).to(model.device)
# вывводи резкльтат
result = model.transcribe("extracted_audio.mp3")
result_srt = model.transcribe("extracted_audio.mp3", verbose=True, fp16=False, task="transcribe")

# ---
# записываем в файлм тайм-коды и субтиртры
# и накладываем на видео
# ---

def format_time(t: float) -> str:
    hours = int(t // 3600)          
    minutes = int((t % 3600) // 60)       
    seconds = int(t % 60)               
    milliseconds = int((t - int(t)) * 1000) 
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

with open("subtitles.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], start=1):
        start = format_time(seg["start"])   
        end = format_time(seg["end"])       
        text = seg["text"].strip()           

        f.write(f"{i}\n")                   
        f.write(f"{start} --> {end}\n")     
        f.write(f"{text}\n\n")              

def burn_subtitles(video_path, srt_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",   # аудио копируем без перекодирования
        output_path
    ]
    subprocess.run(cmd, check=True)

# пример использования
burn_subtitles("video_test.mp4", "subtitles.srt", "output.mp4")