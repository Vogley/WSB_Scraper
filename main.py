#! usr/bin/env python3
import datetime as dt

import keyring
import praw
import matplotlib.pyplot as plt

from Subreddit import Subreddit

import reticker

LIMIT = 1000
CLIENT_ID = keyring.get_password('reddit', 'script_id')
CLIENT_SECRET = keyring.get_password('reddit', 'secret')
USER_AGENT = 'Vogley_Python_NLP'
USERNAME = keyring.get_password('reddit', 'username')
PASSWORD = keyring.get_password('reddit', 'password')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=USERNAME,
                     password=PASSWORD)


def listToFreqDict(my_list):
    """
    Helper Function to generate a frequency dictionary from a list.
    :param my_list: List
    :return:        Dictionary with list item as key, and frequency as value.
    """
    freq_dict = {}
    for item in my_list:
        if item in freq_dict:
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1

    return freq_dict


if __name__ == '__main__':
    # Parameters
    subreddit = 'wallstreetbets'
    limit = 100
    order = 'hot'
    subreddit_cols = ["title", "score", "id", "url", "num_comments", "created", "selftext"]

    # Classes
    sub = Subreddit(subreddit=subreddit, praw_instance=reddit)
    extractor = reticker.TickerExtractor()

    # Subreddit Submissions
    submissions = sub.generate_subreddit_df(limit=limit, order=order, df_cols=subreddit_cols)

    # Format Date Column
    timestamp = submissions["created"].apply(lambda d: dt.datetime.fromtimestamp(d))
    subreddit_df = submissions.assign(timestamp=timestamp)

    # Extract Stock Tickers
    subreddit_df['text'] = subreddit_df['title'] + ' ' + subreddit_df['selftext']
    subreddit_df['tickers'] = subreddit_df['text'].apply(lambda s: extractor.extract(s))

    # * * * * * * * * * * *
    # Reporting on Findings
    # * * * * * * * * * * *

    # Get list of listed tickers
    non_tickers = ['DD', 'YOLO', 'US', 'LOSS', 'GAIN']  # Just some typical WSB talk that are also technically tickers.
    ticker_list = [item for row in subreddit_df['tickers'] for item in row if item not in non_tickers]
    ticker_freq_dict = listToFreqDict(ticker_list)
    ordered_dict = {k: v for k, v in sorted(ticker_freq_dict.items(), key=lambda x: x[1], reverse=True)[:10]}

    plt.bar(ordered_dict.keys(), ordered_dict.values())
    plt.show()

