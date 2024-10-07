from typing import Final, List, Dict, Tuple, Any
from fuzzywuzzy import process
import requests
import re
import os


# Constants
PS_GAMEPASS_URL: Final[str] = (
    "https://www.playstation.com/bin/imagic/gameslist?locale=en-ca&categoryList=plus-games-list"
)

XBOX_GAMEPASS_SHELL_URL: Final[str] = (
    "https://catalog.gamepass.com/sigls/v2?id=09a72c0d-c466-426a-9580-b78955d8173a&language=en-ca&market=CA"
)

XBOX_GAMEPASS_URL_START: Final[str] = (
    "https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds="
)
XBOX_GAMEPASS_URL_END: Final[str] = (
    "&market=CA&languages=en-ca&MS-CV=DGU1mcuYo0WMMp+F.1"
)
API_KEY: str = os.getenv("MY_API_KEY")  # Extracts Api key from environment variable
RAWG_URL: Final[str] = f"https://api.rawg.io/api/games"


def callURL(url: str) -> List[Dict]:
    """Fetch data from the given URL and return JSON response.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        List[Dict]: The JSON response parsed into a list of dictionaries.

    Raises:
        requests.RequestException: If there is an error fetching the data,
                                   a message will be printed to the console.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")


def build_xbox_gamepass_url(first: str, last: str, xbox_gamepass_ids: List[str]) -> str:
    """Build Xbox Game Pass URL with provided IDs.

    Args:
        first (str): The beginning part of the URL.
        last (str): The ending part of the URL.
        xbox_gamepass_ids (List[str]): A list of Xbox Game Pass IDs to include in the URL.

    Returns:
        str: The constructed Xbox Game Pass URL.
    """
    xbox_gamepass_url_ids = ",".join(xbox_gamepass_ids)
    return f"{first}{xbox_gamepass_url_ids}{last}"


def extract_xbox_ids(xbox_gamepass_network_data: str) -> List[str]:
    """Extract Xbox Game Pass game IDs from the given response JSON.

    Args:
        xbox_gamepass_network_data (List[Dict[str, str]]): The JSON response from the Xbox Game Pass API.

    Returns:
        List[str]: A list of extracted Xbox Game Pass IDs.
    """
    xbox_gamepass_id_container: List[Dict[str, str]] = xbox_gamepass_network_data[1:]
    xbox_gamepass_ids: List[str] = []
    xbox_gamepass_ids = [
        list(id_key.values())[0] for id_key in xbox_gamepass_id_container
    ]
    return xbox_gamepass_ids


def extract_xbox_games(xbox_response_json: str) -> List[str]:
    """Extract Xbox Game Pass games from the given response JSON.

    Args:
        xbox_response_json (Dict): The JSON response containing Xbox Game Pass products.

    Returns:
        List[str]: A list of extracted Xbox Game Pass game titles.
    """
    xbox_games: List[str] = []
    for category_list in xbox_response_json["Products"]:
        for game_list in category_list["LocalizedProperties"]:
            xbox_games.append(game_list["ProductTitle"])
    return xbox_games


def extract_ps5_games(ps_response_json: str) -> List[str]:
    """Extract PS5 Game Pass games from the given response JSON.

    Args:
        ps_response_json (List[Dict]): The JSON response containing PS5 game data.

    Returns:
        List[str]: A list of extracted PS5 Game Pass game titles.
    """
    ps5_games: List[str] = []
    for category_list in ps_response_json:
        for game_list in category_list["games"]:
            if "PS5" in game_list["device"]:
                ps5_games.append(game_list["name"])

    return ps5_games


def clean_game_name_with_mapping(game_name: str) -> str:
    """Clean game name using a predefined mapping to remove unwanted text.

    Args:
        game_name (str): The original game name to clean.

    Returns:
        str: The cleaned game name with unwanted parts removed.
    """
    name_corrections = {
        "(PS4 & PS5)": "",
        "PS4® & PS5®": "",
        "PS4 & PS5": "",
        "PS4": "",
        "PS5": "",
        "PS Plus": "",
        "(PlayStation Plus)": "",
        "™": "",
        "®": "",
        "()": "",
        "&": "",
        "【For 】": "",
        "(Game Preview)": "",
        "(Xbox One)": "",
        "(Xbox Series X|S)": "",
        "Xbox Series X|S": "",
        "The Complete Season (Episodes 1-5)": "",
    }

    for key, value in name_corrections.items():
        game_name = game_name.replace(key, value)

    re.sub(r"-\s*$", "", game_name)

    return game_name.strip()


def find_common_games(
    ps5_games: List[str], xbox_games: List[str], threshold: int = 95
) -> List[Tuple[str, str, int]]:
    """
    Find common games between PS5 and Xbox lists using fuzzy matching.

    Args:
    ps5_games (List[str]): A list of PS5 game titles.
    xbox_games (List[str]): A list of Xbox game titles.
    threshold (int): Minimum similarity score for considering a match.

    Returns:
    List[Tuple[str, str, int]]: A list of tuples containing the PS5 game,
                                  matched Xbox game, and their similarity score.
    """

    common_games: List[Tuple[str, str, int]] = []

    for ps5_game in ps5_games:
        # Find the best match for each PS5 game in the Xbox game list
        match, score = process.extractOne(ps5_game, xbox_games)
        if score >= threshold:  # Check if the score is above the threshold
            common_games.append((ps5_game, match, score))

    return common_games


def search_game(game_name: str) -> List[Dict[str, Any]]:
    """
    Search for a game by its name using the RAWG API.

    Args:
        game_name (str): The name of the game to search for.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing game information,
        or an empty list if the request fails or no games are found.
    """
    params = {
        "key": API_KEY,
        "page_size": 1,  # Number of results to return
        "search": game_name,
    }

    try:
        response = requests.get(RAWG_URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        games = response.json()
        return games.get("results", [])

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def main() -> None:
    """Main function to fetch, process, and display game data from PS5 and Xbox Game Pass.

    This function orchestrates the following tasks:
    1. Fetches PS5 game data from the specified URL.
    2. Cleans and processes the PS5 game names.
    3. Fetches Xbox game data from the specified URL.
    4. Cleans and processes the Xbox game names.
    5. Finds and prints common game titles between PS5 and Xbox with similarity scores.
    """
    # Fetch and clean PS5 Game Pass games
    ps_response_json = callURL(PS_GAMEPASS_URL)
    ps5_games = extract_ps5_games(ps_response_json)
    ps5_games = [clean_game_name_with_mapping(ps5_game) for ps5_game in ps5_games]

    # Fetch and process Xbox Game Pass games
    xbox_gamepass_network_data = callURL(XBOX_GAMEPASS_SHELL_URL)
    xbox_gamepass_ids = extract_xbox_ids(xbox_gamepass_network_data)
    xbox_gamepass_url = build_xbox_gamepass_url(
        XBOX_GAMEPASS_URL_START, XBOX_GAMEPASS_URL_END, xbox_gamepass_ids
    )

    xbox_response_json = callURL(xbox_gamepass_url)
    xbox_games = extract_xbox_games(xbox_response_json)
    xbox_games = [clean_game_name_with_mapping(xbox_game) for xbox_game in xbox_games]

    # Find common games between PS5 and Xbox
    common_games = find_common_games(ps5_games, xbox_games)

    # Print out the common games and their similarity scores
    for ps5_game, match, score in com
    mon_games:
        print(
            f"PS5 Game: '{ps5_game}' | Xbox Match: '{match}' | Similarity Score: {score}"
        )


if __name__ == "__main__":
    main()

game_data = search_game("Humans Fall Flat")
print(game_data)
