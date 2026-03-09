import re
from math import floor

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session
from urllib.parse import parse_qs, urlparse
from pydantic import BaseModel

from app.database import get_db
import app.auth as auth
import app.models as models
from app.asl_data import (
    ASL_ALPHABET,
    DAILY_CONVERSATION_VIDEOS,
    DAILY_SENTENCES,
    DAILY_VOCABULARY,
    GREETINGS_DIALOGUES,
    GREETINGS_VOCABULARY,
    MORE_DAILY_VERBS,
    VIDEOS,
    get_alphabet_image_url,
)

router = APIRouter(prefix="/learning", tags=["learning"])
templates = Jinja2Templates(directory="templates")

COURSE_CONTENT = {
    "asl_alpha": {
        "objectives": [
            "Recognize and produce all 26 letters of the manual alphabet.",
            "Spell names and simple words smoothly.",
            "Use proper hand orientation and steady rhythm.",
        ],
        "lessons": [
            "Letters A to I: finger shape and wrist position.",
            "Letters J to R: specific motion letters (J, Z) and transitions.",
            "Letters S to Z: visual precision and frequent error correction.",
        ],
        "practice": [
            "Spell your first name 5 times slowly, then at normal speed.",
            "Spell 10 everyday words (home, school, friend, etc.).",
            "Record yourself and compare the readability of each letter.",
        ],
    },
    "asl_greetings": {
        "objectives": [
            "Master the most common greetings in ASL.",
            "Introduce yourself (name, status, origin) in a natural sequence.",
            "Combine signs with facial expressions to clarify intent.",
        ],
        "lessons": [
            "Core signs: HELLO, GOOD EVENING, HOW ARE YOU, THANK YOU.",
            "Introductions: MY NAME IS..., NICE TO MEET YOU, I AM FROM....",
            "Mini-dialogues: greet, ask a simple question, reply.",
        ],
        "practice": [
            "Deliver a 20-second ASL introduction.",
            "Repeat 3 greeting dialogues with a partner.",
            "Practice facial expressions for question/answer contrast.",
        ],
    },
    "asl_daily": {
        "objectives": [
            "Express daily needs in ASL.",
            "Build short, clear phrases.",
            "Improve comprehension in real situations.",
        ],
        "lessons": [
            "Essential needs: EAT, DRINK, HELP, BATHROOM, STOP.",
            "Time and routine: TODAY, TOMORROW, MORNING, WORK, SCHOOL.",
            "Polite requests: CAN YOU..., WHERE..., HOW MUCH....",
        ],
        "practice": [
            "Create 5 ASL sentences about your daily routine.",
            "Simulate a scene: asking for help in a public place.",
            "Repeat each sentence slowly, then naturally.",
        ],
    },
}


def _find_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def _find_next_course(db: Session, course_id: int):
    return (
        db.query(models.Course)
        .filter(models.Course.id > course_id)
        .order_by(models.Course.id.asc())
        .first()
    )


def _course_key(course_title: str) -> str | None:
    title = (course_title or "").strip().lower()
    if "alphabet" in title:
        return "asl_alpha"
    if "salutation" in title or "greeting" in title:
        return "asl_greetings"
    if "quotidien" in title or "daily" in title or "conversation" in title:
        return "asl_daily"
    return None


def _progress_query(db: Session, user_id: int, course_id: int):
    return db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == user_id,
        or_(
            models.LearningProgress.course_id == str(course_id),
            models.LearningProgress.course_id == course_id,
        ),
    )


def _normalize_video_url(url: str | None) -> str | None:
    if not url:
        return None

    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    if "youtube.com" in host:
        if path.startswith("/embed/"):
            return url
        if path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
        if path.startswith("/shorts/"):
            video_id = path.split("/shorts/", 1)[1].split("/", 1)[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
    if "youtu.be" in host:
        video_id = path.lstrip("/").split("/", 1)[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"

    return url


def _to_watch_url(url: str | None) -> str | None:
    embed_url = _normalize_video_url(url)
    if not embed_url:
        return None
    parsed = urlparse(embed_url)
    path = parsed.path or ""
    if "/embed/" in path:
        video_id = path.split("/embed/", 1)[1].split("/", 1)[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    return embed_url


def _split_video_urls(raw: str | None) -> list[str]:
    if not raw:
        return []
    normalized = raw.replace(";", "\n").replace(",", "\n")
    return [part.strip() for part in normalized.splitlines() if part.strip()]


def _build_video_entries(db_value: str | None, fallback_urls: list[str]) -> list[dict[str, str]]:
    candidates = _split_video_urls(db_value) if db_value else list(fallback_urls)
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for raw in candidates:
        # Ignore partial/invalid values like "https" that can appear from manual edits.
        if not raw.startswith(("http://", "https://")):
            continue
        embed = _normalize_video_url(raw)
        if not embed or embed in seen:
            continue
        parsed = urlparse(embed)
        if not parsed.scheme or not parsed.netloc:
            continue
        watch = _to_watch_url(embed) or embed
        entries.append({"embed": embed, "watch": watch})
        seen.add(embed)
    return entries


def _slugify(text: str) -> str:
    normalized = text.lower().replace("'", "")
    slug = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
    return slug or "item"


def _build_trackable_item_ids(
    course_content: dict,
    extra_content: dict,
) -> list[str]:
    item_ids: list[str] = []
    item_ids.extend([f"objective_{idx}" for idx, _ in enumerate(course_content.get("objectives", []), start=1)])
    item_ids.extend([f"lesson_{idx}" for idx, _ in enumerate(course_content.get("lessons", []), start=1)])
    item_ids.extend([f"practice_{idx}" for idx, _ in enumerate(course_content.get("practice", []), start=1)])

    item_ids.extend([f"alphabet_{letter}" for letter in extra_content.get("alphabet", [])])
    item_ids.extend([f"vocab_{_slugify(word)}" for word in extra_content.get("vocabulary", {}).keys()])
    item_ids.extend([f"daily_{_slugify(word)}" for word in extra_content.get("daily_signs", {}).keys()])
    item_ids.extend([f"dialogue_{idx}" for idx, _ in enumerate(extra_content.get("dialogues", []), start=1)])
    item_ids.extend([f"sentence_{idx}" for idx, _ in enumerate(extra_content.get("sentences", []), start=1)])
    item_ids.extend([f"video_{idx}" for idx, _ in enumerate(extra_content.get("videos", []), start=1)])
    return item_ids


def _build_course_items(
    course_content: dict,
    extra_content: dict,
    item_done_map: dict[str, bool],
) -> list[dict]:
    items: list[dict] = []

    for idx, text in enumerate(course_content.get("objectives", []), start=1):
        item_id = f"objective_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "text",
            "section": "Objective",
            "title": f"Objective {idx}",
            "text": text,
            "done": item_done_map.get(item_id, False),
        })

    for idx, text in enumerate(course_content.get("lessons", []), start=1):
        item_id = f"lesson_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "text",
            "section": "Lesson",
            "title": f"Lesson {idx}",
            "text": text,
            "done": item_done_map.get(item_id, False),
        })

    for idx, text in enumerate(course_content.get("practice", []), start=1):
        item_id = f"practice_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "text",
            "section": "Practice",
            "title": f"Exercise {idx}",
            "text": text,
            "done": item_done_map.get(item_id, False),
        })

    for letter in extra_content.get("alphabet", []):
        item_id = f"alphabet_{letter}"
        items.append({
            "item_id": item_id,
            "kind": "image",
            "section": "Alphabet",
            "title": f"Letter {letter}",
            "text": "Observe the hand shape and reproduce the sign.",
            "media_url": get_alphabet_image_url(letter),
            "done": item_done_map.get(item_id, False),
        })

    for word, media_url in extra_content.get("vocabulary", {}).items():
        item_id = f"vocab_{_slugify(word)}"
        items.append({
            "item_id": item_id,
            "kind": "image",
            "section": "Vocabulary",
            "title": word,
            "text": "Observe and then reproduce this sign.",
            "media_url": media_url,
            "done": item_done_map.get(item_id, False),
        })

    for word, media_url in extra_content.get("daily_signs", {}).items():
        item_id = f"daily_{_slugify(word)}"
        items.append({
            "item_id": item_id,
            "kind": "image",
            "section": "Daily Conversation",
            "title": word,
            "text": "Observe and then reproduce this sign.",
            "media_url": media_url,
            "done": item_done_map.get(item_id, False),
        })

    for idx, text in enumerate(extra_content.get("dialogues", []), start=1):
        item_id = f"dialogue_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "text",
            "section": "Dialogue",
            "title": f"Dialogue {idx}",
            "text": text,
            "done": item_done_map.get(item_id, False),
        })

    for idx, text in enumerate(extra_content.get("sentences", []), start=1):
        item_id = f"sentence_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "text",
            "section": "Sentence",
            "title": f"Sentence {idx}",
            "text": text,
            "done": item_done_map.get(item_id, False),
        })

    for idx, video in enumerate(extra_content.get("videos", []), start=1):
        item_id = f"video_{idx}"
        items.append({
            "item_id": item_id,
            "kind": "video",
            "section": "Video",
            "title": f"Video {idx}",
            "text": "Watch the video, then move to the next step.",
            "media_url": video.get("embed"),
            "watch_url": video.get("watch"),
            "done": item_done_map.get(item_id, False),
        })

    return items


def _compute_progress(item_ids: list[str], done_map: dict[str, bool]) -> tuple[int, bool]:
    if not item_ids:
        return 0, False
    completed_count = sum(1 for item_id in item_ids if done_map.get(item_id, False))
    progress = floor((completed_count / len(item_ids)) * 100)
    return progress, completed_count == len(item_ids)


def _ensure_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
    progress: int,
    completed: bool,
) -> models.LearningProgress:
    course_progress = _progress_query(db, user_id, course_id).first()
    if not course_progress:
        course_progress = models.LearningProgress(
            user_id=user_id,
            course_id=str(course_id),
            progress=progress,
            completed=completed,
        )
        db.add(course_progress)
    else:
        course_progress.progress = progress
        course_progress.completed = completed
    return course_progress


class ItemProgressPayload(BaseModel):
    item_id: str
    completed: bool


@router.get("/", response_class=HTMLResponse)
async def learning_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id
    ).all()
    progress_dict = {}
    for p in progress:
        progress_dict[p.course_id] = p
        if str(p.course_id).isdigit():
            progress_dict[int(p.course_id)] = p

    courses = db.query(models.Course).order_by(models.Course.id.asc()).all()

    return templates.TemplateResponse(
        "learning.html",
        {
            "request": request,
            "user": current_user,
            "courses": courses,
            "progress": progress_dict,
        },
    )


@router.post("/course/{course_id}/start")
async def start_course(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course = _find_course(db, course_id)
    if not course:
        return RedirectResponse(url="/learning", status_code=303)

    existing = _progress_query(db, current_user.id, course_id).first()

    if not existing:
        new_progress = models.LearningProgress(
            user_id=current_user.id,
            course_id=str(course_id),
            progress=0,
            completed=False,
        )
        db.add(new_progress)
        db.commit()

    return RedirectResponse(url=f"/learning/course/{course_id}", status_code=303)


@router.get("/course/{course_id}", response_class=HTMLResponse)
async def course_page(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course = _find_course(db, course_id)
    if not course:
        return RedirectResponse(url="/learning", status_code=303)
    next_course = _find_next_course(db, course_id)

    extra_content = {}
    course_key = _course_key(course.title)
    if course_key == "asl_alpha":
        video_entries = _build_video_entries(course.video_url, [VIDEOS.get("alphabet")])
        extra_content = {
            "alphabet": ASL_ALPHABET,
            "get_image": get_alphabet_image_url,
            "videos": video_entries,
        }
    elif course_key == "asl_greetings":
        video_entries = _build_video_entries(course.video_url, [VIDEOS.get("greetings")])
        extra_content = {
            "vocabulary": GREETINGS_VOCABULARY,
            "dialogues": GREETINGS_DIALOGUES,
            "videos": video_entries,
        }
    elif course_key == "asl_daily":
        video_entries = _build_video_entries(
            course.video_url,
            DAILY_CONVERSATION_VIDEOS or [VIDEOS.get("daily")],
        )
        extra_content = {
            "daily_signs": {**DAILY_VOCABULARY, **MORE_DAILY_VERBS},
            "sentences": DAILY_SENTENCES,
            "videos": video_entries,
        }

    trackable_item_ids = _build_trackable_item_ids(
        COURSE_CONTENT.get(course_key, {"objectives": [], "lessons": [], "practice": []}),
        extra_content,
    )
    item_rows = db.query(models.LearningItemProgress).filter(
        models.LearningItemProgress.user_id == current_user.id,
        models.LearningItemProgress.course_id == str(course_id),
    ).all()
    item_done_map = {row.item_id: bool(row.completed) for row in item_rows}
    progress_value, is_completed = _compute_progress(trackable_item_ids, item_done_map)
    course_progress = _ensure_course_progress(
        db,
        user_id=current_user.id,
        course_id=course_id,
        progress=progress_value,
        completed=is_completed,
    )
    db.commit()
    db.refresh(course_progress)

    return templates.TemplateResponse(
        "learning_course.html",
        {
            "request": request,
            "user": current_user,
            "course": course,
            "course_content": COURSE_CONTENT.get(course_key, {"objectives": [], "lessons": [], "practice": []}),
            "course_progress": course_progress,
            "item_done_map": item_done_map,
            "next_course_url": f"/learning/course/{next_course.id}" if next_course else "/learning",
            "course_items": _build_course_items(
                COURSE_CONTENT.get(course_key, {"objectives": [], "lessons": [], "practice": []}),
                extra_content,
                item_done_map,
            ),
            **extra_content,
        },
    )


@router.post("/course/{course_id}/progress")
async def update_progress(
    request: Request,
    course_id: int,
    progress: int = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course_progress = _progress_query(db, current_user.id, course_id).first()

    if course_progress:
        course_progress.progress = progress
        course_progress.completed = progress >= 100
        db.commit()

    return RedirectResponse(url=f"/learning/course/{course_id}", status_code=303)


@router.post("/course/{course_id}/item")
async def update_item_progress(
    course_id: int,
    payload: ItemProgressPayload,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course = _find_course(db, course_id)
    if not course:
        return JSONResponse(status_code=404, content={"error": "Course not found"})

    course_key = _course_key(course.title)
    extra_content = {}
    if course_key == "asl_alpha":
        video_entries = _build_video_entries(course.video_url, [VIDEOS.get("alphabet")])
        extra_content = {"alphabet": ASL_ALPHABET, "videos": video_entries}
    elif course_key == "asl_greetings":
        video_entries = _build_video_entries(course.video_url, [VIDEOS.get("greetings")])
        extra_content = {"vocabulary": GREETINGS_VOCABULARY, "dialogues": GREETINGS_DIALOGUES, "videos": video_entries}
    elif course_key == "asl_daily":
        video_entries = _build_video_entries(
            course.video_url,
            DAILY_CONVERSATION_VIDEOS or [VIDEOS.get("daily")],
        )
        extra_content = {"daily_signs": {**DAILY_VOCABULARY, **MORE_DAILY_VERBS}, "sentences": DAILY_SENTENCES, "videos": video_entries}

    trackable_item_ids = _build_trackable_item_ids(
        COURSE_CONTENT.get(course_key, {"objectives": [], "lessons": [], "practice": []}),
        extra_content,
    )
    valid_item_ids = set(trackable_item_ids)
    if payload.item_id not in valid_item_ids:
        return JSONResponse(status_code=400, content={"error": "Invalid item_id"})

    item_row = db.query(models.LearningItemProgress).filter(
        models.LearningItemProgress.user_id == current_user.id,
        models.LearningItemProgress.course_id == str(course_id),
        models.LearningItemProgress.item_id == payload.item_id,
    ).first()

    if not item_row:
        item_row = models.LearningItemProgress(
            user_id=current_user.id,
            course_id=str(course_id),
            item_id=payload.item_id,
            completed=payload.completed,
        )
        db.add(item_row)
    else:
        item_row.completed = payload.completed

    current_rows = db.query(models.LearningItemProgress).filter(
        models.LearningItemProgress.user_id == current_user.id,
        models.LearningItemProgress.course_id == str(course_id),
    ).all()
    item_done_map = {row.item_id: bool(row.completed) for row in current_rows}
    item_done_map[payload.item_id] = payload.completed
    progress_value, is_completed = _compute_progress(trackable_item_ids, item_done_map)
    _ensure_course_progress(
        db,
        user_id=current_user.id,
        course_id=course_id,
        progress=progress_value,
        completed=is_completed,
    )
    db.commit()

    return JSONResponse(
        content={
            "ok": True,
            "progress": progress_value,
            "completed": is_completed,
        }
    )
