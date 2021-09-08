#!/usr/bin/python3

# Copyright (C) 2021 Adam Williamson
#
# This file is part of watacheck.
#
# watacheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The GPL can be found at <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <adam@blueradius.ca>

"""Trivial script for dumping graded game population data from the WATA
API. Credit to inasuma for finding the relevant API endpoint.
"""

import requests
import sys

def get_response_list(prompt, items, start=0):
    """Given a question and an iterable of strings, number the strings
    and ask the user which they want. Returns the int for the user's
    selection.
    """
    lines = []
    for (num, item) in enumerate(items, start):
        lines.append(f"{num})  {item}")
    lines.append(prompt)
    prompt = '\n'.join(lines)
    accepted = [str(num) for num in range(start, len(items)+start)]
    resp = input(prompt)
    while not resp.lower() in accepted:
        print(f"Invalid response. Pick a number between {start} and {str(len(items)+start)}")
        resp = input(prompt)
    return int(resp.lower())

platforms = requests.get("https://api.watagames.com/api/platform").json()["data"]
platforms.sort(key=lambda x:x["id"])
prompt = "Select platform: "
answer = get_response_list(prompt, [plat["name"] for plat in platforms], 1)
platform = platforms[answer - 1]["id"]
name = input("Enter game name: ")

resp = requests.get(f"https://api.watagames.com/api/game?name={name}&page=1&size=20&platformId={platform}").json()
if resp["count"] == 0:
    sys.exit("No game found!")
if resp["count"] == 1:
    game = resp["data"][0]
else:
    games = resp["data"]
    prompt = "Select game: "
    answer = get_response_list(prompt, [game["name"] for game in games], 1)
    game = games[answer - 1]
print(f"Game: {game['name']}")
print("")

boxes = sorted([var for var in game["variants"] if var["type"] == 1], key=lambda x: x["count"], reverse=True)
numboxes = sum(box["count"] for box in boxes)
carts = sorted([var for var in game["variants"] if var["type"] == 2], key=lambda x: x["count"], reverse=True)
numcarts = sum(cart["count"] for cart in carts)
manuals = sorted([var for var in game["variants"] if var["type"] == 3], key=lambda x: x["count"], reverse=True)
nummanuals = sum(manual["count"] for manual in manuals)
seals = sorted([var for var in game["variants"] if var["type"] == 6], key=lambda x: x["count"], reverse=True)
numseals = sum(seal["count"] for seal in seals)

print(f"Boxes (total {numboxes}):")
print("")
for box in boxes:
    print(f"{box['count']}: {box['name']}")
print("")
print(f"Seals (total {numseals}):")
print("")
for seal in seals:
    print(f"{seal['count']}: {seal['name']}")
print("")
print(f"Carts (total {numcarts}):")
print("")
for cart in carts:
    print(f"{cart['count']}: {cart['name']}")
print("")
print(f"Manuals (total {nummanuals}):")
print("")
for manual in manuals:
    print(f"{manual['count']}: {manual['name']}")
