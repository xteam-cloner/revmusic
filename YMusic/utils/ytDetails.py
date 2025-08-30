import aiohttp
from pytubefix import Search, YouTube as pyYouTube, Playlist
from urllib.parse import urlparse, parse_qs

API_URL = "https://apis.davidcyriltech.my.id/"


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


async def search_api(query, is_videoId=False, video=False):
    query = str(query)
    async with aiohttp.ClientSession() as session:
        if is_videoId:
            async with session.get(
                f"{API_URL}download/ytmp4?url=https://youtube.com/watch?v={query}"
            ) as response:
                data = await response.json()
                print(data)
                if data["status"] == 200:
                    result = data["result"]
                    title = result["title"]
                    duration = "N/A"
                    link = result["download_url"]
                    return title, duration, link
        else:
            async with session.get(
                f"{API_URL}search/spotify?text={query}", ssl=False
            ) as response:
                data = await response.json()
                print(data)
                if data.get("success") and len(data.get("result", [])) > 0:
                    first_result = data["result"][0]
                    spotify_url = first_result["externalUrl"]
                    async with session.get(
                        f"{API_URL}spotifydl?url={spotify_url}"
                    ) as dl_response:
                        dl_data = await dl_response.json()
                        print(dl_data)
                        if dl_data.get("success") and dl_data.get("status") == 200:
                            title = dl_data["title"]
                            duration = dl_data.get("duration", "N/A")
                            link = dl_data["DownloadLink"]
                            return title, duration, link
                else:
                    async with session.get(
                        f"{API_URL}youtube/search?query={query.replace(' ', '+')}"
                    ) as response:
                        data = await response.json()
                        print(data)
                        if data.get("status") and len(data.get("results", [])) > 0:
                            first_result = data["results"][0]
                            video_url = first_result["url"]
                            async with session.get(
                                f"{API_URL}download/ytmp3?url={video_url}"
                            ) as dl_response:
                                dl_data = await dl_response.json()
                                print(dl_data)
                                if dl_data.get("success") and dl_data.get("status") == 200:
                                    result = dl_data["result"]
                                    title = result["title"]
                                    duration = first_result.get("duration", "N/A")
                                    link = result["download_url"]
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
