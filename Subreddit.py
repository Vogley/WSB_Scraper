import pandas as pd
import praw


class Subreddit:
    def __init__(self, subreddit, praw_instance):
        self.subreddit = subreddit
        self.praw_instance = praw_instance

    def get_from_subreddit(self, limit=100, order='top', time_filter='all'):
        """
        Basic call to grab a list of posts from a subreddit.
        Limit is 1000.
        :param limit:       Integer; Number of posts.
        :param order:       String; hot, new, controversial, top, or gilded
        :param time_filter: String; all, day, hour, month, week, or year
        :return:            List; Reddit post.
        """
        posts = []
        limit = min(1000, limit)
        try:
            sub = self.praw_instance.subreddit(self.subreddit)
            if str(order).lower() == 'top':
                posts = sub.top(limit=limit, time_filter=time_filter)
            elif str(order).lower() == 'new':
                posts = sub.new(limit=limit)
            elif str(order).lower() == 'controversial':
                posts = sub.controversial(limit=limit, time_filter=time_filter)
            elif str(order).lower() == 'gilded':
                posts = sub.gilded(limit=limit, time_filter=time_filter)
            elif str(order).lower() == 'hot':
                posts = sub.hot(limit=limit)
            else:
                print('Invalid Order.')
        except praw.exceptions.APIException as e:
            print(e)
            return []
        except praw.exceptions.ClientException as e:
            print(e)
            return []
        except praw.exceptions.OAuthException as e:
            print(e)
            return []
        finally:
            return posts

    def generate_subreddit_df(self, df_cols=[], limit=100, order='top', time_filter='all'):
        """
        Generates a DataFreame from a list of posts from a subreddit.
        :param df_cols:
        :param limit:       Integer; Number of posts.
        :param order:       String; hot, new, controversial, top, or gilded
        :param time_filter: String; all, day, hour, month, week, or year
        :return:
        """
        submissions = self.get_from_subreddit(limit=limit, order=order)
        subreddit_df = pd.DataFrame.from_records([s.__dict__ for s in submissions])

        # Drop all columns other than the ones specified. If none are specified, then drop none.
        if len(df_cols) != 0:
            subreddit_df = subreddit_df[df_cols]

        return subreddit_df
