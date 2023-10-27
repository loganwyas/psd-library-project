#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:27:28 2023

@author: tsi2
"""

import tkinter as tk
from tkinter import ttk


import json

with open("/Users/tsi2/Dropbox/Mac (2)/Desktop/library/psd-library-project/DummyData1.json", "r") as f:
    dummy_data = json.load(f)

def add_item(category, title, author, release):
    new_id = max([item["id"] for item in dummy_data[category]]) + 1
    new_item = {
        "id": new_id,
        "title": title,
        "author": author,
        "release": release
    }
    dummy_data[category].append(new_item)


def on_submit():
    category = category_combobox.get()
    title = title_entry.get()
    author = author_entry.get()
    release = int(release_entry.get())
    add_item(category, title, author, release)

root = tk.Tk()
root.title("Library Management")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

category_label = ttk.Label(frame, text="Category:")
category_label.grid(row=0, column=0)
category_combobox = ttk.Combobox(frame, values=["Books", "Movies", "Video Games"])
category_combobox.grid(row=0, column=1)
category_combobox.current(0)

title_label = ttk.Label(frame, text="Title:")
title_label.grid(row=1, column=0)
title_entry = ttk.Entry(frame)
title_entry.grid(row=1, column=1)

author_label = ttk.Label(frame, text="Author:")
author_label.grid(row=2, column=0)
author_entry = ttk.Entry(frame)
author_entry.grid(row=2, column=1)

release_label = ttk.Label(frame, text="Release:")
release_label.grid(row=3, column=0)
release_entry = ttk.Entry(frame)
release_entry.grid(row=3, column=1)

submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=4, columnspan=2)

root.mainloop()
