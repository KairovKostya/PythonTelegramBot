class Post:
    views: int
    likes: int
    photo_url: str
    message: str

    def __init__(self, views=0, likes=0, photo_url="pass", message=""):
        self.views = views
        self.likes = likes
        self.photo_url = photo_url
        self.message = message
