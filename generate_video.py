from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
# from moviepy.video.fx.all import resize, zoom_in, crossfadein
from moviepy.video.fx.all import resize, crop, speedx
import PIL
from PIL import Image
import os
import random
from pkg_resources import parse_version
import numpy as np
import textwrap

if parse_version(Image.__version__)>=parse_version('10.0.0'):
    Image.ANTIALIAS=Image.LANCZOS

def jitter_position(t):
    interval = 3  # every 3 seconds
    if int(t) % interval == 0:
        dx = int(np.random.uniform(-10, 10))
        dy = int(np.random.uniform(-5, 5))
    else:
        dx = 0
        dy = 0
    return ('center', 5 + dy)

def get_random_brainrot_clip():
    all_files = os.listdir("./brainrot")

    return "./brainrot/" + random.choice(all_files)
    # return "./brainrot/subway_surfer.mp4"

def create_wrapped_text_clip(text, start, end, max_chars=40):
    wrapped_text = textwrap.fill(text, width=max_chars)
    text_clip = TextClip(
        wrapped_text,
        fontsize=36,
        color="limegreen",
        font="Impact",
        stroke_color="black",
        stroke_width=2,
        method="label"
    )
    text_clip = text_clip.set_position(jitter_position).set_duration(end - start).set_start(start)
    return text_clip

def create_video_with_audio(image_path, audio_path, title, summary, subtitles=None):
    output_file = "video.mp4"

    # loading video
    audio_clip = AudioFileClip(audio_path)

    # loading imgs
    image_clip = ImageClip(image_path, duration=audio_clip.duration)

    # adding brainrot video and play it in the loop
    brainrot_video = get_random_brainrot_clip()
    second_video = VideoFileClip(brainrot_video).loop(duration=audio_clip.duration)

    # setting scenes for images
    scenes = [{"start": 0, "end": 5, "name": "random2.jpg"}, {"start": 5, "end": audio_clip.duration, "name": "random3.jpg"}]

    scene_clips = []
    for scene in scenes:
        clip = ImageClip(scene["name"]).set_duration(scene["end"] - scene["start"])
        clip = clip.set_start(scene["start"])
        scene_clips.append(clip)

    for i in range(1, len(scene_clips)):
        scene_clips[i] = scene_clips[i].crossfadein(1)

    clip = clip.set_position(lambda t: ('center', int(100 + 10 * t)))

    if subtitles is None:
        splitted_summary = summary.split()
        summary_length = len(splitted_summary)
        video_duration = audio_clip.duration

        # 5 words per subtitle frame
        words_per_frame = 7

        # calculating number of frames
        num_of_frames = (summary_length // words_per_frame) + (1 if summary_length % words_per_frame != 0 else 0)

        # calculating duration for each frame
        frame_duration = video_duration / num_of_frames

        # adding title first
        # subtitles = [{"start": 0, "end": 3, "text": title}]
        subtitles = []

        start_time = 0
        for i in range(num_of_frames):
            end_time = start_time + frame_duration
            start_index = i * words_per_frame
            end_index = start_index + words_per_frame
            subtitle_text = " ".join(splitted_summary[start_index:end_index])

            subtitles.append({"start": start_time, "end": end_time, "text": subtitle_text})

            start_time = end_time

    subtitle_clips = []
    for subtitle in subtitles:
        # text_clip = TextClip(subtitle["text"], fontsize=36, color="limegreen", font="Impact", stroke_color="black", stroke_width=1, method="label", size=final_resolution)
        # text_clip = text_clip.set_position(jitter_position).set_duration(subtitle["end"] - subtitle["start"]).set_start(subtitle["start"])

        # text_clip = TextClip(subtitle["text"], fontsize=18, color="white", bg_color=None, size=final_resolution, font="Arial-Bold")
        # text_clip = text_clip.set_position(("center")).set_duration(subtitle["end"] - subtitle["start"]).set_start(subtitle["start"])
        text_clip = create_wrapped_text_clip(subtitle["text"], subtitle["start"], subtitle["end"])
        subtitle_clips.append(text_clip)

    # combining audio and video
    # video = CompositeVideoClip([image_clip] + subtitle_clips)
    video = CompositeVideoClip(scene_clips + subtitle_clips)
    video = video.set_audio(audio_clip)

    # final video
    # video.write_videofile(output_file, fps=24)

    # video = video.resize(width=640, height=720).set_position(("left", "center"))
    # second_video = second_video.resize(width=640, height=720).set_position(("right", "center"))

    video = video.resize(width=1280, height=360).set_position(("center", "top"))
    # video = video.fx(lambda clip: clip.resize(lambda t: 1 + 0.02 * (t % 0.5)))

    second_video = second_video.resize(width=1280, height=360).set_position(("center", "bottom"))

    # emoji = TextClip("🔥", fontsize=8, color="red").set_position(("right", "top")).set_duration(1).set_start(3)
    # final_video = CompositeVideoClip([video, second_video, emoji], size=(1280, 720))

    final_video = CompositeVideoClip([video, second_video], size=(1280, 720))

    # final_video = CompositeVideoClip([video, second_video], size=(1280, 720))
    final_video = final_video.set_audio(audio_clip)

    final_video.write_videofile("video.mp4", fps=24)

    print("Audio duration:", audio_clip.duration)
    print("Image size:", image_clip.size)
    print("Creating video at:", output_file)

def validate_img(img_file):
    try:
        img = Image.open(img_file)
        img.verify()

        return True
    except Exception as e:
        print("Image is invalid:", e)
        return False