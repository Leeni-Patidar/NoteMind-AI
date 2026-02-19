import json
from config import HISTORY_FILE


def save_history(user, query, result):

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
        json.dump(data, f)


def load_history(user):

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)

            return data.get(user, [])

    except:
        return []
