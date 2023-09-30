import os
import re
import json
import itertools

import requests
from bs4 import BeautifulSoup

class MiteneCrawler:
    """MiteneCrawler class for crawling and downloading media files from Mitene."""

    def __init__(self, url_for_browser_user, login_password):
        """Initialize the MiteneCrawler with the browser user's URL and login password.
        Raises:
        Exception: If the login attempt fails."""
        self.url = url_for_browser_user
        self.login_password = login_password
        url_suffix = '/login'
        
        # Get login page for authenticity_token
        self.session = requests.Session()
        login_page_response = self.session.get(self.url + url_suffix)
        login_page_content = BeautifulSoup(login_page_response.content, 'html.parser')
        csrf_token = login_page_content.find('meta', attrs={'name': 'csrf-token'}).get('content')
        login_payload = {
            'authenticity_token': csrf_token,
            'session[password]': self.login_password,
            'commit': 'Login'
        }

        # Attempting login
        login_request_response = self.session.post(self.url + url_suffix, data=login_payload)

        # Checking the result of the login attempt
        if 'Forgot Your Password?' in login_request_response.text:
            raise Exception('Login Failed')

    def media_iter(self):
        """Retrieve a iist of all available media files.
        The iterator response slows down every 25 pages due to the page loading."""
        url_suffix = '?page='
        media_pattern = r'gon\.media\s*=\s*({.*?});'
        print(f'Listing media files on Mitene page... ', end='')
        for page in itertools.count(start=1):
            response = self.session.get(self.url + url_suffix + str(page))
            media = json.loads(re.search(media_pattern, response.text).group(1))
            print(f'{page}, ', end='')
            yield from media['mediaFiles']
            if not media['hasNext']:
                print('done')
                return
            
    def filename(self, media):
        return f'{media["uuid"]}.{media["contentType"].split("/")[1]}'

    def download(self, media):
        """Download a media file given its UUID and content type.
        Raises:
        Exception: If the file download or save fails."""
        download_url = self.url + '/media_files/' + media['uuid'] + '/download'
        response = self.session.get(download_url)
        response.raise_for_status()
        try:
            with open(self.filename(media), 'wb') as file:
                file.write(response.content)
            return os.path.join(os.getcwd(), self.filename(media))
        except Exception as e:
            print(f'Failed to save file: {e}')