from get_playlists import get_playlists
from get_tracks import get_multiple_playlists_tracks, get_tracks_audio_features

import requests
import base64
from dotenv import load_dotenv
import os
import csv


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_header}',
    }
    
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")
    


def write_data_to_csv(data, path):
    """Write the data to the csv.
    """
    
    with open(path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)




# def get_category_playlists(access_token, category_ids, country='US'):
#     all_playlists = []
    
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }
    
#     for category_id in category_ids:
#         url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists'
#         params = {
#             'country': country,  # Optional, specify a country to get localized playlists
#             'limit': 50          # Max limit is 50 playlists per request
#         }
        
#         response = requests.get(url, headers=headers, params=params)
        
#         if response.status_code == 200:
#             playlists = response.json()['playlists']['items']
#             all_playlists.extend(playlists)  # Collect all playlists
#         else:
#             print(f"Failed to get playlists for category {category_id}: {response.status_code}, {response.text}")
    
#     return all_playlists

def get_category_playlists(access_token, category_ids, playlists_per_category=3, country='US'):
    all_playlists = []
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    for category_id in category_ids:
        url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists'
        params = {
            'country': country # Set the limit to 50 to avoid errors (Spotify allows max 50 per request)
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            playlists = response.json()['playlists']['items']
            # Append up to the specified number of playlists per category (3 in this case)
            all_playlists.extend(playlists[:playlists_per_category])
        else:
            print(f"Failed to get playlists for category {category_id}: {response.status_code}, {response.text}")
    
    return all_playlists


def get_category_playlists(access_token, category_name, country='US'):
    # Set up the endpoint to get playlists for a single category
    url = f'https://api.spotify.com/v1/browse/categories/{category_name}/playlists'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    params = {
        'country': country,  # Optional: specify a country for localized playlists
        'limit': 3           # Only get 3 playlists
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    print(response)
    if response.status_code == 200:
        playlists = response.json()['playlists']['items']
        return playlists
    else:
        raise Exception(f"Failed to get playlists: {response.status_code}, {response.text}")



load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

access_token = get_access_token(client_id, client_secret)







if __name__ == "__main__":
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # popular_categories_csv_path = os.path.join(current_dir, '..', 'artifacts', 'popular_categories.csv')
    # popular_categories_df=pd.read_csv(popular_categories_csv_path)
    
    # popular_categories=popular_categories_df['name'].to_list()
    # popular_categories=[item.lower() for item in popular_categories]

    # all_playlists = get_category_playlists(access_token, popular_categories[3])
    # for playlist in all_playlists:
    
    #     print(f"Category Playlist: {playlist['name']}, URL: {playlist['external_urls']['spotify']}, ID: {playlist['id']}")

# # Display categories
#     for category in categories:
#         print(f"Category ID: {category['id']}, Name: {category['name']}")
    # with open('categories.csv', 'w', newline='') as csvfile:
    #     fieldnames = categories[0].keys()
        
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
    #     writer.writeheader()
        
    #     for track in categories:
    #         writer.writerow(track)
    
    
    query = 'English songs'  
    playlists_id = get_playlists(query, access_token, 50)
    # print(len(playlists_id))
    all_tracks_info=get_multiple_playlists_tracks(access_token, playlists_id)
    
    all_tracks_id=[]
    for track in all_tracks_info:
        all_tracks_id.append(track['id'])  
    # print(len(all_tracks_id))

    all_tracks_features=get_tracks_audio_features(all_tracks_id,access_token)
    
    for i in range(0,len(all_tracks_info)):
        # all_tracks_info[i].update(all_tracks_features[i])
        try:
            print(all_tracks_info[i])
        except IndexError:
            break  # Exit the loop if the index is out of range
        
        if all_tracks_features[i] is not None: 
            all_tracks_info[i].update(all_tracks_features[i])
        else:
            all_tracks_info.remove(all_tracks_info[i])

    current_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(current_dir, '..', '..', 'artifacts')

    CSV_PATH = os.path.join(artifacts_dir, "results.csv")

    os.makedirs(artifacts_dir, exist_ok=True)

    with open(CSV_PATH, 'w', newline='') as csvfile:
        fieldnames = all_tracks_info[0].keys()
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for track in all_tracks_info:
            writer.writerow(track)
        