from fastapi import Body, FastAPI, status, HTTPException
from random import randrange

from .models import Post
from .database import cursor, conn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my FASTAPIs!"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts) 
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                    (post.title, post.content, post.published))        
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post created successfully!", "post": new_post}
        
@app.get("/posts/{id}")
def get_post(id: int):
    find_post_result = find_post(id)
    return {"data": find_post_result}

@app.delete("/posts/{id}")
def delete_post(id: int): 
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post deleted successfully!", "post": deleted_post}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    return {"data": updated_post}

def find_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if post:
        return post
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")