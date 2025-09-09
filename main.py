from moviepy import (
    ImageClip, 
    TextClip, 
    CompositeVideoClip, 
    AudioFileClip,
    concatenate_videoclips,
    VideoFileClip
)
import speech_recognition as sr

def clip_video(path, duration):
    video = VideoFileClip(path)
    video_duration = video.duration
    start_time = 0
    end_time = duration

    parts = []
    while end_time <= video_duration:
        part = video.subclipped(start_time, end_time)
        parts.append(part)

        start_time += duration
        end_time += duration

    return parts


video_path = "asset/video_test.mp4"
duration = 5

video_parts = clip_video(video_path, duration)
r = sr.Recognizer()
def create_voice():
    full_text = []
    for i, part in enumerate(video_parts):
        video = part
        audio_file = video.audio
        audio_file.write_audiofile(f"asset/{i + 1}.wav")

        with sr.AudioFile(f"asset/{i + 1}.wav") as source: 
            data = r.record(source)
            text = r.recognize_vosk(data, language='ru')
            
            full_text.append(text)
    return full_text






print(create_voice())

