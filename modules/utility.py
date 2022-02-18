import os
import requests

__author__ = "Ahmosys"
__email__ = "ahmosyspro@pm.me"
__licence__ = "MIT"


def clear():
    """Fonction permettant de vider le terminal.
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_public_ip():
    """Fonction permettant de récupérer l'adresse IP publique du client.

    Returns:
        string: Adresse ip du client.
    """
    return requests.get("https://api.ipify.org").content.decode("utf-8")