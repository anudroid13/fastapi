from fastapi import Body, FastAPI, status, HTTPException

from random import randrange

from .models import Post

app = FastAPI()

my_posts = [
        {"id": 1, "title": "First Post", "content": "This is the first post.", "published": True, "rating": 5},
        {"id": 2, "title": "Second Post", "content": "This is the second post.", "published": True, "rating": None}
]

@app.get("/")
def root():
    return {"message": "Welcome to my FASTAPIs!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump();
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"message": "Post created successfully!", "post": post_dict}

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
        
@app.get("/posts/{id}")
def get_post(id: int):
    find_post_result = find_post(id)
    if not find_post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    return {"data": find_post_result}

@app.delete("/posts/{id}")
def delete_post(id: int):
    find_post_result = find_post(id)
    if not find_post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    my_posts.remove(find_post_result)
    return {"message": "Post deleted successfully!", "post": find_post_result}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    find_post_result = find_post(id)
    if not find_post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[my_posts.index(find_post_result)] = post_dict
    return {"data": find_post_result}