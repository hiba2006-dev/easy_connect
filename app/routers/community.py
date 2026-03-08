from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import app.models as models
import app.schemas as schemas
import app.auth as auth

router = APIRouter(prefix="/community", tags=["community"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def community_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "user": current_user, "posts": posts}
    )

@router.post("/posts/create")
async def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    new_post = models.Post(
        title=title,
        content=content,
        author_id=current_user.id
    )
    db.add(new_post)
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
    db.commit()
    return RedirectResponse(url="/community", status_code=303)