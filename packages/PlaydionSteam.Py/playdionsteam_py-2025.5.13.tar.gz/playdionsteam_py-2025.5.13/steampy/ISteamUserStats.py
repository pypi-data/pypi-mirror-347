import requests


InterfacePath = "https://api.steampowered.com/ISteamUserStats/"


def GetGlobalAchievementPercentagesForApp(app_id:int):
    if app_id is None or "":
        raise ValueError("App ID is required.")
    validated_app_id = str(app_id)

    response = requests.get(InterfacePath + "GetGlobalAchievementPercentagesForApp/v0002/?gameid=" + validated_app_id + "&format=json")

    return response.json()




def GetPlayerAchievements(steam_id:int, app_id:int, api_key:str, language:str="en"):

    if steam_id is None or "":
        raise ValueError("Steam ID is required.")
    if app_id is None or "":
        raise ValueError("App ID is required.")
    if api_key is None or "":
        raise ValueError("API Key is required.")

    validated_steam_id = str(steam_id)
    validated_app_id = str(app_id)

    response = requests.get(InterfacePath + "GetPlayerAchievements/v0001/?appid=" + validated_app_id + "&key=" + api_key + "&steamid=" + validated_steam_id + "&format=json&l=" + language)

    return response.json()



def GetUserStatsForGame(steam_id:int, app_id:int, api_key:str, language:str="en"):

    if steam_id is None or "":
        raise ValueError("Steam ID is required.")
    if app_id is None or "":
        raise ValueError("App ID is required.")
    if api_key is None or "":
        raise ValueError("API Key is required.")

    validated_steam_id = str(steam_id)
    validated_app_id = str(app_id)

    response = requests.get(InterfacePath + "GetUserStatsForGame/v0002/?appid=" + validated_app_id + "&key=" + api_key + "&steamid=" + validated_steam_id + "&format=json&l=" + language)

    return response.json()