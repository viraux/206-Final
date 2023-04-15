import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import re
import requests


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur

#find the average runtime for top movies each year
def runtimeByYear(cur): 
    d = {}
    for i in range(2001,2023):
        year_runtime = cur.execute("""SELECT AVG(runtime) FROM movies WHERE year = (?)""",
                                   (i,)).fetchone()[0]
        if year_runtime != None:
            # print(year_runtime)
            d[i] = round(year_runtime,2)
    # print(d)
    return d
    pass

#find the average runtime by genre
def runtimeByGenre(cur):
    d = {}
    total_genres = cur.execute("SELECT genre FROM Genres").fetchall()
    # print(total_genres)
    for i in range(len(total_genres)):
        current_genre = total_genres[i][0]
        # print(current_id,current_genre)
        genre_runtime = cur.execute("""SELECT AVG(movies.runtime) FROM Movies JOIN genres
        ON movies.genre1_id = genres.id  or movies.genre2_id = genres.id or movies.genre3_id = genres.id
        WHERE genres.genre = (?)""",(current_genre,)).fetchone()[0]
        d[current_genre] = round(genre_runtime,2)

    return d
        

    pass

#find the average score by rating
def scoreByRating(cur):
    d = {}
    total_ratings = cur.execute("SELECT rating from Ratings").fetchall()
    # print(total_ratings)
    for i in range(len(total_ratings)):
        current_rating = total_ratings[i][0]
        # print(current_rating)
        rating_score = cur.execute("""SELECT AVG(movies.metacritic_score) FROM Movies JOIN ratings
        ON movies.rating_id = ratings.id WHERE ratings.rating = (?)""",(current_rating,)).fetchone()[0]
        # print(rating_score)
        d[current_rating] = round(rating_score,2)

    return d

    pass


# plot runtime averages found for given years
def plotYear(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for year in data:
        x = year
        y = data[year]
        ax.scatter(x, y, color='k', linewidth=2)

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Runtime")

    fig.savefig("Average_Runtime_by_Year")

    plt.show()
        
        
    pass

# plot runtime averages found for given genres
def plotGenre(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for genre in data:
        x = genre
        y = data[genre]
        ax.barh(x, y, linewidth=2)

    ax.set_ylabel("Genre")
    ax.set_xlabel("Average Runtime")

    fig.savefig("Average_Runtime_by_Genre")

    plt.show()
    pass

# plot score averages for given ratings
def plotRating(data):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for rating in data:
        x = rating
        y = data[rating]
        ax.bar(x, y, linewidth=2)

    ax.set_xlabel("Rating")
    ax.set_ylabel("Average Metacritic Score")

    fig.savefig("Average_Score_by_Rating")

    plt.show()
    pass








def main():
    cur = setUpDatabase("movies.db")
    year_d = runtimeByYear(cur)
    print(year_d)
    plotYear(year_d)

    genre_d = runtimeByGenre(cur)
    print(genre_d)
    plotGenre(genre_d)

    score_d = scoreByRating(cur)
    print(score_d)
    plotRating(score_d)


    pass



main()


# List old resources we used such a HW's?  Don't need to
# Should all our calculations be written to one file?  Can be multiple
#Should one of the visualizations have data from both APIS? Try to have them include both