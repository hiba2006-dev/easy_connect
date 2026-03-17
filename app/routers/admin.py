from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

import app.auth as auth
import app.models as models
from app.database import get_db
from app.activity import record_activity

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/administration", status_code=303)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/administration?error=user not found", status_code=303)
    
    user.is_active = not user.is_active
    action = "activated" if user.is_active else "deactivated"
    record_activity(db, current_user.id, "admin_user_toggle", f"User {action}: {user.username}")
    db.commit()
    return RedirectResponse(url="/administration?msg=user updated", status_code=303)

@router.post("/users/{user_id}/toggle-admin")
async def toggle_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/administration", status_code=303)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/administration?error=user not found", status_code=303)
    
    user.is_admin = not user.is_admin
    action = "promoted to admin" if user.is_admin else "demoted from admin"
    record_activity(db, current_user.id, "admin_user_role", f"User {action}: {user.username}")
    db.commit()
    return RedirectResponse(url="/administration?msg=user updated", status_code=303)

@router.post("/users/{user_id}/delete")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/administration", status_code=303)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or user.id == current_user.id:
        return RedirectResponse(url="/administration?error=cannot delete self or invalid user", status_code=303)
    
    username = user.username
    db.delete(user)
    record_activity(db, current_user.id, "admin_user_delete", f"Deleted user: {username}")
    db.commit()
    return RedirectResponse(url="/administration?msg=user deleted", status_code=303)

@router.post("/posts/{post_id}/delete")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/administration", status_code=303)
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return RedirectResponse(url="/administration?error=post not found", status_code=303)
    
    title = post.title or "Untitled"
    db.delete(post)
    record_activity(db, current_user.id, "admin_post_delete", f"Deleted post: {title}")
    db.commit()
    return RedirectResponse(url="/administration?msg=post deleted", status_code=303)

@router.post("/comments/{comment_id}/delete")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return RedirectResponse(url="/administration", status_code=303)
    
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        return RedirectResponse(url="/administration?error=comment not found", status_code=303)
    
    db.delete(comment)
    record_activity(db, current_user.id, "admin_comment_delete", f"Deleted comment #{comment_id}")
    db.commit()
    return RedirectResponse(url="/administration?msg=comment deleted", status_code=303)

@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return JSONResponse(status_code=403, content={"error": "Admin required"})
    
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        return JSONResponse(status_code=404, content={"error": "Course not found"})
    
    db.delete(course)
    db.commit()
    return {"success": True}

@router.get("/stats")
async def admin_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not current_user.is_admin:
        return JSONResponse(status_code=403, content={"error": "Admin required"})
    
    stats = {
        "total_users": db.query(func.count(models.User.id)).scalar(),
        "active_users": db.query(func.count(models.User.id)).filter(models.User.is_active == True).scalar(),
        "total_posts": db.query(func.count(models.Post.id)).scalar(),
        "total_comments": db.query(func.count(models.Comment.id)).scalar(),
        "total_courses": db.query(func.count(models.Course.id)).scalar(),
    }
    return stats
