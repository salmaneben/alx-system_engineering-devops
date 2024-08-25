#!/usr/bin/python3
"""
0-main
"""
import sys
from 0-subs import number_of_subscribers

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print("{:d}".format(number_of_subscribers(sys.argv[1])))
