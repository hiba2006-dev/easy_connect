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

DEFAULT_COURSES = [
    {
        "title": "Alphabet ASL",
        "description": "Learn the ASL fingerspelling alphabet.",
        "video_url": "https://www.youtube.com/embed/nHtF3bR5Dq4",
    },
    {
        "title": "Salutations ASL",
        "description": "Essential signs to greet and introduce yourself.",
        "video_url": "https://www.youtube.com/embed/0FcwzMq4iWg",
    },
    {
        "title": "Daily Conversation",
        "description": "Express common daily needs in ASL.",
        "video_url": "https://www.youtube.com/embed/6_gXiBe9y9A",
    },
]


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
            if "image_url" not in post_columns:
                conn.execute(text("ALTER TABLE posts ADD COLUMN image_url VARCHAR(512) NULL"))
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

    # Courses migration safety.
    if "courses" in inspector.get_table_names():
        course_columns = {col["name"] for col in inspector.get_columns("courses")}
        with engine.begin() as conn:
            if "video_url" not in course_columns:
                conn.execute(text("ALTER TABLE courses ADD COLUMN video_url VARCHAR(512) NULL"))


def seed_courses_if_empty() -> None:
    if engine.dialect.name != "mysql":
        return

    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM courses")).scalar() or 0
        if count > 0:
            return

        for course in DEFAULT_COURSES:
            conn.execute(
                text(
                    "INSERT INTO courses (title, description, video_url) "
                    "VALUES (:title, :description, :video_url)"
                ),
                course,
            )


def seed_community_demo_data() -> None:
    if engine.dialect.name != "mysql":
        return

    demo_users = [
        {
            "username": "sarah_asl",
            "email": "sarah.asl@example.com",
            "full_name": "Sarah Miller",
        },
        {
            "username": "mike_signs",
            "email": "mike.signs@example.com",
            "full_name": "Mike Brown",
        },
        {
            "username": "lina_daily",
            "email": "lina.daily@example.com",
            "full_name": "Lina Davis",
        },
    ]

    demo_posts = [
        {
            "title": "My daily ASL routine",
            "content": "I practice 20 minutes every morning with alphabet and greetings. It really helps with speed.",
            "author_username": "sarah_asl",
        },
        {
            "title": "Best way to memorize signs?",
            "content": "I keep mixing up similar signs. Do you use flashcards, videos, or repetition drills?",
            "author_username": "mike_signs",
        },
        {
            "title": "Small win today",
            "content": "I completed the Daily Conversation course and got 86% on the quiz.",
            "author_username": "lina_daily",
        },
    ]

    demo_comments = {
        "My daily ASL routine": [
            ("mike_signs", "Great consistency. Morning practice works best for me too."),
            ("lina_daily", "Same here. I also repeat signs in front of a mirror."),
        ],
        "Best way to memorize signs?": [
            ("sarah_asl", "Flashcards + short daily review helped me a lot."),
            ("lina_daily", "Try grouping signs by context (greetings, food, actions)."),
        ],
        "Small win today": [
            ("sarah_asl", "Nice progress! Keep going."),
            ("mike_signs", "Great score. Next target 90%!"),
        ],
    }

    with engine.begin() as conn:
        # Ensure demo users exist.
        for user in demo_users:
            existing_id = conn.execute(
                text("SELECT id FROM users WHERE username = :username LIMIT 1"),
                {"username": user["username"]},
            ).scalar()
            if existing_id:
                continue

            conn.execute(
                text(
                    "INSERT INTO users (email, username, full_name, hashed_password, is_active) "
                    "VALUES (:email, :username, :full_name, :hashed_password, :is_active)"
                ),
                {
                    "email": user["email"],
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "hashed_password": auth.get_password_hash("demo12345"),
                    "is_active": True,
                },
            )

        # Insert demo posts if missing.
        for post in demo_posts:
            post_id = conn.execute(
                text("SELECT id FROM posts WHERE title = :title LIMIT 1"),
                {"title": post["title"]},
            ).scalar()
            if not post_id:
                author_id = conn.execute(
                    text("SELECT id FROM users WHERE username = :username LIMIT 1"),
                    {"username": post["author_username"]},
                ).scalar()
                if not author_id:
                    continue

                conn.execute(
                    text(
                        "INSERT INTO posts (title, content, author_id) "
                        "VALUES (:title, :content, :author_id)"
                    ),
                    {
                        "title": post["title"],
                        "content": post["content"],
                        "author_id": author_id,
                    },
                )

        # Insert demo comments if missing.
        for post_title, comments in demo_comments.items():
            post_id = conn.execute(
                text("SELECT id FROM posts WHERE title = :title LIMIT 1"),
                {"title": post_title},
            ).scalar()
            if not post_id:
                continue

            for username, comment_text in comments:
                existing_comment = conn.execute(
                    text(
                        "SELECT id FROM comments "
                        "WHERE post_id = :post_id AND content = :content LIMIT 1"
                    ),
                    {"post_id": post_id, "content": comment_text},
                ).scalar()
                if existing_comment:
                    continue

                author_id = conn.execute(
                    text("SELECT id FROM users WHERE username = :username LIMIT 1"),
                    {"username": username},
                ).scalar()
                if not author_id:
                    continue

                conn.execute(
                    text(
                        "INSERT INTO comments (content, author_id, post_id) "
                        "VALUES (:content, :author_id, :post_id)"
                    ),
                    {
                        "content": comment_text,
                        "author_id": author_id,
                        "post_id": post_id,
                    },
                )


migrate_legacy_mysql_schema()
models.Base.metadata.create_all(bind=engine)
seed_courses_if_empty()
seed_community_demo_data()

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
