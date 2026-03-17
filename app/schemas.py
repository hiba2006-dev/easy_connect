from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Post schemas
class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostCreate(PostBase):
    title: str
    content: str

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: 'UserResponse'
    
    class Config:
        from_attributes = True

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentResponse(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
    author: 'UserResponse'
    
    class Config:
        from_attributes = True

# Learning schemas
class LearningProgressBase(BaseModel):
    course_id: str
    progress: int = 0
    completed: bool = False

class LearningProgressCreate(LearningProgressBase):
    pass

class LearningProgressResponse(LearningProgressBase):
    id: int
    user_id: int
    last_accessed: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Quiz schemas
class QuizQuestionBase(BaseModel):
    prompt: str
    prompt_media: Optional[str] = None
    prompt_type: str = 'gif_to_label'
    answer_index: int
    options: str  # JSON string
    category: Optional[str] = None

class QuizQuestionResponse(QuizQuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityLogBase(BaseModel):
    activity_type: str
    detail: str
    meta_info: Optional[str] = None

class ActivityLogResponse(ActivityLogBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Forward refs
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    UserResponse: BaseModel
    PostResponse: BaseModel

