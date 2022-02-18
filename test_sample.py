#!/usr/bin/env python
# -*- coding: utf-8 -*-


from modules.tracking import Parcel


if __name__ == "__main__":
    # Création et instanciation de l'objet de type Parcel.
    my_parcel = Parcel("6A21099298277")
    # Appel de la fonction get_formatting_result() de l'objet.
    print(my_parcel.get_table_events())