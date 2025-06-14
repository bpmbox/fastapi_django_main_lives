import requests

def get_user_profile(user_id, access_token):
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        profile = response.json()
        user_name = profile.get('displayName')
        user_thumbnail = profile.get('pictureUrl')
        return user_name, user_thumbnail
    else:
        print(f"Failed to get user profile: {response.status_code}, {response.text}")
        return None, None