#!/usr/bin/python3
import requests

def number_of_subscribers(subreddit):
    # Define the URL for the subreddit
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
   
    # Set the User-Agent to avoid being blocked by Reddit
    headers = {'User-Agent': 'my-user-agent'}
   
    # Make the GET request to the Reddit API
    response = requests.get(url, headers=headers, allow_redirects=False)
   
    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json().get('data')
        # Return the number of subscribers
        return data.get('subscribers', 0)
    else:
        # Return 0 if the subreddit is invalid or any other error occurs
        return 0
