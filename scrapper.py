from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import json
from cleantext import clean

existing_data = pd.read_csv('new data/best result.csv')

if existing_data is not None:
    tweet_dict = existing_data.to_dict('list')
else:
    tweet_dict = {'tweet': [], 'replies': [], 'retweets': [], 'likes': [], 'ratio': [], 'result':[]}

# We'll use the anime names that I sifted through and edited.
with open("Cleaned_Names (edited).txt", "r") as names:
	anime_names = json.load(names)['cleaned names']

with open("Name Index.txt", "r") as current_index:
    name_index = json.load(current_index)['index']
        

index = 0  # indicator if limit has been reached.
limit = 1000  # limits the amount of tweets scrapped per url.

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe', options=option)
driver.maximize_window()

bottom_counter = 0   # Number of times end of page was reached.
bottom_limit = 3 # Number of times bottom can be hit before going to next URL.
def scroll_down(driver):
    global bottom_counter # Just to make sure we're using the global variable

    total_height = int(driver.execute_script("return window.scrollY"))

    driver.execute_script('window.scrollTo(0, {} + 800)'.format(total_height))

    driver.save_screenshot('screenshot-file-name.png')

    new_height = int(driver.execute_script("return window.scrollY"))

    if(new_height == total_height):
        bottom_counter += 1

    if(bottom_counter == bottom_limit):
        bottom_counter = 0
        return 0

    time.sleep(2)

def calculate_ratio(likes, retweets, replies):
    try:
        ratio = replies / (likes + retweets)
    except ZeroDivisionError:
        ratio = replies / 1
    return ratio

# Turns abbreviated numbers (10K) into full numbers (10000)
def clean_data(data):
    K = '000'     # As in 1000
    M = '000000'  # As in 1000000
    
    try:
        clean_data = int(data.text)
    except ValueError:
        clean_data = int(data.text.replace(',', '').replace('.', '').replace('K', K).replace('M', M))
    except AttributeError:
        clean_data = 0
    
    return clean_data

def make_names_inputable(anime_name):
    need_anime_keyword = re.search(' \[.*?\]', anime_name)

    if need_anime_keyword is None:
        twitter_inputable = anime_name.replace(" ", "%20").replace("&", "and")
        anime_key_inputable = ''
    else:
        twitter_inputable = anime_name.replace(need_anime_keyword.group(0), "").replace(" ", "%20").replace("&", "and")
        anime_key_inputable = need_anime_keyword.group(0).replace("[", "(").replace("]", ")").replace(" ", "%20")

    return twitter_inputable, anime_key_inputable

try:
    for name in anime_names[name_index:]:
        twitter_input, anime_key_input = make_names_inputable(name)

        # URL's that hold information for Twitter Opinions

        # Waits for page to load fully first.
        # This is to ensure any dynamically loaded elements can be scrapped.
        try:
            url = f'https://twitter.com/search?q="{twitter_input}"{anime_key_input}%20-suggestions%20-recs%20-give%20-ideas%20-tell%20-help%20-favorites%20-favourites%20-comment%20-1.%20-mutuals%20-moots%20-%3F%20-commissions%20-10%25%20-recommend%20-recommendations%20-recommendation%20-post%20-posts%20-question%20-reply%20min_replies%3A10%20lang%3Aen%20-filter%3Alinks%20-filter%3Areplies&src=typed_query&f=live'
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[aria-label='Timeline: Search timeline']")))
        except:
            continue


        # Holds past tweets that would be lost from the loop.
        index = 0

        # While-loop is here to limit the amount of tweets scrapped per URL
        while (index <= limit):
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Get scroll height
            #last_height = driver.execute_script("return document.body.scrollHeight")

            # Returns information about the Twitter timeline.
            time.sleep(5)
            tweet_section = soup.find('div', {'aria-label': 'Timeline: Search timeline'})
            # Returns a list of tweets from the twitter timeline.
            tweets = tweet_section.findChildren('div', {'data-testid': 'cellInnerDiv'})

            print("Number of tweets found: {}".format(len(tweets)))

            # Time to look at individual tweets
            for tweet in tweets:
                # If tweets has already been looked at, skip and look for the next one.

                # Finds tweet contents
                try:
                    data = tweet.findChildren('div', {'data-testid': 'tweetText'})[0]
                except IndexError:
                    continue

                description = data.findChildren('span')
                clean_description = clean(''.join([str(elm.text) for elm in description]), no_emoji=True)

                # Skips any tweet with more than 4 lines.
                if clean_description.count('\n') > 4:
                    print('\033[93mSkip\033[0m')
                    continue
                else:
                    clean_description.replace('\n', ' ')

                # Skips any duplicate tweets
                if clean_description in tweet_dict['tweet']:
                    print('\033[94mDuplicate\033[0m')
                    continue

                other_data = tweet.findChildren('span', {'data-testid': 'app-text-transition-container'})
                
                replies = clean_data(other_data[0].findChild('span', {'class': 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'}))
                retweets = clean_data(other_data[1].findChild('span', {'class': 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'}))
                likes = clean_data(other_data[2].findChild('span', {'class': 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'}))
                ratio = calculate_ratio(likes, retweets, replies)

                index += 1

                if index > limit:
                    break

                print('index is now: {}'.format(index))

                accumulated_info = {'tweet': [clean_description], 'replies': [replies], 
                                    'retweets': [retweets], 'likes': [likes], 'ratio': [ratio]}

                if(clean_description not in tweet_dict['tweet']):
                    tweet_dict['tweet'].append(clean_description)
                    tweet_dict['replies'].append(replies)
                    tweet_dict['retweets'].append(retweets)
                    tweet_dict['likes'].append(likes)
                    tweet_dict['ratio'].append(ratio)

                    if(ratio > 1.20):
                        tweet_dict['result'].append(0)
                    else:
                        tweet_dict['result'].append(1)

            # Selenium won't be able to reach the limit in one go (as tweets are dynamically loaded).
            # So, this command will scroll down the twitter timeline virutally
            # in order to load more tweets.
            if(scroll_down(driver) == 0):
                break

            scroll_down(driver)

        print('broke out!')
        name_index += 1
except:
    pass


print(tweet_dict)
print(len(tweet_dict['tweet']))

df = pd.DataFrame(tweet_dict)

df.to_csv('new data/best result.csv', index=False)

with open("Name Index.txt", "w") as outfile:
    out = {"index": name_index}
    json.dump(out, outfile)



