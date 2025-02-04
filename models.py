from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SocialMediaUser(BaseModel):
    id: str
    name: str
    profile_pic: Optional[str]

class Comment(BaseModel):
    id: str
    user: SocialMediaUser
    text: str
    created_time: datetime

class Post(BaseModel):
    id: str
    message: str
    created_time: datetime
    comments: List[Comment]

class Page(BaseModel):
    username: str
    name: str
    url: str
    profile_pic: str
    email: Optional[str]
    website: Optional[str]
    category: str
    followers: int
    likes: int
    creation_date: str
    posts: List[Post]