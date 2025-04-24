from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
# from moviepy.video.fx.all import resize, zoom_in
from PIL import Image

def create_video_with_audio(image_path, audio_path, title, summary, subtitles=None):
    output_file = "video.mp4"

    # loading video
    audio_clip = AudioFileClip(audio_path)

    # loading imgs
    image_clip = ImageClip(image_path, duration=audio_clip.duration)
    # image_clip = resize(image_clip, height=720)
    # image_clip = zoom_in(image_clip, 1.1)

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
        subtitles = [{"start": 0, "end": 3, "text": title}]

        start_time = 3
        for i in range(num_of_frames):
            end_time = start_time + frame_duration
            start_index = i * words_per_frame
            end_index = start_index + words_per_frame
            subtitle_text = " ".join(splitted_summary[start_index:end_index])

            subtitles.append({"start": start_time, "end": end_time, "text": subtitle_text})

            start_time = end_time

    subtitle_clips = []
    for subtitle in subtitles:
        text_clip = TextClip(subtitle["text"], fontsize=18, color="white", bg_color="black", size=image_clip.size, font="Arial-Bold")
        text_clip = text_clip.set_position(("center", "bottom")).set_duration(subtitle["end"] - subtitle["start"]).set_start(subtitle["start"])
        subtitle_clips.append(text_clip)

    # combining audio and video
    video = CompositeVideoClip([image_clip] + subtitle_clips)
    video = video.set_audio(audio_clip)

    # final video
    video.write_videofile(output_file, fps=24)

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