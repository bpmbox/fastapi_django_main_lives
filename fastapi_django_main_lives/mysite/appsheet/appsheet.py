import requests
import json
import os
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
def get_senario(id,res):
    table = "LOG"

    APPSHEET_APPID = os.getenv("APPSHEET_APPID")
    APPSHEET_KEY = os.getenv("APPSHEET_KEY")    
    url = f"https://api.appsheet.com/api/v2/apps/{APPSHEET_APPID}/tables/{table}/Action"

    payload = {
        "Action": "Add", 
        "Properties": {},
        "Rows":[
           {
            "コメント":res,
            "イメージID":"12121",
            "USERNAME":id,
            "ユーザーIMG":"122",
           }
        ]}
    headers = {
        "contentType": "application/json",
        "ApplicationAccessKey": APPSHEET_KEY,
        "Content-Type": "application/json",
    }
    messages = []
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
	#	print(response)
	#print(response)
    for key in response:
        print(key)
    #print(response.text)
    print(response.json)
    return response.text#.json()

# main input
#res = get_senario("LOG")
#print(res)
#return res

#print(response.json())
if __name__ == "__main__":
    get_senario("test","test")