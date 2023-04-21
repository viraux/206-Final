import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import re
import requests

# Create database and set up cursor and connection
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Create Songs table to add to if it does not exist
def createTables(cur,conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS Songs
    (id INTEGER PRIMARY KEY UNIQUE, name TEXT, year INTEGER, duration INTEGER)""")

    conn.commit()

# Go through 25 data items given a given index and year
def collectData(sp, year, index):
    end = index + 25
    results = sp.search(q=f'year:{year}',type='track', limit=50)
    data_l = []
    # print(results)
    for track in results['tracks']['items'][index:end]:
        # print(track)
        name = track["name"].strip()
        duration = track["duration_ms"]
        year = int(track['album']["release_date"][:4].strip())
        data_l.append((name,year,duration))

    return data_l

# update the Songs table with 25 pieces of collected data
def updateMainTable(cur,conn,data_l):
    for data in data_l:
        # print(formatted_data)

        cur.execute("""INSERT OR IGNORE INTO Songs (name, year, duration) VALUES (?,?,?)
        """,(data))

        conn.commit()



def main():
    # Create connection to spotify API with spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="9e43dbbe8a254c218b7cc2aec2dc1d2b",
                                                           client_secret="2567b0ec45c14442a2bfc6ea3446b5e3"))
    cur, conn = setUpDatabase("final.db")
    createTables(cur, conn)
    
    # Prompt user for input until a valid one is entered or -1 is entered to stop program without adding
    # Also keeps track of index to use and year to search
    while True:
        try:
            user_year = int(input("""Please input a year between 2001 and 2022 to add 25 songs from (type "-1" to end code). """))
            if user_year == -1:
                ("Ending Program")
                return None
            if user_year > 2000 and user_year < 2023:
                amount_from_year = cur.execute("""SELECT year FROM Songs WHERE
                year = (?)""",(user_year,)).fetchall()
                # print(amount_from_year)
                index = len(amount_from_year)
                if index > 25:
                    print("You have the maximum data for this year, choose another please")
                else:
                    year = user_year
                    break
            else:
                print("Invalid Year, please try again")
        except:
            print(1)
            print("Invalid Year, please try again")

    data_l = collectData(sp, year, index)
    # data_l = collectData(api_key, 2018, 0)
    # print(data_l)

    updateMainTable(cur,conn,data_l)



    pass



main()