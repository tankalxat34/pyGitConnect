"""
********************************
*------------------------------*
*---------pyGitConnect---------*
*------------------------------*
********************************
Author: tankalxat34
Description:
    Simple API interface for more convenient work with GitHub service

- github: https://github.com/tankalxat34/pyGitConnect
- email: mailto:tankalxat34@gmail.com
- telegram: https://t.me/tankalxat34
"""
import getpass

import requests
import base64

class Exceptions:
    class FileNotFound(Exception):
        def __init__(self, file):
            super().__init__(f'This file "{file}" was not found on your repository')

    class ErrorToGetContent(Exception):
        def __init__(self, file):
            super().__init__("Error to get content from file " + '"' + file + '". Please, use the "download" method!')


class User:
    def __init__(self, token: str, username: str, email="tankalxat34@gmail.com"):
        """Class for work with GitHub"""
        self.token = token
        self.username = username
        self.email = email
        self.auth = (self.username, self.token)
        self.url = "https://api.github.com/repos/{username}/{repo}/contents/{filepath}?ref={branch}"


class File:
    def __init__(self, user_class: User, repository: str, branch: str, path: str):
        """Class for work with file on GitHub

        :param user:      Initialized a copy of User-class
        :param repository:      Repository name
        :param branch:          Branch name
        :param path:            Path to file in repository (path/to/your/file.txt)
        """
        self.user = user_class

        self.repository = repository
        self.branch = branch
        self.path = path

        self.url = self.user.url.format(username=self.user.username, repo=self.repository, filepath=self.path, branch=self.branch)
        self.json = requests.get(self.url, auth=self.user.auth)
        self.json = self.json.json()

    def get(self):
        """Get byte content from file"""
        return requests.get(self.json["download_url"], auth=self.user.auth).content

    def download(self, path_to_save: str = f"C:\\Users\\{getpass.getuser()}\\Downloads\\"):
        """Download file in folder"""
        with open(path_to_save + self.json["name"], 'wb') as f:
            f.write(requests.get(self.json["download_url"]).content)
        return True

    def decodeToBase64(self, string: str):
        """Encode string to base64"""
        message_bytes = string.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def create(self, filecontent: str, commit_message="Created new file / This is an auto commit by pyGitCommit"):
        """Creating file in branch with commit message

        :param filecontent:         Readable content in file in string format.
        :param commit_message:      Message for commit.
        """
        json_content = {
            "owner": self.user.username,
            "repo": self.repository,
            "branch": self.branch,
            "path": self.path,
            "message": commit_message,
            "committer": {
                "name": self.user.username,
                "email": self.user.email
            },
            "content": self.decodeToBase64(filecontent)
        }
        response = requests.put(self.url, auth=self.user.auth, json=json_content).json()
        return response

    def commit(self, filecontent: str, commit_message="Some changes in file / This is an auto commit by pyGitCommit"):
        """Commiting file in branch with commit message

        :param filecontent:         Readable content in file in string format.
        :param commit_message:      Message for commit.
        """
        doc_response = requests.get(self.url, auth=self.user.auth).json()

        json_content = {
            "owner": self.user.username,
            "repo": self.repository,
            "branch": self.branch,
            "path": self.path,
            "message": commit_message,
            "committer": {
                "name": self.user.username,
                "email": self.user.email
            },
            "content": self.decodeToBase64(filecontent),
            "sha": doc_response["sha"]
        }

        response = requests.put(self.url, auth=self.user.auth, json=json_content).json()
        return response

