import requests
from bs4 import BeautifulSoup


def fetch_token():
    url = "https://bit.ly/44E5CYK"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="token")
    token_cell = table.find_all("tr")[1].find("td")  # Second row, first cell

    if not token_cell:
        raise ValueError("Token cell not found in the table.")

    return token_cell.text.strip()

