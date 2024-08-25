#!/usr/bin/python3
"""Module for task 1"""

import requests

def top_ten(subreddit):
    """Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit"""
    
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "My-User-Agent"}
    
    response = requests.get(url, headers=headers, allow_redirects=False)
    
    if response.status_code >= 300:
        print(None)
        return
    
    data = response.json().get("data")
    
    if data is None:
        print(None)
        return
    
    posts = data.get("children")
    
    if not posts:
        print(None)
        return
    
    for post in posts:
        print(post.get("data").get("title"))
