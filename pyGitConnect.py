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
import re


def decodeToBase64(string: str):
    """Decode string to base64"""
    message_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


class Exceptions:
    class FileNotFound(Exception):
        def __init__(self, file, repo):
            super().__init__(
                f'This file "{file}" was not found on repository "{repo}"')

    class ErrorToGetContent(Exception):
        def __init__(self, file):
            super().__init__("Error to get content from file " +
                             '"' + file + '". Please, use the "download" method!')

    class InvalidEmail(Exception):
        def __init__(self, email):
            super().__init__("Invalid email: '" + email + "'")


class User:
    def __init__(self, token: str, username: str, email: str):
        """Class for work with GitHub"""
        self.token = token
        self.username = username
        if len(re.findall("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+$", email)) == 0:
            raise Exceptions.InvalidEmail(email)
        self.email = email
        self.auth = (self.username, self.token)
        self.url = "https://api.github.com/repos/{username}/{repo}/contents/{filepath}?ref={branch}"


class NewFile:
    def __init__(self, user_class: User, filepath: str):
        """Creating NewFile-object for pushing to GitHub"""
        self.filepath = filepath
        self.filename = self.filepath.split("\\")[::-1][0]
        self.user = user_class

        with open(self.filepath, "r", encoding="UTF-8") as file:
            self.filecontent = file.read()

    def push(self, commit_path: str, commit_message="Created new file / This is an auto commit"):
        """Creating new file in branch with commit message

        :param commit_path: Path to file on GitHub on format "repositoryName/branchName/path/to/your/file.txt"
        :param commit_message:      Message for commit.
        """
        repository = commit_path.split("/")[0]
        branch = commit_path.split("/")[1]
        path = "/".join(commit_path.split("/")[2:]) + self.filename

        self.url = self.user.url.format(
            username=self.user.username, repo=repository, filepath=path, branch=branch)

        json_content = {
            "owner": self.user.username,
            "repo": repository,
            "branch": branch,
            "path": path,
            "message": commit_message,
            "committer": {
                "name": self.user.username,
                "email": self.user.email
            },
            "content": decodeToBase64(self.filecontent)
        }
        response = requests.put(
            self.url, auth=self.user.auth, json=json_content).json()
        return response


class File:
    def __init__(self, user_class: User, github_path):
        """Class for work with file on GitHub

        :param user:      Initialized a copy of User-class
        :param github_path: Path to file on GitHub on format "repositoryName/branchName/path/to/your/file.txt"
        """
        self.user = user_class
        self.github_path = github_path

        self.repository = github_path.split("/")[0]
        self.branch = github_path.split("/")[1]
        self.path = "/".join(github_path.split("/")[2:])

        self.url = self.user.url.format(
            username=self.user.username, repo=self.repository, filepath=self.path, branch=self.branch)
        self.json = requests.get(self.url, auth=self.user.auth)
        if (self.json.status_code != 200):
            raise Exceptions.FileNotFound(self.path, self.repository)
        self.json = self.json.json()

    def get(self):
        """Get byte content from file

        If file is text - use `decode("UTF-8")` for get readable content.
        """
        return requests.get(self.json["download_url"], auth=self.user.auth).content

    def download(self, path_to_save: str = f"C:\\Users\\{getpass.getuser()}\\Downloads\\"):
        """Download file in folder"""
        with open(path_to_save + self.json["name"], 'wb') as f:
            f.write(requests.get(self.json["download_url"]).content)
        return True

    def commit(self, filecontent: str, commit_message="Some changes in file / This is an auto commit"):
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
            "content": decodeToBase64(filecontent),
            "sha": doc_response["sha"]
        }

        response = requests.put(
            self.url, auth=self.user.auth, json=json_content).json()
        return response
