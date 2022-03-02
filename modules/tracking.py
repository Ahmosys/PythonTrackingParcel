# -*- coding: utf-8 -*-

import os
from modules import utility

import requests

from dotenv import load_dotenv
from tabulate import tabulate

__author__ = "Ahmosys"
__email__ = "ahmosyspro@pm.me"
__licence__ = "MIT"

tabulate.WIDE_CHARS_MODE = False
load_dotenv()


class Parcel():


    def __init__(self, tracking_number = str):
        self.tracking_number = tracking_number


    def get_track_parcel(self):
        """Fonction permettant de retourner les informations d'un colis.

        Returns:
            json: Objet json contenant les informations du colis.
        """
        # Si l'utilisateur n'a pas renseigné l'argument de la fonction.
        if (self.tracking_number is None):
            return "No id provided."
        BASE_URL = "https://api.laposte.fr/suivi/v2/idships/"
        HEADERS = {
            "accept": "application/json", 
            "X-Forwarded-For": utility.get_public_ip(), 
            "X-Okapi-Key": os.getenv("API_KEY_LAPOSTE")
        }
        req = requests.get(f"{BASE_URL}{self.tracking_number}", headers = HEADERS)
        # Si la requête a échouée.
        if (req.status_code != 200):
            return f"Error: {req.json()['returnMessage']}"
        return req.json()

        
    def get_product_name(self):
        """Fonction retournant le type de produit (colissimo, chronopost, lettre suivis).

        Returns:
            string: Type de produit.
        """
        return self.get_track_parcel().get("shipment", []).get("product", "")
        
        
    def get_entry_date(self):
        """Fonction retournant la date où le colis à été pris en charge pour la première fois.

        Returns:
            string: Date d'entrée dans les circuits de livraison du colis.
        """
        return self.get_track_parcel().get("shipment", []).get("entryDate", "")
    
    
    def get_delivery_date(self):
        """Fonction retournant la date de livraison du colis.

        Returns:
            string: Date de livraison du colis.
        """
        return self.get_track_parcel().get("shipment", []).get("deliveryDate", "")
    
    
    def get_table_events(self):
        """Fonction retournant les événements relatif aux colis.

        Returns:
            string: Tableau avec les événements du colis avec leur date.
        """
        events = [["#", "Date 📆", "Description 🎈"]]
        events.extend(
        [event.get("date", None), event.get("label", None)]
        for event in self.get_track_parcel()["shipment"]["event"]
        )
        return tabulate(events, tablefmt = "fancy_grid", showindex = True, headers = "firstrow", missingval = "N/A")


    def get_url(self):
        """Fonction retournant l'url de suivi du colis.

        Returns:
            string: URL vers le suivis du colis sur le site de la poste.
        """
        utility.clear()
        return self.get_track_parcel().get("shipment", []).get("url", "")


    def is_arrived(self):
        """Fonction permettant de savoir si le colis est livré.

        Returns:
            bool: True si le colis est livré, False sinon.
        """
        return self.get_track_parcel().get("shipment", []).get("isFinal", "")


    def get_formatting_result(self):
        return f"""
📦 Informations générales du colis : 

🌟 Type de produit : {self.get_product_name()}
🌟 Date d'entrée : {self.get_entry_date()}
🌟 Date de livraison estimé : {self.get_delivery_date()}
🌟 URL du colis : {self.get_url()}

📦 Événements du colis :

{self.get_table_events()}
    """