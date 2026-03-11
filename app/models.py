from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    learning_progress = relationship("LearningProgress", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    image_url = Column(String(512))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class LearningProgress(Base):
    __tablename__ = "learning_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(String(100), index=True)  # Identifiant du cours
    progress = Column(Integer, default=0)  # Pourcentage de progression
    completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="learning_progress")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    video_url = Column(String(512))


class LearningItemProgress(Base):
    __tablename__ = "learning_item_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", "item_id", name="uq_learning_item_progress"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(String(100), nullable=False, index=True)
    item_id = Column(String(200), nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String(512), nullable=False)
    prompt_media = Column(String(512))
    prompt_type = Column(String(32), nullable=False, default="gif_to_label")
    answer_index = Column(Integer, nullable=False)
    options = Column(Text, nullable=False)
    category = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
