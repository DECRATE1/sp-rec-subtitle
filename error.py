# ---
# почему оно не работает я без понятия, может у тебя получиться сделать как надо
# либо же осталяем тот вариант, можно попробовать как-то сделать и щрифты и цвет и задний фон. Если получится то кайф
# --- 

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

video = VideoFileClip("video_test.mp4")

subs = []
for seg in result["segments"]:
    start = seg["start"]
    end = seg["end"]
    txt = seg["text"].strip()

    subtitle = (TextClip(txt, size=(video.w, 50), color="white", bg_color="black", method="caption")
                .set_position(("center", "bottom"))
                .set_start(start)
                .set_duration(end - start))
    subs.append(subtitle)

final = CompositeVideoClip([video, *subs])
final.write_videofile("video_with_subs.mp4", codec="libx264", audio_codec="aac")
