ASL_ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def get_alphabet_image_url(letter: str) -> str:
    """Returns a simple Giphy GIF URL for fingerspelling a single letter (approximation)."""
    # ASL letters are rare on Giphy; fallback to Lifeprint if needed
    return f"https://www.lifeprint.com/asl101/fingerspelling/abc-gifs/{letter.lower()}.gif"

# -----------------------------
# Course 1: Greetings & Introductions
# -----------------------------
GREETINGS_VOCABULARY = {
    "HELLO": "/static/asl_gifs/HELLO.gif",
    "GOODBYE": "/static/asl_gifs/GOODBYE.gif",
    "NICE TO MEET YOU": "/static/asl_gifs/NICE_TO_MEET_YOU.gif",
    "WHAT'S YOUR NAME?": "/static/asl_gifs/WHATS_YOUR_NAME.gif",
    "MY NAME IS": "/static/asl_gifs/MY_NAME_IS.gif",
    "HOW ARE YOU?": "/static/asl_gifs/HOW_ARE_YOU.gif",
    "I'M FINE": "/static/asl_gifs/IM_FINE.gif",
    "THANK YOU": "/static/asl_gifs/THANK_YOU.gif",
    "PLEASE": "/static/asl_gifs/PLEASE.gif",
}

GREETINGS_DIALOGUES = [
    "HELLO, MY NAME IS SARA.",
    "HI, NICE TO MEET YOU.",
    "GOOD MORNING, HOW ARE YOU?",
    "THANK YOU, GOODBYE.",
    "PLEASE, WHAT IS YOUR NAME?",
]

# -----------------------------
# Course 2: Daily Needs / Besoins Quotidiens
# -----------------------------
DAILY_VOCABULARY = {
    "HUNGRY": "/static/asl_gifs/HUNGRY.gif",
    "THIRSTY": "/static/asl_gifs/THIRSTY.gif",
    "BATHROOM": "/static/asl_gifs/BATHROOM.gif",
    "HELP": "/static/asl_gifs/HELP.gif",
    "PLEASE": "/static/asl_gifs/PLEASE.gif",
    "THANK YOU": "/static/asl_gifs/THANK_YOU.gif",
    "WATER": "/static/asl_gifs/WATER.gif",
    "FOOD": "/static/asl_gifs/FOOD.gif",
    "TIRED": "/static/asl_gifs/TIRED.gif",
    "SLEEP": "/static/asl_gifs/SLEEP.gif",
}

DAILY_SENTENCES = [
    "I AM HUNGRY.",
    "I WANT WATER.",
    "WHERE IS THE BATHROOM?",
    "I AM THIRSTY, DRINK PLEASE.",
    "I TIRED, SLEEP NOW.",
    "HELP ME EAT FOOD.",
    "I DRINK WATER EVERY DAY.",
]

# -----------------------------
# Bonus verbs / actions
# -----------------------------
MORE_DAILY_VERBS = {
    "EAT": "/static/asl_gifs/EAT.gif",
    "DRINK": "/static/asl_gifs/DRINK.gif",
    "WAKE UP": "/static/asl_gifs/WAKE_UP.gif",
    "GET UP": "/static/asl_gifs/GET_UP.gif",
    "WASH": "/static/asl_gifs/WASH.gif",
    "SHOWER": "/static/asl_gifs/SHOWER.gif",
    "BRUSH TEETH": "/static/asl_gifs/BRUSH_TEETH.gif",
    "GO": "/static/asl_gifs/GO.gif",
    "COME": "/static/asl_gifs/COME.gif",
}

VIDEOS = {
    "alphabet": "https://www.youtube.com/embed/nHtF3bR5Dq4",
    "greetings": "https://www.youtube.com/embed/0FcwzMq4iWg",
    "daily": "https://www.youtube.com/embed/6_gXiBe9y9A",
    "sign_with_robert_intro": "https://www.youtube.com/embed/0FcwzMq4iWg",
}