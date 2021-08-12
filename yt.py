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
            [i['snippet']['title'],  # titulo do video [0]
            i['snippet']['description'],  # descricao do video [1]
            i['snippet']['publishedAt'][:10],  # data YYYY-mm-dd [2]
            i['snippet']['videoOwnerChannelTitle'],  # nome do canal dono do video [3]
            i['snippet']['resourceId']['videoId'],  # ID do video [4]
            i['snippet']['channelTitle'],  # nome do canal dono da playlist [5]
            i['snippet']['playlistId']]  # Id da playlist [6]
            )
    
    return data

# ytube = get_videos('PLR8JXremim5DINkBLBDDhjVah5kWKFWxk')
# print(ytube[0][4])