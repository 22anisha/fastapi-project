from fastapi import APIRouter, HTTPException
from models import Post

router = APIRouter()

posts = []

MAX_POSTS = 5

@router.post("/posts/")
async def create_post(post: Post):
    
    if len(posts) >= MAX_POSTS:
        raise HTTPException(status_code=400, detail="Cannot create more than 5 posts.")

    
    if any(p['title'] == post.title for p in posts):
        raise HTTPException(status_code=400, detail="Post with this title already exists.")
    

    posts.append(post.dict())

    
    numbered_list = [
        {"number": idx + 1, "title": p['title'], "content": p['content'], "author": p['author']}
        for idx, p in enumerate(posts)
    ]
    
    
    return {
        "numbered_list": numbered_list,
        "detailed_list": posts
    }

@router.get("/posts/")
async def get_posts():
    
    numbered_list = [
        {"number": idx + 1, "title": p['title'], "content": p['content'], "author": p['author']}
        for idx, p in enumerate(posts)
    ]
    return {
        "numbered_list": numbered_list,
        "detailed_list": posts
    }

@router.put("/posts/{title}")
async def update_post(title: str, post: Post):
   
    for idx, p in enumerate(posts):
        if p['title'] == title:
            # Update the post details
            posts[idx] = post.dict()
            return post
    
    
    raise HTTPException(status_code=404, detail="Post not found.")

@router.delete("/posts/{title}")
async def delete_post(title: str):
    
    for idx, p in enumerate(posts):
        if p['title'] == title:
            del posts[idx]
            return {"message": f"Post '{title}' deleted successfully."}
    
    
    raise HTTPException(status_code=404, detail="Post not found.")
