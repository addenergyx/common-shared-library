import os
import pandas as pd
import requests, io


class GithubHandler:
    def __init__(self, user: str = os.getenv('GITHUB_USER'),
                 access_token: str = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')) -> None:
        self.user = user
        self.access_token = access_token

    def download_csv(self, raw_csv_url: str, private_repo: bool = False) -> pd.DataFrame:
        github_session = requests.Session()

        if private_repo:
            github_session.auth = (self.user, self.access_token)

        download = github_session.get(raw_csv_url).content
        return pd.read_csv(io.StringIO(download.decode('utf-8')), on_bad_lines='skip')