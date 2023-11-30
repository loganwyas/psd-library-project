#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 12:03:08 2023

@author: tsi2
"""

# global catalog
import json

def load_catalog(filepath):
    """
    Load the catalog from a JSON file.

    :param filepath: Path to the JSON file containing the catalog.
    :return: The loaded catalog.
    """
    with open(filepath, 'r') as file:
        return json.load(file)

global_catalog = load_catalog("/Users/tsi2/Dropbox/Mac (2)/Desktop/library/psd-library-project/DummyData1.json")

# add an item to the catalog
    
def add_item_to_catalog(catalog, title, author, isbn, additional_attribute):
    """
    Add a new item to the global catalog.

    :param catalog: List of dictionaries representing the catalog.
    :param title: Title of the book/item.
    :param author: Author of the book/item.
    :param isbn: ISBN of the book/item.
    :param additional_attribute: Any additional attribute relevant to your catalog.
    """
    # Data validation can be added here (e.g., check for duplicate titles)

    new_item = {
        'title': title,
        'author': author,
        'isbn': isbn,
        'additional_attribute': additional_attribute
    }
    catalog.append(new_item)
    print(f"'{title}' by {author} has been added to the catalog.")

def is_valid_new_item(catalog, title, isbn):
    """
    Check if the new item is valid (not a duplicate).
    """
    for item in catalog:
        if item['title'] == title or item['isbn'] == isbn:
            return False
    return True

add_item_to_catalog(global_catalog, 'New Book', 'New Author', '1112223334445', 'Additional Info')



import json

def save_catalog(catalog, filepath):
    """
    Save the catalog to a JSON file.

    :param catalog: The catalog to be saved.
    :param filepath: Path to the JSON file where the catalog will be saved.
    """
    with open(filepath, 'w') as file:
        json.dump(catalog, file, indent=4)


# After adding items
save_catalog(global_catalog, '/Users/tsi2/Dropbox/Mac (2)/Desktop/library/psd-library-project/DummyData1.json')

