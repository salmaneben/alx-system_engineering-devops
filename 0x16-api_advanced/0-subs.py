#!/usr/bin/python3
import requests

def number_of_subscribers(subreddit):
    """Returns the total number of subscribers for a given subreddit."""
    base_url = 'https://www.reddit.com'
    api_uri = f'{base_url}/r/{subreddit}/about.json'

    # Set a custom User-Agent
    user_agent = {'User-Agent': 'MyRedditAPI/0.1'}

    try:
        # Get the response from the Reddit API
        res = requests.get(api_uri, headers=user_agent, allow_redirects=False)

        # Debugging: Print status code and response text
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")

        # Check if the subreddit is invalid or there is an error
        if res.status_code == 200:
            data = res.json().get('data', {})
            return data.get('subscribers', 0)
        else:
            return 0

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return 0

