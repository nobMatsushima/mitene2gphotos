# :baby: mitene2gphotos :framed_picture:
Mirror your [Mitene](https://mitene.us/)([FamilyAlbum](https://family-album.com/)) to Google Photos daily
- [app.py](app.py) is designed to copies Mitene media files to Google Photos.
- [cron_workflow.yml](.github/workflows/cron_workflow.yml) runs [app.py](app.py) on GitHub Actions daily.
  - [setup_github_actions.py](set_github_actions.py) is a utility that helps you set or update your configurations and credentials into GitHub Secrets and Variables.

## :sparkles: Motivation
Display your daily-updated Mitene photos and videos on digital frames compatible with Google Photos, like [Aura](https://auraframes.com/), [Nixplay](https://www.nixplay.com/), [Google Nest Hub](https://support.google.com/googlenest/answer/9136992) or [Google TV](https://support.google.com/googletv/answer/10070821).

## :hugs: Responsible Manner
Please be respectful and follow the terms of service to ensure that everyone can enjoy the heartwarming service.

##### [Terms of Use for FamilyAlbum](https://family-album.com/terms)
> Article 13: Prohibited Acts  
> The Users may not engage in any of the following acts when using the Service:  
> ...  
> (19) Acts that impose or are deemed likely to impose a burden on the server of the Company or a third party; or acts that hinder or are deemed likely to hinder the operation of the Service or the network system;  

##### [家族アルバム みてね利用規約](https://mitene.us/ja/terms)
> 第13条　禁止事項  
> ユーザーは、本サービスの利用にあたり、次に掲げる行為を行ってはならないものとします。  
> ...  
> (19) 弊社または第三者のサーバーに負担をかける行為、もしくは、本サービスの運営やネットワーク・システムに支障を与える行為、またはこれらのおそれのある行為。

## :gear: Setup
Create a `.env` file by copying `.env.example` and fill in your configuration.

#### Mitene Browser URL and Password
Use your browser version user credentials. If you don't have any, you'll need to add a user to your album.
```.env
# Mitene
MITENE_BROWSER_URL = https://mitene.us/f/YourUrl
MITENE_PASSWORD = your_password
```

#### Google Cloud Console Client Secret
Place your OAuth client file as `gphotos_oauth.json` in the same directory as `app.py`. Basically, follow the [Set up authorization guide](https://github.com/davidedelpapa/gphotospy#set-up-authorization) on gPhotoSpy repository.
- You don't need to use the same accounts for Google Cloud Console Developer and Google Photos User.
- The following URLs must be added to OAuth 2.0 Client IDs > Authorized redirect URIs.
  - http://localhost:8080/
  - https://github.com # if you set up GitHub Actions
- Adding Google Photos User account to OAuth consent screen > Test users is also required for unpublished usecases.

#### App Configuration
Google Photos album title and maximum media count per run are customizable.
```.env
# App configuration
GPHOTOS_ALBUM_TITLE = Mitene Mirror
MEDIA_TRANSFER_LIMIT = 25
```

## :rocket: Usage
You can simply run `app.py` on the local environment.
```
pip install -r requirements.txt
python app.py
```
It launches your default web browser for authorization at the first time and creates `photoslibrary_v1.token` in the same directory.

## :arrows_counterclockwise: Work with GitHub Actions
If you would like to set up daily routine on GitHub Actions, you'll need to fork this project and set up `cron_workflow.yml`.
`setup_github_actions.py` will help you upload your local `.env` configurations you set up above to your repository's GitHub Actions Secret and Variables.
A GitHub personal access token with read permissions for Metadata and read/write permissions for Secrets/Variables must be written in `.env`

```.env
# GitHub personal access token (only required for setup_github_actions.py)
# Note: Read and Write access to Actions Secrets and Variables are required
GITHUB_TOKEN = github_pat_XXXYYYZZZ
```
Of course, you can manually set your configurations in your repository's Setting > GitHub Actions page.

## :books: Related Works
#### Dependencies
- [gPhotoSpy](https://github.com/davidedelpapa/gphotospy): An unofficial Python library for interacting with Google Photos
- [PyGithub](https://github.com/PyGithub/PyGithub): An unoffical Python library to access the GitHub REST API
- Please refer to [requirements.txt](requirements.txt) for other packages.

#### Mitene Downloader
The following repositories may also be helpful if you don't upload media files to Google Photos.
| Repository                                                                        | Runtime         | Target media files                           |
| --------------------------------------------------------------------------------- | --------------- | -------------------------------------------- |
| [perrinjerome/mitene_download](https://github.com/perrinjerome/mitene_download)   | Python          | All media files                              |
| [OGAWASanshiro/mitene-download](https://github.com/OGAWASanshiro/mitene-download) | Python+Selenium | Media files for the user-defined time period |
| [shin-sforzando/mitene-crawler](https://github.com/shin-sforzando/mitene-crawler) | Node.js         | All media files                              |
| [miworky/miteneDownloader](https://github.com/miworky/miteneDownloader)           | Node.js         | Media files on each page                     |