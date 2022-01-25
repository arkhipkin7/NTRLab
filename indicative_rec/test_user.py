import json
import argparse
import requests
from pprint import pprint

HEADERS = {"Content-Type": "application/json"}
URL_USER = 'http://127.0.0.1:8080/api/predict'
URL_BOOK = 'http://127.0.0.1:8080/api/similar'


def get_user_id():
    parser = argparse.ArgumentParser(description='Test user recommendations')
    parser.add_argument('-u', dest='user', type=str)
    parser.add_argument('-i', dest='item', type=str)

    args = parser.parse_args()

    return args.user, args.item


def main():
    user_id, item_id = get_user_id()
    if user_id is not None:
        try:
            response = requests.post(URL_USER,
                                     headers=HEADERS,
                                     data=json.dumps({"user_id": user_id}))
            pprint(response.json())
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    if item_id is not None:
        try:
            response = requests.post(URL_BOOK,
                                     headers=HEADERS,
                                     data=json.dumps({"book_id": item_id}))
            pprint(response.json())
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


if __name__ == '__main__':
    main()