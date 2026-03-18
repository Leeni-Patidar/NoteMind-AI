import json
from config import HISTORY_FILE
import os


def save_history(user, query, result):

    # create file if not exists
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump({}, f)

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    if user not in data:
        data[user] = []

    data[user].append({
        "query": query,
        "result": result
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_history(user):

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data.get(user, [])
    except:
        return []
