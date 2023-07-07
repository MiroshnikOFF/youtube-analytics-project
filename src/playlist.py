from src.channel import Channel
from datetime import timedelta


class PlayList:

    # Объект для работы с YouTube API
    youtube = Channel.get_service()

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"

        self.__videos = PlayList.youtube.playlistItems().list(playlistId=self.pl_id,
                                                              part='contentDetails',
                                                              maxResults=50,).execute()
        self.__random_video_id = self.__videos['items'][0]['contentDetails']['videoId']
        self.__random_video = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=self.__random_video_id).execute()
        self.__channel_id = self.__random_video['items'][0]['snippet']['channelId']
        self.__playlists = Channel.youtube.playlists().list(channelId=self.__channel_id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,).execute()
        for pl in self.__playlists['items']:
            if pl['id'] == self.pl_id:
                self.title = pl['snippet']['title']
        self.__video_ids = [video['contentDetails']['videoId'] for video in self.__videos['items']]

    @property
    def total_duration(self):
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(self.__video_ids)
                                                        ).execute()
        total_duration = timedelta()

        for video in video_response['items']:
            duration = video['contentDetails']['duration']
            dur_list = duration.replace("PT", '').strip("S").split("M")
            if dur_list[0].isdigit():
                minutes = int(dur_list[0])
            else:
                minutes = 0
            if dur_list[1].isdigit():
                seconds = int(dur_list[1])
            else:
                seconds = 0
            time_obj = timedelta(minutes=minutes, seconds=seconds)
            total_duration += time_obj
        return total_duration

    def show_best_video(self):
        videos_like_url_list = []
        for video_id in self.__video_ids:
            items_index = 0
            video_response = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=video_id).execute()
            like = int(video_response['items'][items_index]['statistics']['likeCount'])
            url = f"https://youtu.be/{video_response['items'][items_index]['id']}"
            video_like_url = {'like': like, 'url': url}
            videos_like_url_list.append(video_like_url)
            items_index += 1
        best_video = {'like': 0}
        for video in videos_like_url_list:
            if video['like'] > best_video['like']:
                best_video['like'] = video['like']
                best_video['url'] = video['url']
        return best_video['url']

