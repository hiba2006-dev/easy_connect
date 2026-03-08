from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.database import engine, get_db
import app.models as models
import app.auth as auth
from app.routers import users, community, learning


def migrate_legacy_mysql_schema() -> None:
    # Keep existing MySQL data compatible with current SQLAlchemy models.
    if engine.dialect.name != "mysql":
        return

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing_columns = {col["name"] for col in inspector.get_columns("users")}

    with engine.begin() as conn:
        if "username" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(100) NULL"))
        if "full_name" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN full_name VARCHAR(255) NULL"))
        if "hashed_password" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR(255) NULL"))
        if "is_active" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE"))

        if "name" in existing_columns:
            conn.execute(
                text(
                    "UPDATE users "
                    "SET username = COALESCE(NULLIF(username, ''), name) "
                    "WHERE username IS NULL OR username = ''"
                )
            )
        if "password" in existing_columns:
            conn.execute(
                text(
                    "UPDATE users "
                    "SET hashed_password = COALESCE(NULLIF(hashed_password, ''), password) "
                    "WHERE hashed_password IS NULL OR hashed_password = ''"
                )
            )

    # Posts table migration (legacy schema used user_id and no title/updated_at).
    if "posts" in inspector.get_table_names():
        post_columns = {col["name"] for col in inspector.get_columns("posts")}
        with engine.begin() as conn:
            if "title" not in post_columns:
                conn.execute(text("ALTER TABLE posts ADD COLUMN title VARCHAR(255) NULL"))
            if "author_id" not in post_columns:
                conn.execute(text("ALTER TABLE posts ADD COLUMN author_id INT NULL"))
            if "updated_at" not in post_columns:
                conn.execute(text("ALTER TABLE posts ADD COLUMN updated_at DATETIME NULL"))
            if "user_id" in post_columns:
                conn.execute(
                    text(
                        "UPDATE posts "
                        "SET author_id = COALESCE(author_id, user_id) "
                        "WHERE author_id IS NULL"
                    )
                )
            conn.execute(
                text(
                    "UPDATE posts "
                    "SET title = COALESCE(NULLIF(title, ''), 'Publication') "
                    "WHERE title IS NULL OR title = ''"
                )
            )

    # Comments table migration safety.
    if "comments" in inspector.get_table_names():
        comment_columns = {col["name"] for col in inspector.get_columns("comments")}
        with engine.begin() as conn:
            if "author_id" not in comment_columns and "user_id" in comment_columns:
                conn.execute(text("ALTER TABLE comments ADD COLUMN author_id INT NULL"))
                conn.execute(text("UPDATE comments SET author_id = user_id WHERE author_id IS NULL"))

    # Learning progress migration safety.
    if "learning_progress" in inspector.get_table_names():
        learning_columns = {col["name"] for col in inspector.get_columns("learning_progress")}
        with engine.begin() as conn:
            if "completed" not in learning_columns:
                conn.execute(text("ALTER TABLE learning_progress ADD COLUMN completed BOOLEAN NOT NULL DEFAULT FALSE"))


migrate_legacy_mysql_schema()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EasyConnect")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(users.router)
app.include_router(community.router)
app.include_router(learning.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/auth/login")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    posts_count = db.query(models.Post).filter(
        models.Post.author_id == current_user.id
    ).count()

    comments_count = db.query(models.Comment).filter(
        models.Comment.author_id == current_user.id
    ).count()

    courses_in_progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id,
        models.LearningProgress.completed == False,
    ).count()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "stats": {
                "posts": posts_count,
                "comments": comments_count,
                "courses": courses_in_progress,
            },
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(
    request: Request,
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return templates.TemplateResponse(
        "quiz.html",
        {
            "request": request,
            "user": current_user,
        },
    )
