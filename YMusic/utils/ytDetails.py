import aiohttp
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
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://dab.yeet.su/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            f"{API_URL}/search?q={query.replace(' ', '+')}&offset=0&type=track"
        ) as response:
            data = await response.json()
            print(data)
            if "tracks" in data and len(data["tracks"]) > 0:
                first_result = data["tracks"][0]
                track_id = first_result["id"]
                async with session.get(
                    f"{API_URL}/stream?trackId={track_id}"
                ) as dl_response:
                    dl_data = await dl_response.json()
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
