from bs4 import BeautifulSoup
import requests

r = requests.get("https://raw.githubusercontent.com/Selman3447/SynMax/main/version")

soup = BeautifulSoup(r.content, "html.parser")
version = soup.get_text()
version = version.split("\n")[0]

app_ver = open("uis\\version", "r").read()

def update():
    pass


def check_updates():
    if version > app_ver:
        print("Update Avalible:", version)
    else:
        print("No Update")

check_updates()