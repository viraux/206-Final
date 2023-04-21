import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import requests

# Plot the percent difference for both movies and songs data
def plotPercent(movies,songs):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x_list = []
    y_list = []
    count = 1
    for year in movies:
        x = int(year)
        y = movies[year]
        x_list.append(x)
        y_list.append(y)
        if count == 1:
            ax.scatter(x, y, color='green', linewidth=2,marker="x",label="Movies")
            count +=1
        ax.scatter(x, y, color='green', linewidth=2,marker="x")

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='blue',label="Movie Trendline")

    x_list = []
    y_list = []
    count = 1
    for year in songs:
        x = int(year)
        y = songs[year]
        x_list.append(x)
        y_list.append(y)
        if count == 1:
            ax.scatter(x, y, color='orange', linewidth=2, marker="+",label="Songs")
            count +=1
        ax.scatter(x, y, color='orange', linewidth=2, marker="+")

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='red',label="Song Trendline")

    ax.set_xlabel("Year")
    ax.set_ylabel("Percent Change in Average Runtime/Duration")
    ax.set_title("Percent Change in Average Song Duration vs Percent Change in Average Movie Runtime (based on first year)")
    ax.legend()

    fig.savefig("Percent_Mixed_by_Year")

    plt.show()
    pass



# Opens both data files and loads them in with json.  Then calls function to plot data
def main():

    movies = open(f"{os.path.dirname(os.path.abspath(__file__))}/movies.json")

    movie_data = json.load(movies)["year_data"]["percent_change"]

    songs = open(f"{os.path.dirname(os.path.abspath(__file__))}/songs.json")

    song_data = json.load(songs)["year_data"]["percent_change"]

    print(movie_data,song_data)

    plotPercent(movie_data,song_data)



    movies.close()

    songs.close()
                  

    pass


main()