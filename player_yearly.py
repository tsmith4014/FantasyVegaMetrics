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







# backup file just ignore this works for inactive and covid and inactive this is just a backup just in case.
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

