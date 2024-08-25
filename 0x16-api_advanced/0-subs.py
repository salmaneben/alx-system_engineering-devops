#!/usr/bin/python3
"""Fetch the number of subscribers for a given subreddit."""
import requests

def number_of_subscribers(subreddit):
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "My-User-Agent"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        # Debugging: Print the status code
        print("Status Code:", response.status_code)
        # Debugging: Print the raw response content
        print("Response Content:", response.content)

        if response.status_code == 200:
            return response.json().get('data', {}).get('subscribers', 0)
        return 0
    except requests.RequestException as e:
        # Debugging: Print any request exceptions that occur
        print("Request Exception:", e)
        return 0
