from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import app.auth as auth
import app.models as models
from app.activity import record_activity
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")
COOKIE_MAX_AGE = auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    full_name: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(
        (models.User.email == email) | (models.User.username == username)
    ).first()

    if db_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email or username is already in use"},
        )

    hashed_password = auth.get_password_hash(password)
    new_user = models.User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=COOKIE_MAX_AGE,
        samesite="lax",
    )
    return response


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Incorrect username or password"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=COOKIE_MAX_AGE,
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response

account_router = APIRouter(tags=["account"])


def _recent_activities(db: Session, user_id: int, limit: int = 12):
    return (
        db.query(models.ActivityLog)
        .filter(models.ActivityLog.user_id == user_id)
        .order_by(models.ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )


def render_account_page(
    request: Request,
    user: models.User,
    db: Session,
    **kwargs,
):
    context = {
        "request": request,
        "user": user,
        "activities": _recent_activities(db, user.id),
    }
    if kwargs:
        context.update(kwargs)
    return templates.TemplateResponse("account.html", context)


@account_router.get("/account", response_class=HTMLResponse)
async def account_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return render_account_page(request, current_user, db)


@account_router.post("/account/profile", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    full_name: str = Form(None),
    email: str = Form(...),
    current_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not auth.verify_password(current_password, current_user.hashed_password):
        return render_account_page(
            request,
            current_user,
            db,
            profile_error="Mot de passe incorrect. Vérifiez vos informations.",
        )

    normalized_email = email.strip().lower()
    if normalized_email != current_user.email:
        existing = (
            db.query(models.User)
            .filter(models.User.email == normalized_email, models.User.id != current_user.id)
            .first()
        )
        if existing:
            return render_account_page(
                request,
                current_user,
                db,
                profile_error="Cet e-mail est déjà utilisé par un autre compte.",
            )
        current_user.email = normalized_email

    processed_name = (full_name or "").strip()
    current_user.full_name = processed_name or None

    db.add(current_user)
    record_activity(
        db,
        current_user.id,
        "profile_update",
        "Profil mis à jour",
    )
    db.commit()
    db.refresh(current_user)

    return render_account_page(
        request,
        current_user,
        db,
        profile_success="Profil mis à jour avec succès.",
    )


@account_router.post("/account/password", response_class=HTMLResponse)
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not auth.verify_password(current_password, current_user.hashed_password):
        return render_account_page(
            request,
            current_user,
            db,
            password_error="Mot de passe actuel incorrect.",
        )
    if new_password != confirm_password:
        return render_account_page(
            request,
            current_user,
            db,
            password_error="Les nouveaux mots de passe ne correspondent pas.",
        )
    if len(new_password) < 6:
        return render_account_page(
            request,
            current_user,
            db,
            password_error="Le nouveau mot de passe doit contenir au moins 6 caractères.",
        )

    current_user.hashed_password = auth.get_password_hash(new_password)
    db.add(current_user)
    record_activity(
        db,
        current_user.id,
        "password_change",
        "Mot de passe mis à jour",
    )
    db.commit()
    db.refresh(current_user)

    return render_account_page(
        request,
        current_user,
        db,
        password_success="Mot de passe mis à jour avec succès.",
    )


@account_router.post("/account/delete")
async def delete_account(
    request: Request,
    current_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    if not auth.verify_password(current_password, current_user.hashed_password):
        return render_account_page(
            request,
            current_user,
            db,
            delete_error="Mot de passe incorrect. La suppression a été annulée.",
        )

    user_post_ids = [
        row[0]
        for row in db.query(models.Post.id).filter(models.Post.author_id == current_user.id).all()
    ]
    if user_post_ids:
        db.query(models.Comment).filter(models.Comment.post_id.in_(user_post_ids)).delete(
            synchronize_session=False
        )
    db.query(models.Comment).filter(models.Comment.author_id == current_user.id).delete(
        synchronize_session=False
    )
    db.query(models.Post).filter(models.Post.author_id == current_user.id).delete(
        synchronize_session=False
    )
    db.query(models.LearningItemProgress).filter(
        models.LearningItemProgress.user_id == current_user.id
    ).delete(synchronize_session=False)
    db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id
    ).delete(synchronize_session=False)
    db.delete(current_user)
    db.commit()

    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response
