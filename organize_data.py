import json

# ===================================================================
# organize_data.py will group these prequels into a series name.
# This is used to get more natural twitter search query terms.

# Like people won't search up "Attack on Titan Final Season Part 2".
# They will search up "Attack on Titan"
# ===================================================================

with open("Anime_Names.txt", "r") as f:
        anime_dict = json.load(f)
        print(len(anime_dict))

data = {}

# Groups series with prequels together and returns a list.
def get_prequels(anime_name):
    prequel = anime_dict[anime_name]['prequel']
    prequels = []

    # Checks if the anime has a prequel at all...
    if(prequel != 'None'):
        prequels = []
        prequels.append(prequel)

    else:
        # ... if it doesn't, return an empty list
        return []

    # Loops through the prequels list 10 times.
    for i in range(10):
        try:
            # If the prequel itself has a prequel...
            if(anime_dict[prequels[-1]]['prequel'] != 'None'):
                # ... adds it to the prequel list.
                # (Syntax is clever in that the if statement will always get the last prequel)
                # Returns a list in order of [3rd Season, 2nd Season, 1st Season]
                prequels.append((anime_dict[prequels[-1]]['prequel']))
            else:
                break
        except KeyError:
            break

    return prequels # <-- This is a list

# Loops through all the anime names in the JSON file.
for anime in anime_dict:
    prequels = get_prequels(anime)

    # Completes the series by adding the parent itself
    prequels.insert(0, anime)

    try:
        # Returns in format of {1st season: [then every season after, except for 1st]}
        new_data = {prequels[-1]: prequels[:-1]}

        # If this parent series is not in the new dataset...
        if(prequels[-1] not in data):
            # ... will add it in.
            data.update(new_data)
        else:
            # ... if it is, checks to see if the one already in the list
            # contains the complete series, and replaces accordingly to
            # ensure the parent anime is actually the parent and not a season 2. 
            if(len(new_data) > len(data[prequels[-1]])):
                data.update(new_data)
    # When a series doesn't have a prequel at all...
    except IndexError:
        if anime not in data:
            # ... just returns the anime as the parent with an empty list.
            new_data = {anime: []}
            data.update(new_data)


print(len(data)) # <-- For debug purposes

# 1.2, Isolate the main series name from that group.
# In other words, figures out the series name from each season of a particular anime.
cleaned_data = []
for key, values in data.items():
    # Used to hold words are the same in both the parent series and subsequent sesaons.
    similar_words = []

    # Used to put each word of a name into a list (Ex. Chainsaw Man = ['Chainsaw', 'Man'])
    key_words = []
    for word in key.split():
        key_words.append(word)

    # If the parent series has any prequels...
    if(len(values) != 0):
        for value in values:
            value_words = []
            words = []

            # ... splits the name of the prequels into a list...
            for word in value.split():
                value_words.append(word)

            # ... then checks to see if any words are the same in the parent series.
            # If these words are already accounted for, then don't include them again.
            for word in value_words:
                if (word in key_words and word not in similar_words):
                    similar_words.append(word)

        # Joins the words into a single string.
        new_value = ' '.join(str(e) for e in similar_words)

        # Returns the new string.
        value_data = new_value
    # If the parent has no prequels...
    else:
        # ... just return the parent as the series name.
        value_data = key

    # If the returned string actually doesn't contain anything,
    # Returns the parent as series name
    if (value_data == ''):
        value_data = key
    
    cleaned_data.append(value_data)

# 2. Save new data as a separate file.
# with open("Uncleaned_Names.txt", "w") as outfile:
#         json.dump(data, outfile)

with open("Cleaned_Names.txt", "w") as outfile:
        json.dump(cleaned_data, outfile)