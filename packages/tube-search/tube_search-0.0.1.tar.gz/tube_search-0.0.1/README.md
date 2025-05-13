# Tube Search - Youtube fast and practical search engine in Python

<img height="80" align="right" alt="Tube Search" src="https://i.ibb.co/wNbhxXtf/20250512-123905-0000.png"/>

> Tube Search is an asynchronous, constantly up-to-date and written python library, aiming to do research simply, practically and quickly on YouTube.

# Search for Video (1 Video)

```python
from asyncio import run
from tube_search import VideoSearch

async def main() -> None:
    video = await VideoSearch().video(
        query="Elektronomia",
        language="en-US",
        region="US"
    )
    print(video)
    print()
    print(video.videoTitle)

run(main())
```

# Output from search video (1 video)
```sh
$ TubeVideoInfo(videoID='TW9d8vYrVFQ', videoTitle='Elektronomia - Sky High | Progressive House | NCS - Copyright Free Music', videoDuration='3:58', publishedTime='8 years ago', videoViewCount=TubeViewsInfo(view_count='264,461,922 views', view_abbr_count='264M views'), thumbnails=[TubeThumbnailsInfo(url='https://i.ytimg.com/vi/TW9d8vYrVFQ/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDzHv6boRaBnEoZWSNFdZRGVdUmJw', width=480, height=270)], descriptionSnippet='#nocopyrightsounds #copyrightfree #music #song #edm #dancemusic #royaltyfreemusic #copyrightfreemusic #nocopyrightmusic\xa0...', channel=TubeChannelInfo(title='NoCopyrightSounds', id='UC_aEa8K-EOJ3D6gOs7HcyNg', thumbnails=[TubeThumbnailsInfo(url='https://yt3.ggpht.com/opGwWu2ScRBy-OA81LIzKwSatxlVKjjNyAdt4fWh4LoLzldx05Sdf3OGQz0Fz78ziZ9RLP4=s68-c-k-c0x00ffffff-no-rj', width=68, height=68)], url='https://www.youtube.com/channel/UC_aEa8K-EOJ3D6gOs7HcyNg'), accessibility=TubeAccessibilityInfo(title='Elektronomia - Sky High | Progressive House | NCS - Copyright Free Music 3 minutes, 58 seconds', duration='3 minutes, 58 seconds'), url='https://www.youtube.com/watch?v=TW9d8vYrVFQ', shelfTitle=None)

Elektronomia - Sky High | Progressive House | NCS - Copyright Free Music