import os

from dotenv import load_dotenv
from tqdm import tqdm

from mitene_crawler import MiteneCrawler
from google_photos_uploader import GooglePhotosUploader

def main():
    if os.getenv('GITHUB_ACTIONS') is True:
        try:
            # Save Google Photos API OAuth client secret as a file.
            with open(os.environ['GPHOTS_CLIENT_SECRET_FILENAME'], mode='wb') as f:
                f.write(os.environ['GPHOTOS_CLIENT_SECRET_BASE64'].decode('base64'))
            # Save Google Photos Library token as a file.
            with open(os.environ['photoslibrary_v1.token'], mode='wb') as f:
                f.write(os.environ['GPHOTOS_LIBRARY_TOKEN_BASE64'].decode('base64'))
        except KeyError:
            print(f'Please reconfirm that the client secret and the library token are correctly set on Github Secrets or Variables.')
            exit()
    else:
        # Load .env file if running outside of GitHub Actions.
        load_dotenv()
    config = os.environ

    # Initialize Mitene bot and Google Photos uploader
    try:
        mitene_bot = MiteneCrawler(config['MITENE_BROWSER_URL'], config['MITENE_PASSWORD'])
    except Exception as e:
        print(f'Please reconfirm that the URL and password are correctly listed in the configuration file., Error: {e}')
        exit()
    gphotos = GooglePhotosUploader(config['GPHOTOS_CLIENT_SECRET_FILENAME'], config['GPHOTOS_ALBUM_TITLE'])    
    
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