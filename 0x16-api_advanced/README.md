# 0x16. API Advanced

![API](https://img.shields.io/badge/API-Advanced-blue)
![Reddit](https://img.shields.io/badge/Reddit-API-orange)
![Python](https://img.shields.io/badge/Python-Requests-green)
![Recursion](https://img.shields.io/badge/Recursion-Pagination-red)

## 📋 Description

This advanced API project focuses on mastering complex API interactions including recursive requests, pagination handling, and advanced data processing. Using the Reddit API as a practical example, you'll learn to navigate real-world API challenges like rate limiting, authentication, and large dataset processing.

## 🎯 Learning Objectives

By the end of this project, you should be able to:

- Read and understand API documentation effectively
- Handle API authentication and headers properly
- Implement recursive functions for API pagination
- Process large datasets from API responses
- Handle API rate limiting and error responses
- Parse complex JSON data structures
- Implement efficient data collection strategies
- Use advanced Python techniques for API interactions
- Debug API-related issues and errors
- Optimize API requests for performance

## 📁 Files and Scripts

| File | Description |
|------|-------------|
| `0-subs.py` | Function that queries Reddit API to get subscriber count for a subreddit |
| `1-top_ten.py` | Function that prints titles of first 10 hot posts from a subreddit |
| `2-recurse.py` | Recursive function that returns all hot article titles for a subreddit |
| `100-count.py` | Advanced function that parses titles and counts keyword occurrences |

## 🔧 Reddit API Fundamentals

### API Authentication and Headers
```python
import requests

def get_reddit_headers():
    """
    Returns proper headers for Reddit API requests
    """
    return {
        'User-Agent': 'my-app/1.0 by YourUsername',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

# Example usage
headers = get_reddit_headers()
response = requests.get('https://www.reddit.com/r/python/hot.json', headers=headers)
```

### Understanding Reddit API Structure
```json
{
  "kind": "Listing",
  "data": {
    "modhash": "",
    "dist": 25,
    "children": [
      {
        "kind": "t3",
        "data": {
          "title": "Post Title",
          "score": 1234,
          "num_comments": 56,
          "author": "username",
          "created_utc": 1234567890,
          "url": "https://example.com",
          "selftext": "Post content..."
        }
      }
    ],
    "after": "t3_abc123",
    "before": null
  }
}
```

## 📊 Task Implementation

### 0. Subscriber Count (0-subs.py)
```python
#!/usr/bin/python3
"""
Function that queries the Reddit API and returns the number of subscribers
for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit
        
    Returns:
        int: Number of subscribers, 0 if subreddit doesn't exist
    """
    if not subreddit or not isinstance(subreddit, str):
        return 0
    
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        'User-Agent': 'my-app/1.0 by YourUsername'
    }
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        else:
            return 0
            
    except (requests.RequestException, ValueError, KeyError):
        return 0


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print(number_of_subscribers(sys.argv[1]))
```

### 1. Top Ten Posts (1-top_ten.py)
```python
#!/usr/bin/python3
"""
Function that queries the Reddit API and prints the titles of the first
10 hot posts listed for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit
    """
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'my-app/1.0 by YourUsername'
    }
    params = {
        'limit': 10
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, 
                              allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            if not posts:
                print("None")
                return
            
            for post in posts:
                title = post.get('data', {}).get('title', '')
                if title:
                    print(title)
        else:
            print("None")
            
    except (requests.RequestException, ValueError, KeyError):
        print("None")


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
```

### 2. Recursive API Calls (2-recurse.py)
```python
#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns a list containing
the titles of all the hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries Reddit API to get all hot post titles.
    
    Args:
        subreddit (str): The name of the subreddit
        hot_list (list): List to store post titles
        after (str): Token for pagination
        
    Returns:
        list: List of all hot post titles, None if subreddit doesn't exist
    """
    if not subreddit or not isinstance(subreddit, str):
        return None
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'my-app/1.0 by YourUsername'
    }
    params = {
        'limit': 100,
        'after': after
    }
    
    try:
        response = requests.get(url, headers=headers, params=params,
                              allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            if not posts:
                return hot_list if hot_list else None
            
            # Add titles to the list
            for post in posts:
                title = post.get('data', {}).get('title', '')
                if title:
                    hot_list.append(title)
            
            # Get the 'after' token for next page
            after = data.get('data', {}).get('after')
            
            if after:
                # Recursive call for next page
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return None
            
    except (requests.RequestException, ValueError, KeyError):
        return None


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
```

### 3. Count Keywords (100-count.py)
```python
#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title of all
hot articles, and prints a sorted count of given keywords.
"""
import requests
import re


def count_words(subreddit, word_list, hot_list=[], after=None, word_count={}):
    """
    Recursively queries Reddit API and counts keyword occurrences in titles.
    
    Args:
        subreddit (str): The name of the subreddit
        word_list (list): List of keywords to count
        hot_list (list): List to store post titles
        after (str): Token for pagination
        word_count (dict): Dictionary to store word counts
        
    Returns:
        None: Prints sorted word count results
    """
    if not subreddit or not isinstance(subreddit, str):
        return
    
    # Initialize word_count dictionary on first call
    if not word_count:
        word_count = {word.lower(): 0 for word in word_list}
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'my-app/1.0 by YourUsername'
    }
    params = {
        'limit': 100,
        'after': after
    }
    
    try:
        response = requests.get(url, headers=headers, params=params,
                              allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            if not posts and not after:
                return
            
            # Process titles and count words
            for post in posts:
                title = post.get('data', {}).get('title', '').lower()
                if title:
                    hot_list.append(title)
                    
                    # Count words in title
                    for word in word_list:
                        word_lower = word.lower()
                        # Use regex to find whole words only
                        pattern = r'\b' + re.escape(word_lower) + r'\b'
                        matches = re.findall(pattern, title)
                        word_count[word_lower] += len(matches)
            
            # Get the 'after' token for next page
            after = data.get('data', {}).get('after')
            
            if after:
                # Recursive call for next page
                count_words(subreddit, word_list, hot_list, after, word_count)
            else:
                # Print results when done
                print_results(word_count)
                
    except (requests.RequestException, ValueError, KeyError):
        return


def print_results(word_count):
    """
    Prints the sorted word count results.
    
    Args:
        word_count (dict): Dictionary containing word counts
    """
    # Filter out words with 0 count and sort
    filtered_counts = {k: v for k, v in word_count.items() if v > 0}
    
    if not filtered_counts:
        return
    
    # Sort by count (descending) then alphabetically
    sorted_counts = sorted(filtered_counts.items(), 
                          key=lambda x: (-x[1], x[0]))
    
    for word, count in sorted_counts:
        print(f"{word}: {count}")


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = [x for x in sys.argv[2].split()]
        count_words(subreddit, keywords)
```

## 🔍 Advanced API Techniques

### Error Handling and Resilience
```python
import time
import random
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """
    Decorator to retry API calls on failure.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt) + random.uniform(0, 1))
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=1)
def robust_api_call(url, headers, params):
    """
    Makes API call with retry logic.
    """
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
```

### Rate Limiting Management
```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    """
    Simple rate limiter for API calls.
    """
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """
        Wait if necessary to respect rate limits.
        """
        now = datetime.now()
        
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < timedelta(minutes=1)]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0]).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(now)

# Usage
rate_limiter = RateLimiter(calls_per_minute=30)

def api_call_with_rate_limiting(url, headers, params):
    rate_limiter.wait_if_needed()
    return requests.get(url, headers=headers, params=params)
```

### Advanced Data Processing
```python
def analyze_subreddit_data(subreddit, days=7):
    """
    Advanced function to analyze subreddit posting patterns.
    """
    posts = recurse(subreddit)
    if not posts:
        return None
    
    analysis = {
        'total_posts': len(posts),
        'average_title_length': sum(len(title) for title in posts) / len(posts),
        'most_common_words': get_word_frequency(posts),
        'posting_pattern': analyze_posting_times(subreddit, days),
        'sentiment_analysis': analyze_sentiment(posts)
    }
    
    return analysis

def get_word_frequency(titles, top_n=10):
    """
    Get most common words in titles.
    """
    from collections import Counter
    import re
    
    # Clean and tokenize titles
    all_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    filtered_words = [word for word in all_words if word not in stop_words and len(word) > 2]
    
    return Counter(filtered_words).most_common(top_n)
```

## 📊 Performance Optimization

### Concurrent API Calls
```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

async def fetch_subreddit_data(session, subreddit):
    """
    Asynchronously fetch subreddit data.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'my-app/1.0 by YourUsername'}
    
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        return None

async def fetch_multiple_subreddits(subreddits):
    """
    Fetch data from multiple subreddits concurrently.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_subreddit_data(session, sub) for sub in subreddits]
        results = await asyncio.gather(*tasks)
        return dict(zip(subreddits, results))

# Usage
subreddits = ['python', 'javascript', 'programming', 'webdev']
results = asyncio.run(fetch_multiple_subreddits(subreddits))
```

### Caching Strategies
```python
import json
import os
from datetime import datetime, timedelta
import hashlib

class APICache:
    """
    Simple file-based cache for API responses.
    """
    def __init__(self, cache_dir='cache', expiry_hours=1):
        self.cache_dir = cache_dir
        self.expiry_hours = expiry_hours
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, url, params):
        """Generate cache key from URL and parameters."""
        cache_string = f"{url}_{str(sorted(params.items()) if params else '')}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, url, params=None):
        """Get cached response if available and not expired."""
        cache_key = self._get_cache_key(url, params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - file_time < timedelta(hours=self.expiry_hours):
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        return None
    
    def set(self, url, params, data):
        """Cache API response."""
        cache_key = self._get_cache_key(url, params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        with open(cache_file, 'w') as f:
            json.dump(data, f)

# Usage with cache
cache = APICache(expiry_hours=2)

def cached_api_call(url, headers, params):
    # Try to get from cache first
    cached_data = cache.get(url, params)
    if cached_data:
        return cached_data
    
    # Make API call if not cached
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        cache.set(url, params, data)
        return data
    
    return None
```

## 🔧 Testing and Validation

### Unit Testing
```python
import unittest
from unittest.mock import patch, MagicMock

class TestRedditAPI(unittest.TestCase):
    """Test cases for Reddit API functions."""
    
    @patch('requests.get')
    def test_number_of_subscribers_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {'subscribers': 12345}
        }
        mock_get.return_value = mock_response
        
        result = number_of_subscribers('python')
        self.assertEqual(result, 12345)
    
    @patch('requests.get')
    def test_number_of_subscribers_not_found(self, mock_get):
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = number_of_subscribers('nonexistent')
        self.assertEqual(result, 0)
    
    def test_invalid_subreddit_input(self):
        # Test invalid inputs
        self.assertEqual(number_of_subscribers(None), 0)
        self.assertEqual(number_of_subscribers(''), 0)
        self.assertEqual(number_of_subscribers(123), 0)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing
```python
def integration_test():
    """
    Integration test with real API calls.
    """
    print("Testing real API calls...")
    
    # Test with known good subreddit
    subs = number_of_subscribers('python')
    print(f"Python subreddit subscribers: {subs}")
    assert subs > 0, "Should have subscribers"
    
    # Test with non-existent subreddit
    subs = number_of_subscribers('thisdoesnotexist12345')
    print(f"Non-existent subreddit subscribers: {subs}")
    assert subs == 0, "Should return 0 for non-existent subreddit"
    
    print("All integration tests passed!")

if __name__ == "__main__":
    integration_test()
```

## 📋 Best Practices

### API Usage Guidelines
1. **Always use appropriate User-Agent headers**
2. **Respect rate limits and implement backoff strategies**
3. **Handle errors gracefully and provide meaningful error messages**
4. **Cache responses when appropriate to reduce API calls**
5. **Use HTTPS endpoints for security**
6. **Validate input parameters before making API calls**
7. **Log API interactions for debugging and monitoring**

### Code Quality Standards
```python
# Use type hints for better code documentation
from typing import List, Optional, Dict, Any

def number_of_subscribers(subreddit: str) -> int:
    """
    Returns the number of subscribers for a given subreddit.
    
    Args:
        subreddit: The name of the subreddit
        
    Returns:
        Number of subscribers, 0 if subreddit doesn't exist
        
    Raises:
        requests.RequestException: If API call fails
    """
    pass

def recurse(subreddit: str, hot_list: Optional[List[str]] = None, 
           after: Optional[str] = None) -> Optional[List[str]]:
    """
    Recursively queries Reddit API to get all hot post titles.
    
    Args:
        subreddit: The name of the subreddit
        hot_list: List to store post titles
        after: Token for pagination
        
    Returns:
        List of all hot post titles, None if subreddit doesn't exist
    """
    pass
```

## ✅ Requirements

- Python 3.4.3 or later
- `requests` library installed
- Internet connection for API access
- Valid User-Agent header for Reddit API
- Understanding of recursion and pagination concepts
- Basic knowledge of JSON data structures

## 🎓 Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [JSON Processing in Python](https://docs.python.org/3/library/json.html)
- [Recursion in Python](https://realpython.com/python-recursion/)
- [API Rate Limiting Best Practices](https://cloud.google.com/apis/design/design_patterns#rate_limiting)

## 👨‍💻 Author

**ALX School Project**
- GitHub: [@salmaneben](https://github.com/salmaneben)

---

*This project is part of the ALX School System Engineering & DevOps curriculum.* advanced

## Description
This project focuses on making recursive requests to an API, how to use an API with pagination and how to read API documentation to find the endpoints we’re looking for.

## Table of contents
Files | Description
----- | -----------
[0-subs.py](./0-subs.py) | Python function that queries the Reddit API and returns the number of subscribers (not active users, total subscribers) for a given subreddit
[1-top_ten.py](./1-top_ten.py) | Python function that queries the Reddit API and prints the titles of the first 10 hot posts listed for a given subreddit
[2-recurse.py](./2-recurse.py) | Python recursive function that queries the Reddit API and returns a list containing the titles of all hot articles for a given subreddit
