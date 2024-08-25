#!/usr/bin/python3
"""
0-main
"""
import sys

def number_of_subscribers(subreddit):
    import requests
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {'user-agent': 'request'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return 0

    data = response.json().get("data")
    num_subs = data.get("subscribers", 0)  # Default to 0 if not found

    return num_subs

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subscribers = number_of_subscribers(sys.argv[1])
        if subscribers > 0:
            print("OK")
        else:
            print("0")

