from config import API_KEY
from googleapiclient.discovery import build # pip install google-api-python-client

def get_videos(playlistId):
    youtube= build('youtube', 'v3', developerKey=API_KEY)

    nextPage_token = None
    playlist_videos = []
    while True:
        res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults=50, pageToken=nextPage_token).execute()
        playlist_videos += res['items']
        nextPage_token = res.get('nestPageToken')
        if nextPage_token is None:
            break

    data = []
    for i in playlist_videos:
        data.append(
            [i['snippet']['title'],
            i['snippet']['description'], 
            i['snippet']['publishedAt'][:10],
            i['snippet']['videoOwnerChannelTitle'],
            i['snippet']['resourceId']['videoId'],
            i['snippet']['channelTitle'],
            i['snippet']['playlistId']]
            )
    
    return data

# ytube = get_videos('PLR8JXremim5DINkBLBDDhjVah5kWKFWxk')
# print(ytube)