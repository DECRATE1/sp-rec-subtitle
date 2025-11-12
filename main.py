import moviepy
import whisper
import ffmpeg
import subprocess
import pysubs2

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

# ---
# изначально хотел сразу записать в ass, но он тогда не применяет стили, пришлось сначало записывать в srt, а потом конвертировать в ass
# конвертируем файл srt в ass по другому просто не работет
# ---

subs = pysubs2.load("subtitles.srt", encoding="utf-8")
# меняем стиль
subs.styles["Default"].fontname = "Robot"
subs.styles["Default"].fontsize = 14
subs.styles["Default"].primarycolor = pysubs2.Color(255, 255, 255)  # белый текст
subs.styles["Default"].backcolor = pysubs2.Color(0, 0, 0, a=128)           # чёрный фон
subs.styles["Default"].borderstyle = 3                              # фон-бокс

subs.save("subtitles.ass")

# ---
# объединяем все вместе
# ---

def burn_ass_subtitles(input_video, ass_file, output_file):
    cmd = [
        "ffmpeg",
        "-i", input_video,
        "-vf", f"ass={ass_file}",
        "-c:a", "copy",
        output_file,
        "-y"
    ]
    subprocess.run(cmd, check=True)

burn_ass_subtitles("video_test.mp4", "subtitles.ass", "output.mp4")