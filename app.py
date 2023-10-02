import os

from dotenv import load_dotenv
from tqdm import tqdm

from mitene_crawler import MiteneCrawler
from google_photos_uploader import GooglePhotosUploader

def main():
    if not os.getenv('GITHUB_ACTIONS'):
        # Load .env file if running outside of GitHub Actions.
        load_dotenv()
    config = os.environ

    # Initialize Mitene bot and Google Photos uploader
    try:
        mitene_bot = MiteneCrawler(config['MITENE_BROWSER_URL'], config['MITENE_PASSWORD'])
    except Exception as e:
        print(f'Please reconfirm that the URL and password are correctly listed in the configuration file., Error: {e}')
        exit()
    gphotos = GooglePhotosUploader('gphotos_oauth.json', config['GPHOTOS_ALBUM_TITLE'])
    
    # Pick up all unsynchronized media files from new to old
    upload_media_list = []
    for media in mitene_bot.media_iter():
        # Stop if the media already exists in Google Photos
        if gphotos.exists(mitene_bot.filename(media)):
            break
        upload_media_list.append(media)

    # Copy media files from Mitene to Google Photos
    upload_media_list.reverse()
    progress_bar = tqdm(upload_media_list[:int(config['MEDIA_TRANSFER_LIMIT']):])
    for media in progress_bar:
        progress_bar.set_description(mitene_bot.filename(media))
        try:
            filepath = mitene_bot.download(media)
            gphotos.upload(filepath)
        except Exception as e:
            print(f'Copy Failed: {media}, Error: {e}')
        finally:
            os.remove(filepath)

if __name__ == "__main__":
    main()