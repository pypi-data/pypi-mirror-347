import requests


InterfacePath = "https://api.steampowered.com/ISteamUser/"



def GetPlayerSummaries(api_key:str, steam_ids:list):

    if steam_ids is None or "":
        raise ValueError("Steam IDs are required.")
    if api_key is None or "":
        raise ValueError("API Key is required.")

    response = requests.get(InterfacePath + "GetPlayerSummaries/v0002/?key=" + api_key + "&steamids=" + str(steam_ids) + "&format=json")

    return response.json()



def GetFriendsList(api_key:str, steam_id:int, relationship:str="friend"):
    if steam_id is None or "":
        raise ValueError("Steam ID is required.")
    if api_key is None or "":
        raise ValueError("API Key is required.")

    validated_steam_id = str(steam_id)

    response = requests.get(InterfacePath + "GetFriendList/v0001/?key=" + api_key + "&steamid=" + validated_steam_id + "&relationship=" + relationship + "&format=json")

    return response.json()

    