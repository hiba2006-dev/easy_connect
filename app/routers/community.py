from fastapi import APIRouter, Depends, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from pathlib import Path
from uuid import uuid4
from app.activity import record_activity
from app.database import get_db
import app.models as models
import app.schemas as schemas
import app.auth as auth

router = APIRouter(prefix="/community", tags=["community"])
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = Path("static/uploads/posts")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

@router.get("/", response_class=HTMLResponse)
async def community_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.author),
            joinedload(models.Post.comments).joinedload(models.Comment.author),
        )
        .order_by(models.Post.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "user": current_user, "posts": posts}
    )

@router.post("/posts/create")
async def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    image_url = None
    if image and image.filename:
        suffix = Path(image.filename).suffix.lower()
        if suffix not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        data = await image.read()
        if len(data) > MAX_IMAGE_BYTES:
            raise HTTPException(status_code=400, detail="Image size exceeds 5MB")

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        saved_name = f"{uuid4().hex}{suffix}"
        saved_path = UPLOAD_DIR / saved_name
        saved_path.write_bytes(data)
        image_url = f"/static/uploads/posts/{saved_name}"

    new_post = models.Post(
        title=title,
        content=content,
        image_url=image_url,
        author_id=current_user.id
    )
    db.add(new_post)
    db.flush()
    record_activity(
        db,
        current_user.id,
        "post",
        f"Nouvelle publication \"{title}\"",
        {"post_id": new_post.id},
    )
    db.commit()
    return RedirectResponse(url="/community", status_code=303)

@router.post("/posts/{post_id}/comment")
async def add_comment(
    request: Request,
    post_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    new_comment = models.Comment(
        content=content,
        author_id=current_user.id,
        post_id=post_id
    )
    db.add(new_comment)
    db.flush()
    record_activity(
        db,
        current_user.id,
        "comment",
        f"Commentaire ajouté sur le post #{post_id}",
        {"post_id": post_id},
    )
    db.commit()
    return RedirectResponse(url="/community", status_code=303)
