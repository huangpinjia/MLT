import json

def check_credentials(username, password):
    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    return username in users and users[username] == password
