from src.channel import Channel


class Video:
    """Класс для видео ютуб"""

    # Объект для работы с YouTube API
    youtube = Channel.get_service()

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=video_id
                                                 ).execute()
        try:
            self.title: str = self.video['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title: str = self.video['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count: int = self.video['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает строку с названием видео"""
        return self.title


class PLVideo(Video):
    """Класс для плейлиста видео ютуб, дочерний от Video"""

    def __init__(self, video_id, pl_id):
        """Расширяет функционал класса Video добавлением id плейлиста"""
        super().__init__(video_id)
        self.pl_id = pl_id


