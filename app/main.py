from random import randint
from typing import Optional
from fastapi import FastAPI, Response, HTTPException
from fastapi import status
from fastapi.params import Body
import psycopg.rows
from pydantic import BaseModel
import psycopg
import time


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True  # it has default values as true, hence it is optional


for i in range(5):
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi user=postgres password=postgres")
        cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
        print("Connection was successful")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
app = FastAPI()

my_posts = [{"title": "GOAT Dev", "content": "RP Dev", "id": 1},
            {"title": "GOAT Trader", "content": "SM Trader", "id": 2}]


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    my_posts = []
    cursor.execute("SELECT * FROM posts")
    records = cursor.fetchall()
    return {"posts": records}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    # payload here is object of pydantic model
    post_dict = payload.model_dump()
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post_dict["title"], post_dict["content"], post_dict["publish"]))
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(post_id),))
    post = cursor.fetchone()
    if not post:
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"error": "Post not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    return {"post": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute(
        "DELETE FROM posts WHERE id = %s returning *", (str(post_id),))
    del_post = cursor.fetchone()

    if not del_post:
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"error": "Post not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("Update posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
                                    (post.title, post.content, post.publish, id))
    post_to_update = cursor.fetchone()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    conn.commit()
    return {"post": post_to_update}


def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
