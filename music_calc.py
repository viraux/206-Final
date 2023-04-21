import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import requests

# Create database and set up cursor and connection
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur

# Calculate average duration of songs for each year
def durationByYear(cur): 
    d = {}
    for i in range(2001,2023):
        year_duration = cur.execute("""SELECT AVG(duration) FROM Songs WHERE year = (?)""",
                                   (i,)).fetchone()[0]
        if year_duration != None:
            # print(year_runtime)
            d[i] = round(year_duration,2)
    # print(d)
    return d


# Calculate percent difference in duration based on first year
def percentDif(data):
    d = {}
    items = list(data.items())
    for i in range(len(items)):
        pair = items[i]
        # print(pair[0])
        if i == 0:
            d[pair[0]] = 1
            pass
        # print(items[i])
        else:
            prev_pair = items[0]
            # prev_pair = items[i-1]
            dif = pair[1] - prev_pair[1]
            percentage = dif / (prev_pair[1])
            # print(percentage)
            d[pair[0]] = round(percentage,2) + 1

    # print(d)
    return d


# Plots values for average duration for each year
def plotYear(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x_list = []
    y_list = []
    for year in data:
        x = year
        y = data[year]
        x_list.append(x)
        y_list.append(y)
        ax.scatter(x, y, color='k', linewidth=2)

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='red')

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Duration")
    ax.set_title("Average Song Duration by Year Over Time")


    fig.savefig("Average_Duration_by_Year")

    plt.show()


# Plots values for average percent change in duration for each year
def plotPercent(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x_list = []
    y_list = []
    for year in data:
        x = year
        y = data[year]
        x_list.append(x)
        y_list.append(y)
        ax.scatter(x, y, color='k', linewidth=2)

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    a, b = np.polyfit(x_list, y_list, 1)
    plt.plot(x_list, a*x_list+b, color='blue')

    ax.set_xlabel("Year")
    ax.set_ylabel("Percent Change in Average Duration")
    ax.set_title("Percent Change in Average Song Duration (based on first year)")


    fig.savefig("Percent_Average_Duration_by_Year")

    plt.show()


# Write the calculated data to a json file
def writeData(data_l):
    final_d = {}
    final_d["year_data"] = {}
    for d in data_l:
        keys = list(d.keys())
        if d[keys[0]] == 1:
            final_d["year_data"]["percent_change"] = d
            pass
        else:
            final_d["year_data"]["avg_duration"] = d
            pass
        
    with open("songs.json","w") as f:
        json.dump(final_d,f, indent=2)


    pass

# Calls all calculation files, plots the data, and the writes the data
def main():
    data_l = []
    cur = setUpDatabase("final.db")
    year_d = durationByYear(cur)
    print(year_d)
    data_l.append(year_d)
    percent_d = percentDif(year_d)
    data_l.append(percent_d)
    # print(percent_d)
    plotPercent(percent_d)
    plotYear(year_d)

    writeData(data_l)

    


    pass



main()