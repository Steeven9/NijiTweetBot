from os import getenv

from tweepy import Client

from data import guerrilla_keywords, schedule_keywords, talents

# Separator between tweets
separator = "---------------------------------"
# Twitter bearer token
bearer_token = getenv("TWITTER_BEARER_TOKEN")

if bearer_token == None:
    raise ValueError("Twitter bearer token not found!")
client = Client(bearer_token, wait_on_rate_limit=True)


# Matches tweets that:
# - have a keyword from schedule_keywords in them and have an image attached
#   OR have a keyword from guerrilla_keywords in them
# - are not retweets
# - are from someone in the talents array
def fetch_tweets(newest_id, talents):
    user_names = []
    for user in talents:
        user_names.append(user.username)
    query = "-is:retweet ((" + " OR ".join(
        guerrilla_keywords) + ") OR ((" + " OR ".join(
            schedule_keywords) + ") has:media)) (from:"
    query += " OR from:".join(user_names)
    query += ")"
    response = client.search_recent_tweets(query,
                                           since_id=newest_id,
                                           max_results=len(user_names),
                                           expansions=["author_id"])

    new_tweets = response.meta["result_count"]
    if new_tweets != 0:
        newest_id = response.meta["newest_id"]
    return [response, new_tweets, newest_id]


# Matches spaces that:
# - are from the talents array
def fetch_spaces(talents):
    user_ids = []
    for user in talents:
        user_ids.append(user.id)
    response = client.get_spaces(user_ids=user_ids, expansions=["creator_id"])
    new_spaces = response.meta["result_count"]
    return [response, new_spaces]


def fetch_user_ids():
    usernames = ",".join(talents)
    response = client.get_users(usernames=usernames).data
    return [response, len(response)]
