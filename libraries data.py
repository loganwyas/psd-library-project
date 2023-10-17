#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:09:49 2023

@author: tsi2
"""

import random

# Define a list of library names
library_names = ["Pius Library", "Cliff Cave Library", "Main Street Library", "City Central Library",
                 "Oakwood Library", "Maplewood Library", "Riverside Library", "Hillside Library",
                 "West End Library", "Sunnydale Library"]

# Function to generate a random library ID
def generate_random_id():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(8))

# Generate data for at least 10 libraries
libraries = []
for i in range(10):
    library = {
        'id': generate_random_id(),
        'latitude': round(random.uniform(30.0, 40.0), 6),  # Random latitude between 30 and 40 degrees
        'longitude': round(random.uniform(-100.0, -80.0), 6),  # Random longitude between -100 and -80 degrees
        'name': random.choice(library_names)
    }
    libraries.append(library)

# Print the library data
for library in libraries:
    print(f'ID: {library["id"]}, Name: {library["name"]}, Latitude: {library["latitude"]}, Longitude: {library["longitude"]}')
