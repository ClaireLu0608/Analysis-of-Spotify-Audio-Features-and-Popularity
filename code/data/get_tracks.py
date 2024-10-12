import requests
import time
# from dotenv import load_dotenv
# import os
# import base64
# from pprint import pprint

# def get_access_token(client_id, client_secret):
#     auth_url = 'https://accounts.spotify.com/api/token'
#     auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
    
#     headers = {
#         'Authorization': f'Basic {auth_header}',
#     }
    
#     data = {
#         'grant_type': 'client_credentials'
#     }
    
#     response = requests.post(auth_url, headers=headers, data=data)
#     if response.status_code == 200:
#         token_info = response.json()
#         return token_info['access_token']
#     else:
#         raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")
    

# def get_multiple_playlists_tracks(access_token, playlist_ids):
#     all_tracks_info = [] 

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }

#     for playlist_id in playlist_ids:
#         playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
#         response = requests.get(playlist_url, headers=headers)
        
#         if response.status_code != 200:
#             raise Exception(f"Failed to get playlist tracks for playlist {playlist_id}: {response.status_code}, {response.text}")
        
#         data = response.json()
        
#         for item in data['items']:
        
#             track = item['track']
#             # track_info['id'] = track['id']  
#             # track_id=track.get('id')
#             # if track_id:
#             #     track_info = {}
#             #     track_info['id'] = track['id']  
#             #     track_info['name'] = track['name']
#             #     track_info['artists'] = track['artists'][0]['name']
#             #     track_info['duration (ms)'] = track['duration_ms']
#             #     track_info['popularity'] = track['popularity']
#             #     track_info['url'] = track['preview_url']
#             #     all_tracks_info.append(track_info)
#             # else:
#             #     break
            
#             # all_tracks_info.append(track_info)
#             # track_info = {}
#             # track_info['id'] = track['id']  
#             # track_info['name'] = track['name']
#             # track_info['artists'] = track['artists'][0]['name']
#             # track_info['duration (ms)'] = track['duration_ms']
#             # track_info['popularity'] = track['popularity']
#             # track_info['url'] = track['preview_url']
                
#             # all_tracks_info.append(track_info)
#             # Check if any key data is missing or is None
#         # if (track is None or 
#         #     track.get('id') is None or 
#         #     track.get('name') is None or 
#         #     not track.get('artists') or  # Check if artists list exists and is non-empty
#         #     track['artists'][0].get('name') is None or 
#         #     track.get('duration_ms') is None or 
#         #     track.get('popularity') is None or 
#         #     track.get('preview_url') is None):
#         #     continue  # Skip this track if any of the fields is None

#         # If all required data is present, create track_info dictionary
#         track_info = {}
#         track_info['id'] = track['id']  
#         track_info['name'] = track['name']
#         track_info['artists'] = track['artists'][0]['name']
#         track_info['duration (ms)'] = track['duration_ms']
#         track_info['popularity'] = track['popularity']
#         track_info['url'] = track['preview_url']

#         # Add track_info to all_tracks_info list
#         all_tracks_info.append(track_info)
            
    
#     return all_tracks_info


def get_multiple_playlists_tracks(access_token, playlist_ids):
    all_tracks_info = []  # Store all tracks info

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    for playlist_id in playlist_ids:
        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        params = {
            'limit': 100,  # Retrieve up to 100 tracks per page
        }
        
        while playlist_url:
            response = requests.get(playlist_url, headers=headers, params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to get playlist tracks for playlist {playlist_id}: {response.status_code}, {response.text}")
            
            data = response.json()

            # Loop through all items in the current page of results
            for item in data['items']:
                track = item['track']

                # Skip tracks that have None values in key fields
                if (track is None or 
                    track.get('id') is None or 
                    track.get('name') is None or 
                    not track.get('artists') or  # Check if artists list exists and is non-empty
                    track['artists'][0].get('name') is None or 
                    track.get('duration_ms') is None or 
                    track.get('popularity') is None or 
                    track.get('preview_url') is None):
                    continue  # Skip this track if any of the fields is None

                # If all required data is present, create track_info dictionary
                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artists': track['artists'][0]['name'],
                    'duration (ms)': track['duration_ms'],
                    'popularity': track['popularity'],
                    'url': track['preview_url'],
                }

                # Add track_info to all_tracks_info list
                all_tracks_info.append(track_info)

            # Check if there is a next page (pagination)
            playlist_url = data['next']

            # Add a delay to prevent rate-limiting
            time.sleep(5)

    return all_tracks_info





def get_tracks_audio_features(track_ids, access_token, retries=3):
    batch_size = 50
    all_audio_features = []
    
    for i in range(0, len(track_ids), batch_size):
        batch_ids = track_ids[i:i + batch_size]  
        ids = ','.join(batch_ids)
        url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        for attempt in range(retries):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'audio_features' in data:
                    all_audio_features.extend(data['audio_features'])  
                break  
            elif response.status_code >= 500:
                print(f"Server error {response.status_code}, retrying in 5 seconds...")
                time.sleep(5)  
            else:
                raise Exception(f"Failed to get audio features: {response.status_code}, {response.text}")
    
    return all_audio_features



# def get_access_token(client_id, client_secret):
#     auth_url = 'https://accounts.spotify.com/api/token'
#     auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
    
#     headers = {
#         'Authorization': f'Basic {auth_header}',
#     }
    
#     data = {
#         'grant_type': 'client_credentials'
#     }
    
#     response = requests.post(auth_url, headers=headers, data=data)
#     if response.status_code == 200:
#         token_info = response.json()
#         return token_info['access_token']
#     else:
#         raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")
    


# load_dotenv()

# client_id = os.getenv('SPOTIFY_CLIENT_ID')
# client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# access_token = get_access_token(client_id, client_secret)

# ids=['5muSk2zfQ3LI70S64jbrX7']
# get_multiple_playlists_tracks(access_token, ids)