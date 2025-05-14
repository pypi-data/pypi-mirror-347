from pathlib2 import Path


SteamApiKey = ""



def set_api_key(api_key):
    global SteamApiKey
    if not isinstance(api_key, str):
        raise ValueError("API key must be a string.")
    if api_key is None or "":
        raise ValueError("API key cannot be empty.")
    else:
        SteamApiKey = api_key
        with open("apikey.txt", "w") as file:
            file.write(SteamApiKey)



def get_api_key():
    global SteamApiKey
    if SteamApiKey is None or "":
        raise ValueError("API key not set. Please set it before using.")
    else:
        if Path("apikey.txt").exists():
            with open("apikey.txt", "r") as file:
                SteamApiKey = file.read()
            return SteamApiKey
        else:
            raise ValueError("API key file not found. Please set the API key first.")

