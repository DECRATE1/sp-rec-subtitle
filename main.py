import os
import sys
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper

# Проверка аргументов
if len(sys.argv) < 3:
    print("Usage: python main_no_ffmpeg.py <video_path> <curr_dir>")
    sys.exit(1)

video_path = os.path.abspath(sys.argv[1])
curr_dir = os.path.abspath(sys.argv[2])
os.makedirs(curr_dir, exist_ok=True)

# Извлечение аудио
def extract_audio(video_path, audio_fname="extracted_audio.wav"):
    audio_full_path = os.path.join(curr_dir, audio_fname)
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_full_path, logger=None)
    video.close()
    return audio_full_path

# Транскрипция через Whisper
def transcribe_audio(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, fp16=False, task="transcribe")
    return result

# Форматирование времени для SRT
def format_time(t: float) -> str:
    hours = int(t // 3600)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)
    milliseconds = int((t - int(t)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Сохранение SRT
def save_srt(result, srt_fname="subtitles.srt"):
    srt_full_path = os.path.join(curr_dir, srt_fname)
    with open(srt_full_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result.get("segments", []), start=1):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    return srt_full_path

# Создание текстовых клипов
def create_text_clips_from_segments(
    segments, video_w, video_h,
    font_size=32, color="white",
    stroke_color="black", stroke_width=2,
    pos=("center","bottom")
):
    txt_clips = []
    for seg in segments:
        txt = seg["text"].strip()
        start = seg["start"]
        end = seg["end"]
        duration = max(0.01, end - start)

        txt_clip = (
            TextClip(
                font="D:/Projects/sp-backend/zrniccyr_normal.ttf",  # путь к TTF
                text=txt,
                font_size=font_size,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                method="caption",
                size=(int(video_w*0.9), None),
                duration=duration,

                
            ).with_start(start)
        )

        txt_clips.append(txt_clip)
    return txt_clips

# Наложение субтитров
def burn_subtitles_with_moviepy(video_path, segments, output_path):
    video = VideoFileClip(video_path)
    w, h = video.size
    txt_clips = create_text_clips_from_segments(segments, w, h)
    final = CompositeVideoClip([video, *txt_clips])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, logger=None)
    video.close()
    final.close()

# Основной процесс
def process_video(video_path, output_path="output.mp4"):
    audio_path = extract_audio(video_path)
    result = transcribe_audio(audio_path)
    srt_path = save_srt(result)
    segments = result.get("segments", [])
    if not segments:
        raise RuntimeError("No segments from Whisper transcription")
    burn_subtitles_with_moviepy(video_path, segments, output_path)
    print(output_file)

if __name__ == "__main__":
    output_file = os.path.join(curr_dir, "output_noffmpeg.mp4")
    try:
        process_video(video_path, output_file)
    except Exception as e:
        print("Error:", str(e))
        raise
