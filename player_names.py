# player_names.py
import json
import requests
from bs4 import BeautifulSoup

def get_player_suffixes():
    url = "https://www.pro-football-reference.com/players/A/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data with status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    player_suffixes = []
    
    for player in soup.select('p b a'):
        player_path = player['href']
        player_years = player.find_parent().find_parent().text.split(' ')[-1]
        
        if '2023' in player_years:
            player_suffix = player_path.split('/')[-1].split('.')[0]
            player_suffixes.append(player_suffix)
            
    return player_suffixes

if __name__ == '__main__':
    player_suffixes = get_player_suffixes()
    with open("active_player_suffixes.json", "w") as f:
        json.dump(player_suffixes, f)


# all players active and inactive
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import json

# def fetch_player_suffixes(letter):
#     base_url = 'https://www.pro-football-reference.com/players/'
#     url = urljoin(base_url, f"{letter}/")
    
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to fetch URL for letter {letter}. Status code: {response.status_code}")
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     player_links = soup.select('#div_players p > a')
    
#     suffixes = []
#     for link in player_links:
#         suffix = link['href'].split('/')[-1].split('.')[0]
#         suffixes.append(suffix)

#     return suffixes

# if __name__ == "__main__":
#     letters = ['A']  # Extend this list for more letters
#     all_suffixes = []
    
#     for letter in letters:
#         suffixes = fetch_player_suffixes(letter)
#         all_suffixes.extend(suffixes)
    
#     with open('player_suffixes.json', 'w') as f:
#         json.dump(all_suffixes, f)







