import requests



InterfacePath = "https://api.steampowered.com/IPlayerService/"



def GetOwnedGames(steam_id:int, api_key:str, include_appinfo:bool=False, include_played_free_games:bool=False):

    if api_key is None or "":
        raise ValueError("API key is required.")
    if steam_id is None or "":
        raise ValueError("Steam ID is required.")
    validated_steam_id = str(steam_id)

    response = requests.get(InterfacePath + "GetOwnedGames/v0001/?key=" + api_key + "&steamid=" + validated_steam_id + "&include_appinfo=" + str(include_appinfo).lower() + "&include_played_free_games=" + str(include_played_free_games).lower() + "&format=json")

    return response.json()

def GetRecentlyPlayedGames(steam_id:int, api_key:str, count:int):

    if api_key is None or "":
        raise ValueError("API key is required.")
    if steam_id is None or "":
        raise ValueError("Steam ID is required.")
    validated_steam_id = str(steam_id)

    response = requests.get(InterfacePath + "GetRecentlyPlayedGames/v0001/?key=" + api_key + "&steamid=" + validated_steam_id + "&count=" + str(count) + "&format=json")

    return response.json()