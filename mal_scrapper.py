import requests
from bs4 import BeautifulSoup
import re
import json
import time

# =========================================================================
# Scrapes MyAnimeList for a list of English anime names (if possible)
# Script will also put prequels together in a JSON file to create a series.

# organize_data.py will group these prequels into a series name.
# This is used to get more natural twitter search query terms.

# Like people won't search up "Attack on Titan Final Season Part 2".
# They will search up "Attack on Titan"

# So make sure you run it after you get all your anime names,
# Although you can just used mine.
# =========================================================================

try:
    with open("Anime_Names.txt", "r") as f:
        anime_dict = json.load(f)
        anime_number = len(anime_dict)
except FileNotFoundError:
    anime_dict = {}
    anime_number = 0
    
url = "https://myanimelist.net/topanime.php"

pages = 100
names_to_stop = 2500  # When the script should stop after getting a certain amount of anime names.

def get_anime_data(link_to_webpage):
    anime_page = requests.get(link_to_webpage)
    anime_soup = BeautifulSoup(anime_page.content, "html.parser")
    english_tag = "English:"

    # Finds the English name of the anime.
    anime_banner_name = anime_soup.findAll("span", {"class": "dark_text"})

    for language in anime_banner_name:
        anime_banner_name = language

        if language.text == english_tag:
            break

    if(re.search(english_tag, anime_banner_name.parent.text.strip())) != None:
        # Removes empty lines
        cleaned_name = anime_banner_name.parent.text.strip()

        # Removes the "English:" prefix.
        # NOTE: str.strip() doesn't work and results in bugs.
        anime_name = cleaned_name.replace("{} ".format(english_tag), "")
    else:
        anime_name = anime_soup.find("h1", {"class": "title-name h1_bold_none"}).text

    return anime_name, anime_soup


# Gets content from search page on MyAnimeList
with requests.Session() as session:
    limit = anime_number
    try:
        for page in range(pages):
            parameters = {"type": "tv", "limit": limit}
            page = session.get(url, params=parameters)
            soup = BeautifulSoup(page.content, "html.parser")

            anime_section = soup.find("div", {"class": "pb12"})
            animes = anime_section.findChildren("tr", {"class": "ranking-list"})

            for anime in animes:
                data = anime.findChildren("a")[1]
                link = data["href"]

                anime_name, anime_soup = get_anime_data(link)

                # Sees if the anime has a prequel.
                related_anime = anime_soup.findAll('td', {'class': 'ar fw-n borderClass'})

                for item in related_anime:
                    if item.text == 'Prequel:':
                        prequel = item
                        break
                    else:
                        prequel = None

                if prequel != None:
                    prequel_link = "https://myanimelist.net/{}".format(prequel.parent.findChild('a')['href'])
                    prequel_name, prequal_soup = get_anime_data(prequel_link)
                else:
                    prequel_name = 'None'

                limit += 1

                data = {anime_name: {'prequel': prequel_name}}
                anime_dict.update(data)
                
                print("{} | Number: {}".format(anime_name, limit))
                time.sleep(5)

            if(limit >= names_to_stop):
                break

        print("Page Progress #: {}".format(limit/50))

    # You can stop whenever you want by pressing Ctrl + C on the terminal.
    except KeyboardInterrupt:
        pass
    except:
        pass

with open("Anime_Names.txt", "w") as outfile:
        json.dump(anime_dict, outfile)