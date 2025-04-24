from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx.all import resize
from PIL import Image

def create_video_with_audio(image_path, audio_path, title):
    output_file = "video.mp4"

    # loading video
    audio_clip = AudioFileClip(audio_path)

    # loading imgs
    image_clip = ImageClip(image_path, duration=audio_clip.duration)
    # image_clip = resize(image_clip, height=720)

    # text overlay
    # text = TextClip(title, fontsize=48, color="white", bg_color="black", size=image_clip.size)
    # text = text.set_position(("center", "bottom")).set_duration(audio_clip.duration)

    # combining audio and video
    # video = CompositeVideoClip([image_clip, text])
    video = CompositeVideoClip([image_clip])
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