from gphotospy import authorize
from gphotospy.album import Album
from gphotospy.media import Media

class GooglePhotosUploader:
    def __init__(self, client_secret_file, album_title):
        # Authorization (Opens default browser if the app is not verified.)
        self.service = authorize.init(client_secret_file)

        # Target Album
        self.album = None
        album_manager = Album(self.service)
        try:
            self.album = next((album for album in album_manager.list() if album['title']==album_title), None)
        except TypeError as e:
            self.album = None
        finally:
            if self.album is None:
                self.album = album_manager.create(album_title)
                print(f'Album Created: {self.album["title"]}')
        
        # All Media filenames in the album
        self.filenames = []
        self.media_manager = Media(self.service)
        try:
            self.filenames = [media['filename'] for media in self.media_manager.search_album(self.album['id'])]
        except TypeError as e:
            self.filenames = []
        
    def exists(self, filename):
        return filename in self.filenames
    
    def upload(self, filepath):
        """Uploads a file to Google Photos
        Returns:
        Upload Token if successfull, otherwise None
        """
        try:
            self.media_manager.stage_media(filepath)
            return self.media_manager.batchCreate(self.album['id'])
        except Exception as e:
            print(f'Upload Failed: {e}')