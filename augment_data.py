import pandas as pd

# ===========================================
# Augments data for AI if there isn't enough.
# This is targeted at negatively labeled data.
# ===========================================

df = pd.read_csv('new data/best result.csv')
print(len(df))
tweets = df[df['result']==0]
print(len(tweets))

words_to_replace = {
    "good": ["fine", "acceptable", "excellent", "exceptional", "great", "marvelous", "satisfactory", "superb", "wonderful"],
    "bad": ["atrocious", "awful", "cheap", "crummy", "dreadful", "lousy", "poor", "rough", "sad", "unacceptable"],
    "people": ["folk", "individuals", "humans"],
    "fun": ["amusing", "enjoyable", "entertaining", "lively", "pleasant"],
    "like": ["admire", "appreciate", "go for", "love", "adore", "dig"],
    "love": ["admire", "care for", "cherish", "go for", "prize", "treasure", "worship"],
    "dislike": ["abhor", "avoid", "condemn", "deplore", "despise", "detest", "dsapprove", "loathe", "resent", "scorn", "shun"],
    "sad": ["bitter", "somber", "unhappy"],
    "better": ["exceptional", "superior", "perferred"],
    "best": ["finest", "first-rate", "outstanding", "perfect", "terrific"],
    "started": ["began"],
    "starting": ["beginning"],
    "masterpiece": ["classic", "gem", "jewel", "monument", "treasure"],
    "never": ["at no time", "no way", "not ever"],
    "seen": ["looked at", "checked"],
    "similar": ["akin", "analogous", "comparable", "related"],
    "mid": ["meh", "okay", "not that great", "lukewarm", "boring"],
    "mad": ["distraught", "exasperated", "frantic", "furious", "livid"],
    "worst": ["lowest"],
    "finished": ["concluded", "ended", "stopped"],
    "overrated": ["exaggerated", "hyped-up", "puffed-up"],
    "top": ["number one", "winner", "champion"],
    "enjoy": ["appreciate", "like", "love", "relish", "revel in", "savor"],
    "enjoyed": ["appreciated", "liked", "loved", "relished", "reveled in", "savored"],
    "enjoying": ["appreciating", "liking", "loving", "relishing", "reveling in", "savoring"],
    "bored": ["disinterested", "tired"],
    "boring": ["dull", "lifeless", "mundane", "monotonous", "stale", "stupid", "tedious", "tiresome", "tiring", "uninteresting"],
    "weird": ["awful", "eccentric", "odd", "bizarre"],
    "terrible": ["bad", "horrible", "abhorrent", "appalling", "awful", "dreadful", "horrid"],
    "literally": ["truly", "simply", "really"],
    "well": ["good", "fine", "right"],
    "horrible": ["unpleasant", "abhorrent", "appaling", "awful", "disgusting", "dreadful", "horrid", "nasty", "terrible"],
}

new_dict = {'tweet': [], 'replies': [], 'retweets': [], 'likes': [], 'ratio': [], 'result':[]}

# Essentially just replaces words with their appropriate synoymns.
for tweet in tweets['tweet']:
    words = tweet.split()

    for word in words_to_replace:
        if word in words:
            for synonym in words_to_replace[word]:
                #print(synonym)
                reassembled_tweet = ' '.join(words)
                new_tweet = reassembled_tweet.replace(word, synonym)
                new_dict['tweet'].append(new_tweet)
                new_dict['replies'].append(0)
                new_dict['retweets'].append(0)
                new_dict['likes'].append(0)
                new_dict['ratio'].append(0)
                new_dict['result'].append(0)

new_new_dict = {'tweet': [], 'replies': [], 'retweets': [], 'likes': [], 'ratio': [], 'result':[]}

# Sometimes, a tweet will have multiple words that can be replaced.
# This will create variations with or without those words.
for tweet in new_dict['tweet']:
    words = tweet.split()

    for word in words_to_replace:
        if word in words:
            for synonym in words_to_replace[word]:
                reassembled_tweet = ' '.join(words)
                new_tweet = reassembled_tweet.replace(word, synonym)
                new_new_dict['tweet'].append(new_tweet)
                new_new_dict['replies'].append(0)
                new_new_dict['retweets'].append(0)
                new_new_dict['likes'].append(0)
                new_new_dict['ratio'].append(0)
                new_new_dict['result'].append(0)
        
new_new_df = pd.DataFrame(new_new_dict)
new_df = pd.DataFrame(new_dict)

new_df.update(new_new_df)
df.update(new_df)
df = df.drop_duplicates(subset='tweet')

df.to_csv('new data/augmented result.csv', index=False)
print(len(df[df['result']==0]))