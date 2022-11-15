import tweepy
from time import sleep
import json
import re

from roast_handler import decide_roast
from credentials import * # You can delete this if you want all your API keys in this file.

# ===============================================================================
# This is the main event.
# This will reply to any tweet the AI deems bad.
# You will need to supply your own Twitter API keys.
# The credentials.py is optional, but put the keys in their respective locations.
# ===============================================================================

# List of anime names that will be used for making the search query.
# We'll use the names that I edited.
with open("Cleaned_Names (edited).txt", "r") as names:
	anime_names = json.load(names)['cleaned names']

# Get's a list of tweets that have been replied to.
try:
    with open("tweet reply index.txt", "r") as indexes:
	    replied = json.load(indexes)['replies']
except FileNotFoundError:
    replied = []

get_tweet_client = tweepy.Client(bearer_token)

create_tweet_client = tweepy.Client( 
    consumer_key=api_key, 
    consumer_secret=secret_key, 
    access_token=access_token, 
    access_token_secret=access_token_secret
    )

def make_names_inputable(anime_name):
    need_anime_keyword = re.search(' \[.*?\]', anime_name)

    if need_anime_keyword is None:
        twitter_inputable = anime_name
        anime_key_inputable = ''
    else:
        twitter_inputable = anime_name.replace(need_anime_keyword.group(0), "")
        anime_key_inputable = need_anime_keyword.group(0).replace("[", "(").replace("]", ")")

    return twitter_inputable, anime_key_inputable

max_tweets = 30
recent_tweets = get_tweet_client.search_recent_tweets(f'classroom of the elite -suggestions -recs -give -ideas -tell -help -favorites -favourites -comment -1. -mutuals -moots -commissions -10% -recommend -recommendations -recommendation -post -posts -question -reply lang:en -is:retweet -is:reply -is:quote', max_results=max_tweets)
counter = 0 # For debug purposes

# For any anime tweet, see if it meets criteria
for tweet in recent_tweets.data:
    tweet_id = tweet['id']
    tweet_text = tweet['text']

    if tweet_id in replied:
        print('\033[93mSkip: Duplicate\033[0m')
        continue

    # IF a tweet has too many new lines, just skips it.
    if tweet_text.count('\n') > 3:
            print('\033[93mSkip New Line\033[0m')
            continue
    else:
        tweet_text.replace('\n', ' ')

    # Get's AI response to tweet.
    response, result = decide_roast(tweet_text)

    if float(result) > 0.4:
        print('\033[93mSkip: Not Bad Enough\033[0m')
        continue

    # Reply to tweet with Roast AI
    try:
        create_tweet_client.create_tweet(text=response, in_reply_to_tweet_id=tweet_id)
    except:
        continue

    replied.append(tweet_id)
    counter += 1
    print(f"Progress for 'Anime Bad' query: {counter}/{max_tweets}")

    #sleep(1)

    #print (f'og: {tweet_text}, resp: {response}, result: {result}')

counter = 0

# After "anime bad" query, loops through different anime names to find more tweets.
for name in anime_names[:500]:
    twitter_input, anime_key_input = make_names_inputable(name)
    recent_anime_tweets = get_tweet_client.search_recent_tweets(f'"{twitter_input}"{anime_key_input} -suggestions -recs -give -ideas -tell -help -favorites -favourites -comment -1. -mutuals -moots -commissions -10% -recommend -recommendations -recommendation -post -posts -question -reply lang:en -is:retweet -is:reply -is:quote', max_results=max_tweets)
    try:
        for tweet in recent_anime_tweets.data:
            tweet_id = tweet['id']
            tweet_text = tweet['text']

            if tweet_id in replied:
                print('\033[93mSkip: Duplicate\033[0m')
                continue

            if tweet_text.count('\n') > 3:
                    print('\033[93mSkip: New Line\033[0m')
                    continue
            else:
                tweet_text.replace('\n', ' ')

            response, result = decide_roast(tweet_text)

            if float(result) > 0.4:
                print('\033[93mSkip: Not Bad Enough\033[0m')
                continue
            
            try:
                create_tweet_client.create_tweet(text=response, in_reply_to_tweet_id=tweet_id)
            except:
                continue

            replied.append(tweet_id)
            counter += 1
            print(f"Progress for '{twitter_input}' query: {counter}/{max_tweets}")
    except TypeError:
        continue
    except KeyboardInterrupt:
        break

        #sleep(1)

        #print (f'og: {tweet_text}, resp: {response}, result: {result}')

    counter = 0

# Save tweets that have been replied to.
# This is used to avoid replying again.
with open("tweet reply index.txt", "w") as outfile:
    out = {"replies": replied}
    json.dump(out, outfile)
