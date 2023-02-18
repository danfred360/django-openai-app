import requests
import os
import json

class BearerOAuth(requests.auth.AuthBase):
    def __call__(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {os.environ.get('TWITTER_BEARER_TOKEN')}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r

class TweetLookup:
    def __init__(self, authour_id, max_results, pagination_token=None):
        # To set your enviornment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

        if pagination_token is None:
            url = self.create_url(authour_id, max_results)
        else:
            url = self.create_url(authour_id, max_results, pagination_token)
        self.response = self.connect_to_endpoint(url)


    # TODO use pagination_token parameter to load results until max_result
    def create_url(self, author_id, max_results, pagination_token=None):
        tweet_fields = "tweet.fields=lang,author_id"
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        ids = "ids={}".format(author_id) # specifying specific tweets instead of all user tweets
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        max_results_param = "max_results={}".format(max_results)
        exclude = "exclude={}".format("retweets,replies")
        if pagination_token is None:
            url = "https://api.twitter.com/2/users/{}/tweets?{}&{}".format(author_id, exclude, max_results_param)
        else:
            pagination_token_param = "pagination_token={}".format(pagination_token)
            url = "https://api.twitter.com/2/users/{}/tweets?{}&{}&{}".format(author_id, exclude, max_results_param, pagination_token_param)
        # "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        return url


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r


    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=self.bearer_oauth)
        status_code = response.status_code
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json(), indent=4, sort_keys=True)


class UserLookup:

    def __init__(self, username_query):
        # To set your enviornment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        # self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        url = self.create_url(username_query)
        self.response = self.connect_to_endpoint(url)


    def create_url(self, username_query):
        # Specify the usernames that you want to lookup below
        # You can enter up to 100 comma-separated values.
        usernames = "usernames={}".format(username_query)
        user_fields = "user.fields=description,created_at"
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        return url


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=BearerOAuth())
        status_code = response.status_code # do nothing
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json(), indent=4, sort_keys=True)
