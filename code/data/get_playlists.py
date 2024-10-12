import requests


def get_playlists(query, access_token, limit=10):
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=playlist&limit={limit}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        playlists_data = response.json()
    else:
        raise Exception(f"Failed to search playlists: {response.status_code}, {response.text}")
    
    playlists_id = []
    for playlist in playlists_data['playlists']['items']:
        playlist_id = playlist['id']
        playlists_id.append(playlist_id)
    
    return playlists_id