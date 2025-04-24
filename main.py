import os
import requests

from wiki_article import get_random_wikipedia_article
from tts import generate_voice_over
from generate_video import create_video_with_audio, validate_img

import moviepy.config as mpc

mpc.change_settings({
    'IMAGEMAGICK_BINARY': r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
})

if __name__ == "__main__":
    article = get_random_wikipedia_article()

    if article:
        print("Summary:", article["summary"])
        print("URL:", article["url"])

        generate_voice_over(article["title"] ,article["summary"])

        if article["images"]:
            # header to make wikipedia fall in love with me
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) pyvideo-bot/1.0"
            }

            # selecting img
            image_path = article["images"][0]

            # getting response
            response = requests.get(image_path, headers=headers)

            # if response OK
            if response.status_code == 200:
                img_data = response.content

                # deleting previous file
                if os.path.exists("article_image.jpeg"):
                    os.remove("article_image.jpeg")

                # saving img
                with open("article_image.jpeg", "wb") as handler:
                    handler.write(img_data)

                print("Image downloaded and saved as 'article_image.jpeg'")
            else:
                print(f"Failed to download image: {response.status_code}")

            # print("Audio exists:", os.path.exists("test.wav"), "Size:", os.path.getsize("test.wav"))
            print("Audio exists:", os.path.exists("test.mp3"), "Size:", os.path.getsize("test.mp3"))

            if validate_img("article_image.jpeg"):
                create_video_with_audio("article_image.jpeg", "test.mp3", article["title"], article["summary"])
                # create_video_with_audio("article_image.jpeg", "test.wav", article["title"])
            else:
                create_video_with_audio("random.jpeg", "test.mp3", article["title"], article["summary"])
                # create_video_with_audio("random.jpeg", "test.wav", article["title"])
        else:
            print("no images found in the article")