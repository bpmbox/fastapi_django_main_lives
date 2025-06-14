import requests

def phprunner_create_vector(word,prompt):

    url = "https://kenken999-php.hf.space/api/v1.php"

    payload = f"""model_name={word}&vector_text={prompt}&table=products&action=insert"""
    headers = {
    'X-Auth-Token': 'admin',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'runnerSession=muvclb78zpsdjbm7y9c3; pD1lszvk6ratOZhmmgvkp=13767810ebf0782b0b51bf72dedb63b3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)    
    return True


