import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests
import getpass

if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent.absolute()
else:
    base_path = Path(__file__).parent.absolute()

config_path = base_path / "config.txt"
load_dotenv(dotenv_path=config_path)

# Load the API key from env var
API_KEY = os.getenv("API_KEY")
API_URL = "http://vm.deklenn.dev:8000"

if not API_KEY:
    print(f"DEBUG: I am looking for the .env file at: {config_path.absolute()}")
    print("ERROR: API_KEY not found. Ensure the .env file is in the same folder.")
    input("Press Enter to exit...")
    sys.exit()

HEADERS = {
    'X-API-Key': API_KEY
}

# Registers a new user with the API
def register_user(username: str, password: str):
    url = API_URL + "/users/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Logs in a user and requests an access token
def login(username, password):
    url = API_URL + "/users/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(response.text)
        return None


# Sends an add card request to API
def add_card(text: str, quantity: int = 1):
    url = API_URL + "/import/card"
    payload = {"text": text, "quantity": quantity}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Sends a move card request to API
def trade_card(text: str, to_username: str, quantity: int = 1):
    url = API_URL + "/trade/card"
    payload = {"text": text, "to_username": to_username, "quantity": quantity}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Sends a remove card request to API
def remove_card(text: str, quantity: int = 1):
    url = API_URL + "/remove/card"
    payload = {"text": text, "quantity": quantity}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Sends a bulk add card request to API
def add_bulk(cards: list):
    url = API_URL + "/import/bulk"
    payload = {"cards": cards}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Sends a bulk move card request to API
def trade_bulk(cards: list, to_username: str):
    url = API_URL + "/trade/bulk"
    payload = {"cards": cards, "to_username": to_username}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Sends a bulk remove card request to API
def remove_bulk(cards: list):
    url = API_URL + "/remove/bulk"
    payload = {"cards": cards}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Requests the user's inventory from the API
def fetch_inventory():
    url = API_URL + "/inventory/user"
    response = requests.get(url, headers=HEADERS)
    return response.json()

username = input("Enter username: ")
password = getpass.getpass("Password: ")

user_token = login(username, password)

if user_token:

    # Implement token
    HEADERS["Authorization"] = f"Bearer {user_token}"

    running = True
    while running:
        command = input("\nEnter a command (fetch, add, remove, move, exit): ").strip().lower()
        if command == "fetch":
            inventory = fetch_inventory()
            print("Your inventory:")
            card_list = inventory.get("inventory", [])
            if not card_list:
                print("Your inventory is empty.")
            else:
                for card in card_list:
                    name = card.get('card_name', 'Unknown Card')
                    qty = card.get('quantity', 0)
                    print(f"{name} x{qty}")
        elif command == "add":
            text = input("Enter card name: ")
            try:
                quantity = int(input("Enter quantity: "))
                result = add_card(text, quantity)
                print(result)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif command == "remove":
            text = input("Enter card name: ")
            try:
                quantity = int(input("Enter quantity: "))
                result = remove_card(text, quantity)
                print(result)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif command == "move":
            text = input("Enter card name: ")
            to_username = input("Enter username to move card to: ")
            try:
                quantity = int(input("Enter quantity: "))
                result = trade_card(text, to_username, quantity)
                print(result)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif command == "exit":
            running = False
        else:
            print("Unknown command")
else:
    print("Invalid login.")