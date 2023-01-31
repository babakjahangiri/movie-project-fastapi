from fastapi import FastAPI
from dotenv import load_dotenv
import json
from connection import myConnection
import mysql.connector

load_dotenv()
app = FastAPI()
mydb = myConnection()
mycursor = mydb.cursor()


@app.get("/")
async def root():
    return {"Application name": "Movie Project", "OPEN API Doc": "Browse /docs"}


@app.get("/movies")
async def get_movies():
    query = "SELECT id_movies,title,year,storyline FROM tbl_movies"
    mycursor.execute(query)
    movies = mycursor.fetchall()
    new_movies = []
    time_keys = ("id_movies", "title", "year", "storyline")

    for item in movies:
        new_item = dict((x, y) for x, y in zip(time_keys, item))
        new_movies.append(new_item)

    return new_movies


@app.get("/movie/{id}")
async def get_movie(id: int):
    query = "SELECT id_movies,title,year,storyline FROM tbl_movies WHERE id_movies = %s"
    value = (id,)
    try:
        mycursor.execute(query, value)
        movie = mycursor.fetchall()
        if not len(movie) == 0:
            return movie
        else:
            return {"err": "moive not found"}

    except mysql.connector.Error as err:
        return {"err": err}


@app.delete("/movie/{id}")
async def remove_movie(id: int):
    query = "DELETE FROM tbl_movies WHERE id_movies = %s"
    values = (id,)
    mycursor.execute(query, values)
    mydb.commit()
    return {"err": "moive has deleted"}


@app.post("/movie/")
async def create_movie(movie: dict):
    query = "INSERT INTO tbl_movies (title, year, storyline) VALUES (%s,%s,%s)"
    values = (movie["title"], movie["year"], movie["storyline"])
    mycursor.execute(query, values)
    mydb.commit()
    return {"msg": "moive has added"}


@app.put("/movie/")
async def update_movie(id: int, new_movie: dict):
    query = "UPDATE tbl_movies SET title = %s , year = %s , storyline = %s WHERE id_movies = %s"
    values = (new_movie["title"], new_movie["year"], new_movie["storyline"], id)
    print(query)
    mycursor.execute(query, values)
    mydb.commit()
    return {"msg": "moive updated"}


# uvicorn main:app --reload
