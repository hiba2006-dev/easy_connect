from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from sqlalchemy import inspect, text, func
from sqlalchemy.orm import Session, joinedload

from app.database import engine, get_db
import app.models as models
import app.auth as auth
from app.routers import users, community, learning, admin, quiz

DEFAULT_COURSES = [
    {
        "title": "Alphabet ASL",
        "description": "Learn the ASL fingerspelling alphabet.",
        "video_url": "https://www.youtube.com/embed/nHtF3bR5Dq4",
    },
    {
        "title": "ASL Greetings",
        "description": "Essential signs to greet and introduce yourself.",
        "video_url": "https://www.youtube.com/embed/0FcwzMq4iWg",
    },
    {
        "title": "Daily Conversation",
        "description": "Express common daily needs in ASL.",
        "video_url": "https://www.youtube.com/embed/6_gXiBe9y9A",
    },
]

DEFAULT_QUIZ_QUESTIONS = [
    {
        "prompt": "Which GIF depicts the letter A?",
        "prompt_media": "/static/asl_gifs/alphabet/A.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "A", "gif": "/static/asl_gifs/alphabet/A.gif"},
            {"label": "B", "gif": "/static/asl_gifs/alphabet/B.gif"},
            {"label": "G", "gif": "/static/asl_gifs/alphabet/G.gif"},
        ],
        "answer_index": 0,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter B?",
        "prompt_media": "/static/asl_gifs/alphabet/B.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "A", "gif": "/static/asl_gifs/alphabet/A.gif"},
            {"label": "B", "gif": "/static/asl_gifs/alphabet/B.gif"},
            {"label": "C", "gif": "/static/asl_gifs/alphabet/C.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter C?",
        "prompt_media": "/static/asl_gifs/alphabet/C.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "C", "gif": "/static/asl_gifs/alphabet/C.gif"},
            {"label": "D", "gif": "/static/asl_gifs/alphabet/D.gif"},
            {"label": "E", "gif": "/static/asl_gifs/alphabet/E.gif"},
        ],
        "answer_index": 0,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter D?",
        "prompt_media": "/static/asl_gifs/alphabet/D.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "D", "gif": "/static/asl_gifs/alphabet/D.gif"},
            {"label": "F", "gif": "/static/asl_gifs/alphabet/F.gif"},
            {"label": "H", "gif": "/static/asl_gifs/alphabet/H.gif"},
        ],
        "answer_index": 0,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter F?",
        "prompt_media": "/static/asl_gifs/alphabet/F.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "E", "gif": "/static/asl_gifs/alphabet/E.gif"},
            {"label": "F", "gif": "/static/asl_gifs/alphabet/F.gif"},
            {"label": "G", "gif": "/static/asl_gifs/alphabet/G.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter H?",
        "prompt_media": "/static/asl_gifs/alphabet/H.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "G", "gif": "/static/asl_gifs/alphabet/G.gif"},
            {"label": "H", "gif": "/static/asl_gifs/alphabet/H.gif"},
            {"label": "I", "gif": "/static/asl_gifs/alphabet/I.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter L?",
        "prompt_media": "/static/asl_gifs/alphabet/L.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "K", "gif": "/static/asl_gifs/alphabet/K.gif"},
            {"label": "L", "gif": "/static/asl_gifs/alphabet/L.gif"},
            {"label": "M", "gif": "/static/asl_gifs/alphabet/M.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter O?",
        "prompt_media": "/static/asl_gifs/alphabet/O.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "O", "gif": "/static/asl_gifs/alphabet/O.gif"},
            {"label": "P", "gif": "/static/asl_gifs/alphabet/P.gif"},
            {"label": "Q", "gif": "/static/asl_gifs/alphabet/Q.gif"},
        ],
        "answer_index": 0,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter R?",
        "prompt_media": "/static/asl_gifs/alphabet/R.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "P", "gif": "/static/asl_gifs/alphabet/P.gif"},
            {"label": "R", "gif": "/static/asl_gifs/alphabet/R.gif"},
            {"label": "T", "gif": "/static/asl_gifs/alphabet/T.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Which GIF depicts the letter S?",
        "prompt_media": "/static/asl_gifs/alphabet/S.gif",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "R", "gif": "/static/asl_gifs/alphabet/R.gif"},
            {"label": "S", "gif": "/static/asl_gifs/alphabet/S.gif"},
            {"label": "T", "gif": "/static/asl_gifs/alphabet/T.gif"},
        ],
        "answer_index": 1,
        "category": "alphabet",
    },
    {
        "prompt": "Select the GIF that matches the greeting \"HELLO\".",
        "prompt_media": None,
        "prompt_type": "label_to_gif",
        "options": [
            {"label": "HELLO", "gif": "/static/asl_gifs/greetings/HELLO.mp4"},
            {"label": "THANK YOU", "gif": "/static/asl_gifs/greetings/THANK_YOU.mp4"},
            {"label": "GOODBYE", "gif": "/static/asl_gifs/greetings/GOODBYE.mp4"},
        ],
        "answer_index": 0,
        "category": "greetings",
    },
    {
        "prompt": "Match the label \"THANK YOU\" to the correct GIF.",
        "prompt_media": None,
        "prompt_type": "label_to_gif",
        "options": [
            {"label": "THANK YOU", "gif": "/static/asl_gifs/greetings/THANK_YOU.mp4"},
            {"label": "PLEASE", "gif": "/static/asl_gifs/greetings/PLEASE.mp4"},
            {"label": "HELLO", "gif": "/static/asl_gifs/greetings/HELLO.mp4"},
        ],
        "answer_index": 0,
        "category": "greetings",
    },
    {
        "prompt": "Which GIF shows the sign for \"PLEASE\"?",
        "prompt_media": "/static/asl_gifs/greetings/PLEASE.mp4",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "PLEASE", "gif": "/static/asl_gifs/greetings/PLEASE.mp4"},
            {"label": "THANK YOU", "gif": "/static/asl_gifs/greetings/THANK_YOU.mp4"},
            {"label": "HELLO", "gif": "/static/asl_gifs/greetings/HELLO.mp4"},
        ],
        "answer_index": 0,
        "category": "greetings",
    },
    {
        "prompt": "Choose the GIF that illustrates \"GOODBYE\".",
        "prompt_media": "/static/asl_gifs/greetings/GOODBYE.mp4",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "GOODBYE", "gif": "/static/asl_gifs/greetings/GOODBYE.mp4"},
            {"label": "MY NAME IS", "gif": "/static/asl_gifs/greetings/MY_NAME_IS.mp4"},
            {"label": "NICE TO MEET YOU", "gif": "/static/asl_gifs/greetings/NICE_TO_MEET_YOU.mp4"},
        ],
        "answer_index": 0,
        "category": "greetings",
    },
    {
        "prompt": "Choose the GIF that matches \"THIRSTY\".",
        "prompt_media": "/static/asl_gifs/daily/THIRSTY.mp4",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "THIRSTY", "gif": "/static/asl_gifs/daily/THIRSTY.mp4"},
            {"label": "HUNGRY", "gif": "/static/asl_gifs/daily/HUNGRY.mp4"},
            {"label": "WATER", "gif": "/static/asl_gifs/daily/WATER.mp4"},
        ],
        "answer_index": 0,
        "category": "daily",
    },
    {
        "prompt": "Which GIF shows the sign for \"HUNGRY\"?",
        "prompt_media": "/static/asl_gifs/daily/HUNGRY.mp4",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "HUNGRY", "gif": "/static/asl_gifs/daily/HUNGRY.mp4"},
            {"label": "TIRED", "gif": "/static/asl_gifs/daily/TIRED.mp4"},
            {"label": "FOOD", "gif": "/static/asl_gifs/daily/FOOD.mp4"},
        ],
        "answer_index": 0,
        "category": "daily",
    },
    {
        "prompt": "Match the label \"WATER\" to the correct GIF.",
        "prompt_media": None,
        "prompt_type": "label_to_gif",
        "options": [
            {"label": "WATER", "gif": "/static/asl_gifs/daily/WATER.mp4"},
            {"label": "SLEEP", "gif": "/static/asl_gifs/daily/SLEEP.mp4"},
            {"label": "FOOD", "gif": "/static/asl_gifs/daily/FOOD.mp4"},
        ],
        "answer_index": 0,
        "category": "daily",
    },
    {
        "prompt": "Match the label \"HELP\" to the correct GIF.",
        "prompt_media": None,
        "prompt_type": "label_to_gif",
        "options": [
            {"label": "HELP", "gif": "/static/asl_gifs/daily/HELP.mp4"},
            {"label": "PLEASE", "gif": "/static/asl_gifs/daily/PLEASE.mp4"},
            {"label": "TIRED", "gif": "/static/asl_gifs/daily/TIRED.mp4"},
        ],
        "answer_index": 0,
        "category": "daily",
    },
    {
        "prompt": "Match the label \"BRUSH TEETH\" to the correct GIF.",
        "prompt_media": None,
        "prompt_type": "label_to_gif",
        "options": [
            {"label": "BRUSH TEETH", "gif": "/static/asl_gifs/daily_verbs/BRUSH_TEETH.mp4"},
            {"label": "WASH", "gif": "/static/asl_gifs/daily_verbs/WASH.mp4"},
            {"label": "SHOWER", "gif": "/static/asl_gifs/daily_verbs/SHOWER.mp4"},
        ],
        "answer_index": 0,
        "category": "daily_verbs",
    },
    {
        "prompt": "Which GIF illustrates \"DRINK\"?",
        "prompt_media": "/static/asl_gifs/daily_verbs/DRINK.mp4",
        "prompt_type": "gif_to_label",
        "options": [
            {"label": "DRINK", "gif": "/static/asl_gifs/daily_verbs/DRINK.mp4"},
            {"label": "EAT", "gif": "/static/asl_gifs/daily_verbs/EAT.mp4"},
            {"label": "WAKE UP", "gif": "/static/asl_gifs/daily_verbs/WAKE_UP.mp4"},
        ],
        "answer_index": 0,
        "category": "daily_verbs",
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
        if "is_admin" not in existing_columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE"))

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

    # Quiz question migration safety.
    if "quiz_questions" in inspector.get_table_names():
        quiz_columns = {col["name"] for col in inspector.get_columns("quiz_questions")}
        with engine.begin() as conn:
            if "prompt_media" not in quiz_columns:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN prompt_media VARCHAR(512) NULL"))
            if "prompt_type" not in quiz_columns:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN prompt_type VARCHAR(32) NOT NULL DEFAULT 'gif_to_label'"))
            if "answer_index" not in quiz_columns:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN answer_index INT NOT NULL DEFAULT 0"))
            if "options" not in quiz_columns:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN options TEXT NOT NULL"))
            if "category" not in quiz_columns:
                conn.execute(text("ALTER TABLE quiz_questions ADD COLUMN category VARCHAR(64) NULL"))
            # ensure new columns have defaults where necessary
            if "prompt_type" not in quiz_columns:
                conn.execute(text("UPDATE quiz_questions SET prompt_type = 'gif_to_label' WHERE prompt_type IS NULL"))
            if "options" not in quiz_columns:
                conn.execute(text("UPDATE quiz_questions SET options = '[]' WHERE options IS NULL"))
            if "answer_index" not in quiz_columns:
                conn.execute(text("UPDATE quiz_questions SET answer_index = 0 WHERE answer_index IS NULL"))


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
            "username": "admin",
            "email": "admin@easyconnect.local",
            "full_name": "Administrator",
            "password": "admin12345",
            "is_admin": True,
        },
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

            password = user.get("password", "demo12345")
            conn.execute(
                text(
                    "INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin) "
                    "VALUES (:email, :username, :full_name, :hashed_password, :is_active, :is_admin)"
                ),
                {
                    "email": user["email"],
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "hashed_password": auth.get_password_hash(password),
                    "is_active": True,
                    "is_admin": bool(user.get("is_admin", False)),
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


def seed_quiz_questions() -> None:
   with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM quiz_questions")).scalar() or 0
        if count > 0:
            return

        for question in DEFAULT_QUIZ_QUESTIONS:
            if question["prompt"] in existing_prompts:
                continue
            conn.execute(
                text(
                    "INSERT INTO quiz_questions (prompt, prompt_media, prompt_type, answer_index, options, category) "
                    "VALUES (:prompt, :prompt_media, :prompt_type, :answer_index, :options, :category)"
                ),
                {
                    "prompt": question["prompt"],
                    "prompt_media": question.get("prompt_media"),
                    "prompt_type": question["prompt_type"],
                    "answer_index": question["answer_index"],
                    "options": json.dumps(question["options"], ensure_ascii=False),
                    "category": question.get("category"),
                },
            )


migrate_legacy_mysql_schema()
models.Base.metadata.create_all(bind=engine)
seed_courses_if_empty()
seed_community_demo_data()
seed_quiz_questions()

app = FastAPI(title="EasyConnect")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(users.router)
app.include_router(users.account_router)
app.include_router(community.router)
app.include_router(learning.router)
app.include_router(admin.router)
app.include_router(quiz.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/auth/login")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if current_user.is_admin:
        return RedirectResponse(url="/administration")

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


@app.get("/administration", response_class=HTMLResponse)
async def administration_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/dashboard")

    total_users = db.query(func.count(models.User.id)).scalar() or 0
    active_users = (
        db.query(func.count(models.User.id))
        .filter(models.User.is_active == True)
        .scalar()
        or 0
    )
    posts_total = db.query(func.count(models.Post.id)).scalar() or 0
    comments_total = db.query(func.count(models.Comment.id)).scalar() or 0
    courses_total = db.query(func.count(models.Course.id)).scalar() or 0
    recent_users = (
        db.query(models.User)
        .order_by(models.User.created_at.desc())
        .limit(5)
        .all()
    )

    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    courses = db.query(models.Course).order_by(models.Course.title.asc()).all()
    posts = (
        db.query(models.Post)
        .options(joinedload(models.Post.author))
        .order_by(models.Post.created_at.desc())
        .limit(8)
        .all()
    )
    comments = (
        db.query(models.Comment)
        .options(
            joinedload(models.Comment.author),
            joinedload(models.Comment.post),
        )
        .order_by(models.Comment.created_at.desc())
        .limit(8)
        .all()
    )
    quiz_rows = (
        db.query(models.QuizQuestion)
        .order_by(models.QuizQuestion.created_at.desc())
        .all()
    )
    quiz_questions = [
        {
            "id": row.id,
            "prompt": row.prompt,
            "prompt_media": row.prompt_media,
            "prompt_type": row.prompt_type,
            "answer_index": row.answer_index,
            "category": row.category,
            "options": json.loads(row.options or "[]"),
        }
        for row in quiz_rows
    ]

    return templates.TemplateResponse(
        "administration.html",
        {
            "request": request,
            "user": current_user,
            "stats": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": max(total_users - active_users, 0),
                "posts": posts_total,
                "comments": comments_total,
                "courses": courses_total,
            },
            "recent_users": recent_users,
            "users": users,
            "courses": courses,
            "posts": posts,
            "comments": comments,
            "quiz_questions": quiz_questions,
            "message": request.query_params.get("msg"),
            "error": request.query_params.get("error"),
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
