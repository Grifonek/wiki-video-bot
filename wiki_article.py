import wikipedia

def get_random_wikipedia_article():
    # getting a random title
    title = wikipedia.random(1)
    print(f"selected article: {title}")

    # getting full article content
    try:
        page = wikipedia.page(title)
        summary = wikipedia.summary(title, sentences = 5)

        return {
            "title": page.title,
            "summary": summary,
            "content": page.content,
            "images": page.images,
            "url": page.url
        }
    
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"disambiguation page, skipping: {title}")
        return get_random_wikipedia_article()

    except Exception as e:
        print(f"failed to fetch article: {e}")
        return None