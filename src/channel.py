import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    YT_API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet, statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    # @channel_id.setter
    # def channel_id(self, new_name):
    #     self.__channel_id = new_name

    @property
    def title(self):
        return self.__channel["items"][0]["snippet"]['title']

    @property
    def description(self):
        return self.__channel["items"][0]["snippet"]['description']

    @property
    def subscriberCount(self):
        return self.__channel["items"][0]["statistics"]['subscriberCount']

    @property
    def video_count(self):
        return self.__channel["items"][0]["statistics"]['videoCount']

    @property
    def viewCount(self):
        return self.__channel["items"][0]["statistics"]['viewCount']

    @property
    def url(self):
        return f"https://www.youtube.com/{self.__channel['items'][0]['snippet']['customUrl']}"

    @classmethod
    def get_service(cls):
        return Channel.youtube

    def to_json(self, file_name):
        moscowpython = {
           "channel_id": self.channel_id,
           "title": self.title,
           "description": self.description,
           "subscriberCount": self.subscriberCount,
           "video_count": self.video_count,
           "viewCount": self.viewCount,
        }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(str(moscowpython), file, ensure_ascii=False)









