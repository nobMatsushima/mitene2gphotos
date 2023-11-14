import os
from base64 import b64encode

from dotenv import load_dotenv
from gphotospy import authorize
from github import Auth, Github

def create_or_update_variable(repo, name, value=None):
    value = value or os.environ[name]
    # Todo: Use Variable.edit() instead of Repository.delete_variable/create_variable()
    # https://docs.github.com/en/rest/actions/variables?apiVersion=2022-11-28#update-a-repository-variable
    # Variable.edit() of pyGitHub does not work. It only works with the Variable object that Repository.create_variable() returned.
    if any(v for v in repo.get_variables() if v.name == name):
        repo.delete_variable(name)
    repo.create_variable(name, value)

def main():
    """Setup Secrets and Variables for GitHub Actions."""
    load_dotenv()

    # Get Google Photos API token file ("photoslibrary_v1.token" will be created)
    authorize.init('gphotos_oauth.json')

    # Create/Update GitHub Actions Secrets and Variables
    try:
        github_auth = Auth.Token(os.environ['GITHUB_TOKEN'])
    except Exception as e:
        print(f'Please reconfirm that the GitHub token is correctly listed in .env file., Error: {e}')
        exit()
    with Github(auth=github_auth) as g:
        repo = g.get_user().get_repo(os.path.basename(os.getcwd()))
        
        # Secrets: Mitene Browser URL and password
        repo.create_secret('MITENE_BROWSER_URL', os.environ['MITENE_BROWSER_URL'])
        repo.create_secret('MITENE_PASSWORD', os.environ['MITENE_PASSWORD'])
        
        # Secrets: Google Photos OAuth client file and API token
        with open('gphotos_oauth.json', 'rb') as f:
            repo.create_secret('GPHOTOS_CLIENT_SECRET_BASE64', b64encode(f.read()).decode())
        with open(authorize.token_file, 'rb') as f:
            repo.create_secret('GPHOTOS_LIBRARY_TOKEN_BASE64', b64encode(f.read()).decode())
        
        # Variables: Album title and media transfer limit
        create_or_update_variable(repo, 'GPHOTOS_ALBUM_TITLE')
        create_or_update_variable(repo, 'MEDIA_TRANSFER_LIMIT')
        
if __name__ == "__main__":
    main()