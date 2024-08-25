#!/usr/bin/python3
"""Module for task 0"""
import requests

def number_of_subscribers(subreddit):
    """Queries the Reddit API and returns the number of subscribers
    to the subreddit."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "My-User-Agent"}

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return 0
    
    try:
        data = response.json().get("data", {})
        return data.get("subscribers", 0)
    except ValueError:
        return 0
