from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
import app.auth as auth
import app.models as models

router = APIRouter(prefix="/learning", tags=["learning"])
templates = Jinja2Templates(directory="templates")

COURSES = [
    {"id": "asl_alpha", "title": "Alphabet ASL", "description": "Apprenez l'alphabet en langue des signes."},
    {"id": "asl_greetings", "title": "Salutations ASL", "description": "Les signes essentiels pour se presenter et saluer."},
    {"id": "asl_daily", "title": "Conversation du quotidien", "description": "Exprimez des besoins simples en ASL."},
]

COURSE_CONTENT = {
    "asl_alpha": {
        "objectives": [
            "Reconnaitre et produire les 26 lettres de l'alphabet manuel.",
            "Epeler des noms et mots simples avec fluidite.",
            "Utiliser la bonne orientation de la main et le bon rythme.",
        ],
        "lessons": [
            "Lettres A a I: forme des doigts et position du poignet.",
            "Lettres J a R: mouvements specifiques (J, Z) et transitions.",
            "Lettres S a Z: precision visuelle et correction des erreurs frequentes.",
        ],
        "practice": [
            "Epeler votre prenom 5 fois a vitesse lente, puis normale.",
            "Epeler 10 mots du quotidien (maison, ecole, ami, etc.).",
            "Filmez-vous et comparez la lisibilite de chaque lettre.",
        ],
    },
    "asl_greetings": {
        "objectives": [
            "Maitriser les salutations les plus utilisees en ASL.",
            "Se presenter (nom, etat, origine) en une sequence naturelle.",
            "Combiner signe + expression faciale pour clarifier l'intention.",
        ],
        "lessons": [
            "Signes de base: BONJOUR, BONSOIR, COMMENT CA VA, MERCI.",
            "Presentation: JE M'APPELLE..., ENCHANTE, JE VIENS DE....",
            "Mini-dialogues: saluer, poser une question simple, repondre.",
        ],
        "practice": [
            "Realisez une presentation de 20 secondes en ASL.",
            "Repetez 3 dialogues de salutation avec un partenaire.",
            "Travaillez l'expression du visage pour question/reponse.",
        ],
    },
    "asl_daily": {
        "objectives": [
            "Exprimer des besoins quotidiens en ASL.",
            "Construire des phrases courtes et claires.",
            "Ameliorer la comprehension dans des situations reelles.",
        ],
        "lessons": [
            "Besoins essentiels: MANGER, BOIRE, AIDE, TOILETTES, STOP.",
            "Temps et routine: AUJOURD'HUI, DEMAIN, MATIN, TRAVAIL, ECOLE.",
            "Demandes polies: POUVEZ-VOUS..., OU..., COMBIEN....",
        ],
        "practice": [
            "Creez 5 phrases ASL sur votre routine quotidienne.",
            "Simulez une scene: demander de l'aide dans un lieu public.",
            "Refaites chaque phrase avec rythme lent puis naturel.",
        ],
    },
}


def _find_course(course_id: str):
    return next((course for course in COURSES if course["id"] == course_id), None)


@router.get("/", response_class=HTMLResponse)
async def learning_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id
    ).all()
    progress_dict = {p.course_id: p for p in progress}

    return templates.TemplateResponse(
        "learning.html",
        {
            "request": request,
            "user": current_user,
            "courses": COURSES,
            "progress": progress_dict,
        },
    )


@router.post("/course/{course_id}/start")
async def start_course(
    request: Request,
    course_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course = _find_course(course_id)
    if not course:
        return RedirectResponse(url="/learning", status_code=303)

    existing = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id,
        models.LearningProgress.course_id == course_id,
    ).first()

    if not existing:
        new_progress = models.LearningProgress(
            user_id=current_user.id,
            course_id=course_id,
            progress=0,
            completed=False,
        )
        db.add(new_progress)
        db.commit()

    return RedirectResponse(url=f"/learning/course/{course_id}", status_code=303)


@router.get("/course/{course_id}", response_class=HTMLResponse)
async def course_page(
    request: Request,
    course_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course = _find_course(course_id)
    if not course:
        return RedirectResponse(url="/learning", status_code=303)

    course_progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id,
        models.LearningProgress.course_id == course_id,
    ).first()

    if not course_progress:
        course_progress = models.LearningProgress(
            user_id=current_user.id,
            course_id=course_id,
            progress=0,
            completed=False,
        )
        db.add(course_progress)
        db.commit()
        db.refresh(course_progress)

    return templates.TemplateResponse(
        "learning_course.html",
        {
            "request": request,
            "user": current_user,
            "course": course,
            "course_content": COURSE_CONTENT.get(course_id, {"objectives": [], "lessons": [], "practice": []}),
            "course_progress": course_progress,
        },
    )


@router.post("/course/{course_id}/progress")
async def update_progress(
    request: Request,
    course_id: str,
    progress: int = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    course_progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.user_id == current_user.id,
        models.LearningProgress.course_id == course_id,
    ).first()

    if course_progress:
        course_progress.progress = progress
        course_progress.completed = progress >= 100
        db.commit()

    return RedirectResponse(url=f"/learning/course/{course_id}", status_code=303)
