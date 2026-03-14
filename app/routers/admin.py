import json
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.auth as auth
import app.models as models
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])


def _admin_user(current_user: models.User = Depends(auth.get_current_active_user)) -> models.User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def _bool_from_form(value: str | None) -> bool:
    return value in ("true", "True", "on", "1", "yes")


def _redirect(message: str | None = None, error: str | None = None) -> RedirectResponse:
    params = []
    if message:
        params.append(f"msg={quote_plus(message)}")
    if error:
        params.append(f"error={quote_plus(error)}")
    suffix = f"?{'&'.join(params)}" if params else ""
    return RedirectResponse(url=f"/administration{suffix}", status_code=303)


def _collect_quiz_options(option_pairs: list[tuple[str | None, str | None]]) -> list[dict]:
    options = []
    for label, gif in option_pairs:
        if not label:
            continue
        entry = {"label": label.strip()}
        if gif:
            entry["gif"] = gif.strip()
        options.append(entry)
    return options


@router.post("/users/create")
async def create_user(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    full_name: str | None = Form(None),
    is_active: str | None = Form(None),
    is_admin: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    normalized_email = email.strip().lower()
    normalized_username = username.strip()
    if (
        db.query(models.User)
        .filter(
            (models.User.email == normalized_email) | (models.User.username == normalized_username)
        )
        .first()
    ):
        return _redirect(error="Email or username is already in use.")

    new_user = models.User(
        email=normalized_email,
        username=normalized_username,
        full_name=(full_name.strip() if full_name else None),
        hashed_password=auth.get_password_hash(password.strip()),
        is_active=_bool_from_form(is_active),
        is_admin=_bool_from_form(is_admin),
    )
    db.add(new_user)
    db.commit()
    return _redirect(message="User added.")


@router.post("/users/{user_id}/update")
async def update_user(
    user_id: int,
    full_name: str | None = Form(None),
    password: str | None = Form(None),
    is_active: str | None = Form(None),
    is_admin: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    user = db.get(models.User, user_id)
    if not user:
        return _redirect(error="User not found.")

    if full_name is not None:
        user.full_name = full_name.strip() or None
    if password:
        user.hashed_password = auth.get_password_hash(password.strip())
    user.is_active = _bool_from_form(is_active)
    user.is_admin = _bool_from_form(is_admin)
    db.commit()
    return _redirect(message="User updated.")


@router.post("/users/{user_id}/delete")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(_admin_user),
):
    user = db.get(models.User, user_id)
    if not user:
        return _redirect(error="User not found.")
    if user.id == current_admin.id:
        return _redirect(error="You cannot delete your own account.")
    if user.is_admin:
        admin_count = db.query(models.User).filter(models.User.is_admin == True).count()
        if admin_count <= 1:
            return _redirect(error="At least one administrator must remain.")
    db.delete(user)
    db.commit()
    return _redirect(message="User deleted.")


@router.post("/courses/create")
async def create_course(
    title: str = Form(...),
    description: str | None = Form(None),
    video_url: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    normalized_title = title.strip()
    if not normalized_title:
        return _redirect(error="Course title is required.")

    db.add(
        models.Course(
            title=normalized_title,
            description=(description.strip() if description else None),
            video_url=(video_url.strip() if video_url else None),
        )
    )
    db.commit()
    return _redirect(message="Course created.")


@router.post("/courses/{course_id}/update")
async def update_course(
    course_id: int,
    title: str = Form(...),
    description: str | None = Form(None),
    video_url: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    course = db.get(models.Course, course_id)
    if not course:
        return _redirect(error="Course not found.")
    course.title = title.strip()
    course.description = description.strip() if description else None
    course.video_url = video_url.strip() if video_url else None
    db.commit()
    return _redirect(message="Course updated.")


@router.post("/courses/{course_id}/delete")
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    course = db.get(models.Course, course_id)
    if not course:
        return _redirect(error="Course not found.")
    db.delete(course)
    db.commit()
    return _redirect(message="Course deleted.")


@router.post("/posts/{post_id}/delete")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    post = db.get(models.Post, post_id)
    if not post:
        return _redirect(error="Post not found.")
    db.delete(post)
    db.commit()
    return _redirect(message="Post deleted.")


@router.post("/comments/{comment_id}/delete")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        return _redirect(error="Comment not found.")
    db.delete(comment)
    db.commit()
    return _redirect(message="Comment deleted.")


@router.post("/quizzes/create")
async def create_quiz(
    prompt: str = Form(...),
    prompt_type: str = Form(...),
    prompt_media: str | None = Form(None),
    answer_index: int = Form(...),
    category: str | None = Form(None),
    option_label_0: str | None = Form(None),
    option_gif_0: str | None = Form(None),
    option_label_1: str | None = Form(None),
    option_gif_1: str | None = Form(None),
    option_label_2: str | None = Form(None),
    option_gif_2: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    if prompt_type not in ("gif_to_label", "label_to_gif"):
        return _redirect(error="Invalid quiz type.")

    options = _collect_quiz_options(
        [
            (option_label_0, option_gif_0),
            (option_label_1, option_gif_1),
            (option_label_2, option_gif_2),
        ]
    )
    if len(options) < 2:
        return _redirect(error="At least two options are required.")
    if not (0 <= answer_index < len(options)):
        return _redirect(error="Invalid answer index.")

    question = models.QuizQuestion(
        prompt=prompt.strip(),
        prompt_media=(prompt_media.strip() if prompt_media else None),
        prompt_type=prompt_type,
        answer_index=answer_index,
        category=category.strip() if category else None,
        options=json.dumps(options, ensure_ascii=False),
    )
    db.add(question)
    db.commit()
    return _redirect(message="Question added.")


@router.post("/quizzes/{quiz_id}/update")
async def update_quiz(
    quiz_id: int,
    prompt: str = Form(...),
    prompt_type: str = Form(...),
    prompt_media: str | None = Form(None),
    answer_index: int = Form(...),
    category: str | None = Form(None),
    option_label_0: str | None = Form(None),
    option_gif_0: str | None = Form(None),
    option_label_1: str | None = Form(None),
    option_gif_1: str | None = Form(None),
    option_label_2: str | None = Form(None),
    option_gif_2: str | None = Form(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    question = db.get(models.QuizQuestion, quiz_id)
    if not question:
        return _redirect(error="Question not found.")
    if prompt_type not in ("gif_to_label", "label_to_gif"):
        return _redirect(error="Invalid quiz type.")

    options = _collect_quiz_options(
        [
            (option_label_0, option_gif_0),
            (option_label_1, option_gif_1),
            (option_label_2, option_gif_2),
        ]
    )
    if len(options) < 2:
        return _redirect(error="At least two options are required.")
    if not (0 <= answer_index < len(options)):
        return _redirect(error="Invalid answer index.")

    question.prompt = prompt.strip()
    question.prompt_type = prompt_type
    question.prompt_media = prompt_media.strip() if prompt_media else None
    question.answer_index = answer_index
    question.category = category.strip() if category else None
    question.options = json.dumps(options, ensure_ascii=False)
    db.commit()
    return _redirect(message="Question updated.")


@router.post("/quizzes/{quiz_id}/delete")
async def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(_admin_user),
):
    question = db.get(models.QuizQuestion, quiz_id)
    if not question:
        return _redirect(error="Question not found.")
    db.delete(question)
    db.commit()
    return _redirect(message="Question deleted.")
