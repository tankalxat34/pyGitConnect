"""
********************************
*------------------------------*
*---------pyGitConnect---------*
*------------------------------*
********************************
Author: tankalxat34
Description:
    Simple API interface for more convenient work with GitHub service

"""
import getpass

import requests
import base64


class GitHub:
    """Класс для работы с файлами на GitHub"""
    def __init__(self, repo, token, username, email="tankalxat34@gmail.com"):
        self.token = token
        self.username = username
        self.repo = repo
        self.email = email
        self.auth = (self.username, self.token)
        self.url_file = "https://api.github.com/repos/{username}/{repo}/contents/{filepath}?ref={branch}"

    def get_user(self):
        """Возвращает информацию о пользователе"""
        r = requests.get('https://api.github.com/user', auth=self.auth)
        return r.json()

    def get_file(self, filepath, branch="main"):
        """Возвращает текст из текстового файла"""
        doc_response = requests.get(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth).json()["content"]
        try:
            return base64.b64decode(doc_response).decode('utf-8')
        except Exception:
            return base64.b64decode(doc_response)

    def get_file_new_method(self, filepath, branch="main"):
        try:
            return requests.get(requests.get(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth).json()["download_url"], auth=self.auth).content
        except KeyError:
            pass

    def get_image(self, filepath, branch="main"):
        """Возвращает читабельную ссылку на картинку
        Читабельная ссылка - при запросе по этой ссылке и получении атрибута content можно получить саму картинку"""
        response = requests.get(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth).json()["download_url"]
        return response

    def dirlist(self, dirpath="", branch="main"):
        """Список файлов в директории"""
        response = requests.get(self.url_file.format(username=self.username, repo=self.repo, filepath=dirpath, branch=branch), auth=self.auth).json()
        return response

    def decodeToBase64(self, string):
        """Кодировать строку в base64"""
        message_bytes = string.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def create(self, filecontent, filepath, branch="main", commit_message="Created new file / This is an auto commit by tankalxat34`s Python-API"):
        """Создает файл с именем filepath ветки branch. Сопровождает сообщением commit_message

        :param filecontent:         Новый контент в файле. Функция закодирует его в base64 и отправит на GitHub.
        :param filepath:            Путь к файлу на GitHub, в который следует внести такие изменения.
        :param branch:              Ветка, где находится этот файл.
        :param commit_message:      Сообщение к коммиту.
        """
        json_content = {
            "owner": self.username,
            "repo": self.repo,
            "branch": branch,
            "path": filepath,
            "message": commit_message,
            "committer": {
                "name": self.username,
                "email": self.email
            },
            "content": self.decodeToBase64(filecontent)
        }
        response = requests.put(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth, json=json_content).json()
        return response

    def commit(self, filecontent, filepath, branch="main", commit_message="Some changes in file / This is an auto commit by tankalxat34`s Python-API"):
        """Коммитит новые изменения в filepath ветки branch. Сопровождает сообщением commit_message

        :param filecontent:         Новый контент в файле. Функция закодирует его в base64 и отправит на GitHub.
        :param filepath:            Путь к файлу на GitHub, в который следует внести такие изменения.
        :param branch:              Ветка, где находится этот файл.
        :param commit_message:      Сообщение к коммиту.
        """
        doc_response = requests.get(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth).json()
        # print(doc_response)

        json_content = {
            "owner": self.username,
            "repo": self.repo,
            "branch": branch,
            "path": filepath,
            "message": commit_message,
            "committer": {
                "name": self.username,
                "email": self.email
            },
            "content": self.decodeToBase64(filecontent),
            "sha": doc_response["sha"]
        }
        response = requests.put(self.url_file.format(username=self.username, repo=self.repo, filepath=filepath, branch=branch), auth=self.auth, json=json_content).json()
        return response


class Exceptions:
    class FileNotFound(Exception):
        def __init__(self, file):
            super().__init__(f'This file "{file}" was not found on your repository')

    class ErrorToGetContent(Exception):
        def __init__(self, file):
            super().__init__("Error to get content from file " + '"' + file + '". Please, use the "download" method!')


class User:
    """Класс для работы с файлами на GitHub"""
    def __init__(self, token, username, email="tankalxat34@gmail.com"):
        self.token = token
        self.username = username
        self.email = email
        self.auth = (self.username, self.token)
        self.url = "https://api.github.com/repos/{username}/{repo}/contents/{filepath}?ref={branch}"


class File:
    """Класс для работы с конкретным файлом на GitHub

    :param user_class:      Инициализированный экземпляр класса User
    :param repository:      Название репозитория, где находится файл
    :param branch:          Название ветки, где находится файл
    :param path:            Путь к файлу (path/to/your/file.txt)
    """
    def __init__(self, user_class, repository: str, branch: str, path: str):
        self.user = user_class

        self.repository = repository
        self.branch = branch
        self.path = path

        self.url = self.user.url.format(username=self.user.username, repo=self.repository, filepath=self.path, branch=self.branch)
        self.json = requests.get(self.url, auth=self.user.auth)
        self.json = self.json.json()

    def get(self):
        return requests.get(self.json["download_url"], auth=self.user.auth).content

    def download(self, path_to_save=f"C:\\Users\\{getpass.getuser()}\\Downloads\\"):
        with open(path_to_save + self.json["name"], 'wb') as f:
            f.write(requests.get(self.json["download_url"]).content)
        return True

    def decodeToBase64(self, string):
        """Кодировать строку в base64"""
        message_bytes = string.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def create(self, filecontent, commit_message="Created new file / This is an auto commit by pyGitCommit"):
        """Создает файл с именем filepath ветки branch. Сопровождает сообщением commit_message

        :param filecontent:         Новый контент в файле. Функция закодирует его в base64 и отправит на GitHub.
        :param commit_message:      Сообщение к коммиту.
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

    def commit(self, filecontent, commit_message="Some changes in file / This is an auto commit by pyGitCommit"):
        """Коммитит новые изменения в filepath ветки branch. Сопровождает сообщением commit_message

        :param filecontent:         Новый контент в файле. Функция закодирует его в base64 и отправит на GitHub.
        :param commit_message:      Сообщение к коммиту.
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

