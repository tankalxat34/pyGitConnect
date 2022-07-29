# pyGitConnect
Python module for more convenient work with GitHub.

[![Downloads](https://pepy.tech/badge/pygitconnect)](https://pepy.tech/project/pygitconnect)
[![Downloads](https://pepy.tech/badge/pygitconnect/month)](https://pepy.tech/project/pygitconnect)
[![Downloads](https://pepy.tech/badge/pygitconnect/week)](https://pepy.tech/project/pygitconnect)
[![Supported Versions](https://img.shields.io/pypi/pyversions/pygitconnect.svg)](https://pypi.org/project/pygitconnect)
[![PyPI](https://img.shields.io/pypi/v/pygitconnect.svg)](https://pypi.org/project/pygitconnect/)
[![PyPi](https://img.shields.io/pypi/format/pygitconnect)](https://pypi.org/project/pygitconnect/)
![GitHub top language](https://img.shields.io/github/languages/top/tankalxat34/pygitconnect)
[![GitHub last commit](https://img.shields.io/github/last-commit/tankalxat34/pygitconnect)](https://github.com/tankalxat34/pygitconnect/commits/main)        
[![GitHub Release Date](https://img.shields.io/github/release-date/tankalxat34/pygitconnect)](https://github.com/tankalxat34/pygitconnect/releases)

[![GitHub Repo stars](https://img.shields.io/github/stars/tankalxat34/pygitconnect?style=social)](https://github.com/tankalxat34/pygitconnect)

# Example of use

```py
import pyGitConnect

# Creating User-object
userGitHub = pyGitConnect.User(
    token="YOUR_TOKEN",
    username="YOUR_USERNAME_ON_GITHUB",
    email="YOUR_EMAIL_ON_GITHUB"
)

# conneting to file on GitHub
file = pyGitConnect.File(userGitHub, "repositoryName/branchName/path/to/your/file.txt")
# getting readable text from file on GitHub
print(file.get().decode("UTF-8"))

# reading file from your drive
newFile = pyGitConnect.NewFile(userGitHub, "B:\\GITHUB\\path\\to\\script.py")
# pushing new file to your repository on GitHub
print(newFile.push("repositoryName/branchName/path/to/your/script/"))

# connecting to uploaded file
uploadedFile = pyGitConnect.File(userGitHub, "repositoryName/branchName/path/to/your/script/script.py")
# printing readable content from uploaded file
print(uploadedFile.get().decode("UTF-8"))
```