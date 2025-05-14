import requests


InterfacePath = "https://api.steampowered.com/ISteamNews/"



def GetNewsForApp(app_id:int, api_key:str, count:int=3, max_length:int=300):

    if api_key is None or "":
        raise ValueError("API key is required.")
    if app_id is None or "":
        raise ValueError("App ID is required.")
    validated_app_id = str(app_id)

    response = requests.get(InterfacePath + "GetNewsForApp/v0002/?appid=" + validated_app_id + "&count=" + str(count) + "&maxlength=" + str(max_length) + "&format=json&key=" + api_key)

    return response.json()