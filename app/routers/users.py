from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import app.auth as auth
import app.models as models
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
