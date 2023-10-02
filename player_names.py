import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def fetch_player_suffixes(letter):
    base_url = 'https://www.pro-football-reference.com/players/'
    url = urljoin(base_url, f"{letter}/")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL for letter {letter}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    player_links = soup.select('#div_players p > a')
    
    suffixes = []
    for link in player_links:
        suffix = link['href'].split('/')[-1].split('.')[0]
        suffixes.append(suffix)

    return suffixes

if __name__ == "__main__":
    letters = ['A']  # Extend this list for more letters
    all_suffixes = []
    
    for letter in letters:
        suffixes = fetch_player_suffixes(letter)
        all_suffixes.extend(suffixes)
    
    with open('player_suffixes.json', 'w') as f:
        json.dump(all_suffixes, f)




# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# def fetch_player_suffixes(letter):
#     base_url = 'https://www.pro-football-reference.com/players/'
#     url = urljoin(base_url, f"{letter}/")
    
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to fetch URL for letter {letter}. Status code: {response.status_code}")
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Update the selector based on the HTML structure you shared
#     player_links = soup.select('#div_players p > a')
    
#     suffixes = []
#     for link in player_links:
#         suffix = link['href'].split('/')[-1].split('.')[0]
#         suffixes.append(suffix)

#     return suffixes

# if __name__ == "__main__":
#     # Get player suffixes for players whose names start with 'A' as an example
#     letters = ['A']  # You can extend this to include other letters
#     all_suffixes = []
    
#     for letter in letters:
#         suffixes = fetch_player_suffixes(letter)
#         all_suffixes.extend(suffixes)

#     print(f"Collected {len(all_suffixes)} player URL suffixes.")
#     print("Sample suffixes:", all_suffixes[:5])




