from fastapi import FastAPI, HTTPException, Query
from scraper import scrape_facebook_page
from db import save_page_to_db, get_page_from_db
from models import Page

app = FastAPI()

@app.get("/pages/{username}", response_model=Page)
async def get_page(username: str):
    # Check if page exists in DB
    page = get_page_from_db(username)
    if not page:
        # Scrape and save to DB
        page_data = scrape_facebook_page(username)
        save_page_to_db(page_data)
        page = page_data
    return page

@app.get("/pages")
async def get_pages(
    category: str = None,
    min_followers: int = None,
    max_followers: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    query = {}
    if category:
        query["category"] = category
    if min_followers and max_followers:
        query["followers"] = {"$gte": min_followers, "$lte": max_followers}
    
    pages = list(get_page_from_db(query).skip(skip).limit(limit))
    return pages

@app.get("/pages/{username}/followers")
async def get_followers(username: str):
    page = get_page_from_db(username)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.get("followers", [])

@app.get("/pages/{username}/posts")
async def get_recent_posts(username: str, limit: int = 10):
    page = get_page_from_db(username)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    posts = page.get("posts", [])[:limit]
    return posts