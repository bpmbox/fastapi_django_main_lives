import requests

def connect_wordpress_rest(url, username, password):
    response = requests.post(f'{url}/wp-json/wp/v2/token', 
                             auth=(username, password))
    if response.status_code == 200:
        token = response.json()
        return token
    else:
        return None
