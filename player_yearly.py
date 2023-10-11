# player_yearly.py
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://www.pro-football-reference.com/players/J/JackLa00/gamelog/'

# Fetch the URL
print("Fetching the URL...")
response = requests.get(url)

# Check if URL fetch was successful
if response.status_code == 200:
    print("Successfully fetched the URL.")
else:
    print(f"Failed to fetch the URL. Status code: {response.status_code}")
    exit(1)

# Parse the HTML
print("Parsing the HTML...")
soup = BeautifulSoup(response.text, 'html.parser')

# Extract rows
print("Extracting rows...")
rows = soup.select('tbody tr:not(.thead)')

# Check if rows were successfully extracted
if rows:
    print(f"Successfully extracted {len(rows)} rows.")
else:
    print("Failed to extract rows.")
    exit(1)

# Prepare an empty list to store rows
data = []

# Columns for the DataFrame
columns = [
    "Rk", "Year", "Date", "G#", "Week", "Age", "Tm", "", "Opp", "Result", "GS",
    "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate", "Sk", "Yds", "Y/A", "AY/A",
    "Att", "Yds", "Y/A", "TD", "TD", "Pts", "Sk", "Solo", "Ast", "Comb", "TFL",
    "QBHits", "Fmb", "FL", "FF", "FR", "Yds", "TD", "Num", "Pct", "Num", "Pct",
    "Num", "Pct", "Status"
]

# Populate data
print("Populating the data...")
for row in rows:
    cells = row.select('td, th')
    if len(cells) > 1:
        row_data = [cell.text for cell in cells]
        row_dict = {}
        
        # Detect 'Inactive' or 'COVID-19 List' and handle specially
        special_statuses = ['Inactive', 'COVID-19 List']
        if any(status in row_data for status in special_statuses):
            detected_status = next(status for status in special_statuses if status in row_data)
            for i in range(len(row_data)):
                row_dict[columns[i]] = row_data[i]
            for i in range(len(row_data), len(columns)):
                row_dict[columns[i]] = detected_status
        else:
            # Loop through each column and assign data accordingly
            for i in range(len(columns)):
                try:
                    row_dict[columns[i]] = row_data[i]
                except IndexError:
                    row_dict[columns[i]] = None  # Use None if data is not available
            
        data.append(row_dict)

# Create DataFrame from the list of dictionaries
print("Creating DataFrame...")
df = pd.DataFrame(data)

# Save DataFrame to CSV
print("Saving data to CSV...")
df.to_csv('full_player_game_stats.csv', index=False, na_rep='N/A')

print("Data saved to 'full_player_game_stats.csv'")




# # # player_yearly.py
# import requests
# import pandas as pd
# import time
# import random
# import json
# from bs4 import BeautifulSoup

# def fetch_player_data(player_suffix):
#     url = f'https://www.pro-football-reference.com/players/{player_suffix[0]}/{player_suffix}/gamelog/'

#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         rows = soup.select('tbody tr:not(.thead)')

#         if rows:
#             data = []
#             columns = [
#                 "Rk", "Year", "Date", "G#", "Week", "Age", "Tm", "", "Opp", "Result", "GS",
#                 "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate", "Sk", "Yds", "Y/A", "AY/A",
#                 "Att", "Yds", "Y/A", "TD", "TD", "Pts", "Sk", "Solo", "Ast", "Comb", "TFL",
#                 "QBHits", "Fmb", "FL", "FF", "FR", "Yds", "TD", "Num", "Pct", "Num", "Pct",
#                 "Num", "Pct", "Status"
#             ]
#             for row in rows:
#                 cells = row.select('td, th')
#                 if len(cells) > 1:
#                     row_data = [cell.text for cell in cells]
#                     row_dict = {}
#                     special_statuses = ['Inactive', 'COVID-19 List']
#                     if any(status in row_data for status in special_statuses):
#                         detected_status = next(status for status in special_statuses if status in row_data)
#                         for i in range(len(row_data)):
#                             row_dict[columns[i]] = row_data[i]
#                         for i in range(len(row_data), len(columns)):
#                             row_dict[columns[i]] = detected_status
#                     else:
#                         for i in range(len(columns)):
#                             try:
#                                 row_dict[columns[i]] = row_data[i]
#                             except IndexError:
#                                 row_dict[columns[i]] = None
#                     data.append(row_dict)
#             return pd.DataFrame(data)
#         else:
#             return None
#     else:
#         return None

# if __name__ == "__main__":
#     with open("active_player_suffixes.json", "r") as f:
#         player_suffixes = json.load(f)

#     all_data_frames = []
#     for player_suffix in player_suffixes:
#         print(f"Fetching data for player {player_suffix}...")
#         df = fetch_player_data(player_suffix)
#         if df is not None:
#             df['PlayerSuffix'] = player_suffix  # Add a new column to identify the player
#             all_data_frames.append(df)
#         time.sleep(random.uniform(5, 10))  # Random sleep between 5 and 10 seconds

#     print("Concatenating all data frames...")
#     final_df = pd.concat(all_data_frames, ignore_index=True)

#     print("Saving data to CSV...")
#     final_df.to_csv('full_player_game_stats.csv', index=False, na_rep='N/A')

#     print("Data saved to 'full_player_game_stats.csv'")





# import json
# import requests
# import time
# import random
# import os
# from bs4 import BeautifulSoup

# def fetch_and_save_player_stats(player_suffix, retry_after=60, max_retries=3):
#     first_letter = player_suffix[0]
#     url = f"https://www.pro-football-reference.com/players/{first_letter}/{player_suffix}.htm"

#     for _ in range(max_retries):
#         print(f"Fetching the URL for player {player_suffix}...")
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             player_data = {}
            
#             name = soup.select_one("h1[itemprop='name']")
#             position = soup.select_one("span[itemprop='jobTitle']")
            
#             if name and position:
#                 player_data['name'] = name.text.strip()
#                 player_data['position'] = position.text.strip()
                
#                 try:
#                     print(f"Current Working Directory: {os.getcwd()}")
#                     with open("player_data.json", "a") as f:
#                         json.dump(player_data, f)
#                         f.write('\n')
#                     print(f"Data written to player_data.json for {player_suffix}")
#                 except Exception as e:
#                     print(f"An error occurred while writing to the file: {e}")
#             else:
#                 print("Failed to extract name and/or position. Skipping this player.")

#             print(f"Data fetched and saved successfully for player {player_suffix}")
#             break

#         elif response.status_code == 429:
#             print(f"Rate limited by the server. Waiting for {retry_after} seconds before retrying...")
#             time.sleep(retry_after)
#             retry_after *= random.uniform(1.1, 1.5)  # Increment retry_after by a random factor between 1.1 and 1.5
#         else:
#             print(f"Failed to fetch the URL for player {player_suffix}. Status code: {response.status_code}")
#             break

# if __name__ == "__main__":
#     try:
#         with open("active_player_suffixes.json", "r") as f:
#             player_suffixes = json.load(f)
#     except Exception as e:
#         print(f"An error occurred while reading the suffixes file: {e}")
#         exit(1)

#     for player_suffix in player_suffixes:
#         fetch_and_save_player_stats(player_suffix)
#         time.sleep(random.uniform(30, 60))  # Random sleep between 30 and 60 seconds





# # player_yearly.py
# import json
# import requests
# import time
# import random
# from bs4 import BeautifulSoup

# def fetch_and_save_player_stats(player_suffix, retry_after=60, max_retries=3):
#     first_letter = player_suffix[0]
#     url = f"https://www.pro-football-reference.com/players/{first_letter}/{player_suffix}.htm"
    
#     for _ in range(max_retries):
#         print(f"Fetching the URL for player {player_suffix}...")
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             player_data = {}
            
#             name = soup.select_one("h1[itemprop='name']")
#             position = soup.select_one("span[itemprop='jobTitle']")
            
#             if name and position:
#                 player_data['name'] = name.text.strip()
#                 player_data['position'] = position.text.strip()
                
#                 with open("player_data.json", "a") as f:
#                     json.dump(player_data, f)
#                     f.write('\n')
                    
#             print(f"Data fetched and saved successfully for player {player_suffix}")
#             break
#         elif response.status_code == 429:
#             print(f"Rate limited by the server. Waiting for {retry_after} seconds before retrying...")
#             time.sleep(retry_after)
#             retry_after *= random.uniform(1.1, 1.5)  # Increment retry_after by a random factor between 1.1 and 1.5
#         else:
#             print(f"Failed to fetch the URL for player {player_suffix}. Status code: {response.status_code}")
#             break

# if __name__ == "__main__":
#     with open("active_player_suffixes.json", "r") as f:  # Changed this line
#         player_suffixes = json.load(f)

#     for player_suffix in player_suffixes:
#         fetch_and_save_player_stats(player_suffix)
#         time.sleep(random.uniform(30, 60))  # Random sleep between 5 and 10 seconds




# import json
# import requests
# import time
# import random
# from bs4 import BeautifulSoup

# def fetch_and_save_player_stats(player_suffix, retry_after=60, max_retries=3):
#     first_letter = player_suffix[0]
#     url = f"https://www.pro-football-reference.com/players/{first_letter}/{player_suffix}.htm"
    
#     for _ in range(max_retries):
#         print(f"Fetching the URL for player {player_suffix}...")
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             player_data = {}
            
#             name = soup.select_one("h1[itemprop='name']")
#             position = soup.select_one("span[itemprop='jobTitle']")
            
#             if name and position:
#                 player_data['name'] = name.text.strip()
#                 player_data['position'] = position.text.strip()
                
#                 with open("player_data.json", "a") as f:
#                     json.dump(player_data, f)
#                     f.write('\n')
                    
#             print(f"Data fetched and saved successfully for player {player_suffix}")
#             break
#         elif response.status_code == 429:
#             print(f"Rate limited by the server. Waiting for {retry_after} seconds before retrying...")
#             time.sleep(retry_after)
#             retry_after *= random.uniform(1.1, 1.5)  # Increment retry_after by a random factor between 1.1 and 1.5
#         else:
#             print(f"Failed to fetch the URL for player {player_suffix}. Status code: {response.status_code}")
#             break

# if __name__ == "__main__":
#     with open("player_suffixes.json", "r") as f:
#         player_suffixes = json.load(f)

#     for player_suffix in player_suffixes:
#         fetch_and_save_player_stats(player_suffix)
#         time.sleep(random.uniform(30, 60))  # Random sleep between 5 and 10 seconds






# import json
# import requests
# import time
# from bs4 import BeautifulSoup

# def fetch_and_save_player_stats(player_suffix):
#     first_letter = player_suffix[0]  # First letter of the player's last name

#     # Correct URL to scrape
#     url = f"https://www.pro-football-reference.com/players/{first_letter}/{player_suffix}.htm"

#     print(f"Fetching the URL for player {player_suffix}...")
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         player_data = {}
        
#         name = soup.select_one("h1[itemprop='name']")
#         position = soup.select_one("span[itemprop='jobTitle']")
        
#         if name and position:
#             player_data['name'] = name.text.strip()
#             player_data['position'] = position.text.strip()

#             # Save data to JSON
#             with open("player_data.json", "a") as f:
#                 json.dump(player_data, f)
#                 f.write('\n')
                
#         print(f"Data fetched and saved successfully for player {player_suffix}")

#     elif response.status_code == 429:
#         print(f"Rate limited by the server. Waiting for {response.headers.get('retry-after', 60)} seconds before retrying...")
#         time.sleep(int(response.headers.get('retry-after', 60)))
#         fetch_and_save_player_stats(player_suffix)

#     else:
#         print(f"Failed to fetch the URL for player {player_suffix}. Status code: {response.status_code}")

# if __name__ == "__main__":
#     # Make sure you have player_suffixes.json with the list of player suffixes
#     with open("player_suffixes.json", "r") as f:
#         player_suffixes = json.load(f)

#     for player_suffix in player_suffixes:
#         fetch_and_save_player_stats(player_suffix)
#         time.sleep(5)  # Adding a delay of 5 seconds between requests








# # player_yearly.py
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# # URL to scrape
# url = 'https://www.pro-football-reference.com/players/J/JackLa00/gamelog/'

# # Fetch the URL
# print("Fetching the URL...")
# response = requests.get(url)

# # Check if URL fetch was successful
# if response.status_code == 200:
#     print("Successfully fetched the URL.")
# else:
#     print(f"Failed to fetch the URL. Status code: {response.status_code}")
#     exit(1)

# # Parse the HTML
# print("Parsing the HTML...")
# soup = BeautifulSoup(response.text, 'html.parser')

# # Extract rows
# print("Extracting rows...")
# rows = soup.select('tbody tr:not(.thead)')

# # Check if rows were successfully extracted
# if rows:
#     print(f"Successfully extracted {len(rows)} rows.")
# else:
#     print("Failed to extract rows.")
#     exit(1)

# # Prepare an empty list to store rows
# data = []

# # Columns for the DataFrame
# columns = [
#     "Rk", "Year", "Date", "G#", "Week", "Age", "Tm", "", "Opp", "Result", "GS",
#     "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate", "Sk", "Yds", "Y/A", "AY/A",
#     "Att", "Yds", "Y/A", "TD", "TD", "Pts", "Sk", "Solo", "Ast", "Comb", "TFL",
#     "QBHits", "Fmb", "FL", "FF", "FR", "Yds", "TD", "Num", "Pct", "Num", "Pct",
#     "Num", "Pct", "Status"
# ]

# # Populate data
# print("Populating the data...")
# for row in rows:
#     cells = row.select('td, th')
#     if len(cells) > 1:
#         row_data = [cell.text for cell in cells]
#         row_dict = {}
        
#         # Detect 'Inactive' or 'COVID-19 List' and handle specially
#         special_statuses = ['Inactive', 'COVID-19 List']
#         if any(status in row_data for status in special_statuses):
#             detected_status = next(status for status in special_statuses if status in row_data)
#             for i in range(len(row_data)):
#                 row_dict[columns[i]] = row_data[i]
#             for i in range(len(row_data), len(columns)):
#                 row_dict[columns[i]] = detected_status
#         else:
#             # Loop through each column and assign data accordingly
#             for i in range(len(columns)):
#                 try:
#                     row_dict[columns[i]] = row_data[i]
#                 except IndexError:
#                     row_dict[columns[i]] = None  # Use None if data is not available
            
#         data.append(row_dict)

# # Create DataFrame from the list of dictionaries
# print("Creating DataFrame...")
# df = pd.DataFrame(data)

# # Save DataFrame to CSV
# print("Saving data to CSV...")
# df.to_csv('full_player_game_stats.csv', index=False, na_rep='N/A')

# print("Data saved to 'full_player_game_stats.csv'")






# works for inactive below and covid and inactive above, this is just a backup just in case.
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# # URL to scrape
# url = 'https://www.pro-football-reference.com/players/J/JackLa00/gamelog/'

# # Fetch the URL
# print("Fetching the URL...")
# response = requests.get(url)

# # Check if URL fetch was successful
# if response.status_code == 200:
#     print("Successfully fetched the URL.")
# else:
#     print(f"Failed to fetch the URL. Status code: {response.status_code}")
#     exit(1)

# # Parse the HTML
# print("Parsing the HTML...")
# soup = BeautifulSoup(response.text, 'html.parser')

# # Extract rows
# print("Extracting rows...")
# rows = soup.select('tbody tr:not(.thead)')

# # Check if rows were successfully extracted
# if rows:
#     print(f"Successfully extracted {len(rows)} rows.")
# else:
#     print("Failed to extract rows.")
#     exit(1)

# # Prepare an empty list to store rows
# data = []

# # Columns for the DataFrame
# columns = [
#     "Rk", "Year", "Date", "G#", "Week", "Age", "Tm", "", "Opp", "Result", "GS",
#     "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate", "Sk", "Yds", "Y/A", "AY/A",
#     "Att", "Yds", "Y/A", "TD", "TD", "Pts", "Sk", "Solo", "Ast", "Comb", "TFL",
#     "QBHits", "Fmb", "FL", "FF", "FR", "Yds", "TD", "Num", "Pct", "Num", "Pct",
#     "Num", "Pct", "Status"
# ]

# # Populate data
# print("Populating the data...")
# for row in rows:
#     cells = row.select('td, th')
#     if len(cells) > 1:
#         row_data = [cell.text for cell in cells]
#         row_dict = {}
        
#         # Detect 'Inactive' and handle specially
#         if 'Inactive' in row_data:
#             # Keep initial fields and set latter part to 'Inactive'
#             for i in range(len(row_data)):
#                 row_dict[columns[i]] = row_data[i]
#             for i in range(len(row_data), len(columns)):
#                 row_dict[columns[i]] = 'Inactive'
#         else:
#             # Loop through each column and assign data accordingly
#             for i in range(len(columns)):
#                 try:
#                     row_dict[columns[i]] = row_data[i]
#                 except IndexError:
#                     row_dict[columns[i]] = None  # Use None if data is not available
            
#         data.append(row_dict)

# # Create DataFrame from the list of dictionaries
# print("Creating DataFrame...")
# df = pd.DataFrame(data)

# # Save DataFrame to CSV
# print("Saving data to CSV...")
# df.to_csv('full_player_game_stats.csv', index=False, na_rep='N/A')

# print("Data saved to 'full_player_game_stats.csv'")



