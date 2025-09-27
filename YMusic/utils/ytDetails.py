from curl_cffi.requests import AsyncSession
from pytubefix import Search, YouTube as pyYouTube, Playlist
from urllib.parse import urlparse, parse_qs

API_URL = "https://dab.yeet.su/api"


def searchYt(query, is_videoId=False):
    # raise Exception("This request was detected as a bot")
    query = str(query)
    if is_videoId:
        video = pyYouTube(f"https://www.youtube.com/watch?v={query}")
        title = video.title
        duration = video.length
        link = video.watch_url
        return title, duration, link
    else:
        videosResult = Search(query)
        for Result in videosResult.videos:
            title = Result.title
            duration = Result.length
            link = Result.watch_url
            return title, duration, link
    return None, None, None


async def search_api(query):
    query = str(query)

    async with AsyncSession() as session:
        response = await session.get(
            f"{API_URL}/search?q={query.replace(' ', '+')}&offset=0&type=track",
            impersonate="chrome"
        )
        data = response.json()
        print(data)
        if "tracks" in data and len(data["tracks"]) > 0:
            first_result = data["tracks"][0]
            track_id = first_result["id"]
            dl_response = await session.get(
                f"{API_URL}/stream?trackId={track_id}",
                impersonate="chrome"
            )
            dl_data = dl_response.json()
            print(dl_data)
            if "url" in dl_data:
                title = first_result["title"]
                duration = first_result.get("duration", "N/A")
                link = dl_data["url"]
                return title, duration, link

    return None, None, None


def searchPlaylist(query):
    query = str(query)
    playlistResult = Playlist(query)
    title = playlistResult.title
    duration = playlistResult.length
    return title, duration


def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get("list", [None])[0]
    return playlist_id


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path[1:]
    else:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
    return video_id
