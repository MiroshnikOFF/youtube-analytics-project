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
        self.title = self.__channel["items"][0]["snippet"]['title']
        self.description = self.__channel["items"][0]["snippet"]['description']
        self.subscriberCount = self.__channel["items"][0]["statistics"]['subscriberCount']
        self.video_count = self.__channel["items"][0]["statistics"]['videoCount']
        self.viewCount = self.__channel["items"][0]["statistics"]['viewCount']
        self.url = f"https://www.youtube.com/{self.__channel['items'][0]['snippet']['customUrl']}"

    def __str__(self):
        """Возвращает строку с названием и url канала"""
        return f"{self.title} ({self.url})"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self.__channel_id


    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return Channel.youtube

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
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

    def __add__(self, other):
        """Суммирует количество подписчиков двух каналов"""
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        """Вычитает количество подписчиков одного канала из количества подписчиков другого канала"""
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        """
        Сравнивает количество подписчиков двух каналов. Если в первом больше
        чем во втором, возвращает True, иначе False
        """
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        """
        Сравнивает количество подписчиков двух каналов. Если в первом больше либо равно
        чем во втором, возвращает True, иначе False
        """
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        """
        Сравнивает количество подписчиков двух каналов. Если в первом меньше
        чем во втором, возвращает True, иначе False
        """
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        """
        Сравнивает количество подписчиков двух каналов. Если в первом меньше либо равно
        чем во втором, возвращает True, иначе False
        """
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        """
        Сравнивает количества подписчиков двух каналов.
        Если они равны, возвращает True, иначе False
        """
        return int(self.subscriberCount) == int(other.subscriberCount)






