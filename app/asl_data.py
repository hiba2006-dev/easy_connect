ASL_ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def get_alphabet_image_url(letter: str) -> str:
    """Returns a local ASL fingerspelling GIF URL for a single letter."""
    return f"/static/asl_gifs/alphabet/{letter.upper()}.gif"

# -----------------------------
# Course 1: Greetings & Introductions
# -----------------------------
GREETINGS_VOCABULARY = {
    "HELLO": "/static/asl_gifs/greetings/HELLO.gif",
    "GOODBYE": "/static/asl_gifs/greetings/GOODBYE.gif",
    "NICE TO MEET YOU": "/static/asl_gifs/greetings/NICE_TO_MEET_YOU.gif",
    "WHAT'S YOUR NAME?": "/static/asl_gifs/greetings/WHATS_YOUR_NAME.gif",
    "MY NAME IS": "/static/asl_gifs/greetings/MY_NAME_IS.gif",
    "HOW ARE YOU?": "/static/asl_gifs/greetings/HOW_ARE_YOU.gif",
    "I'M FINE": "/static/asl_gifs/greetings/IM_FINE.gif",
    "THANK YOU": "/static/asl_gifs/greetings/THANK_YOU.gif",
    "PLEASE": "/static/asl_gifs/greetings/PLEASE.gif",
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
    "HUNGRY": "/static/asl_gifs/daily/HUNGRY.gif",
    "THIRSTY": "/static/asl_gifs/daily/THIRSTY.gif",
    "BATHROOM": "/static/asl_gifs/daily/BATHROOM.gif",
    "HELP": "/static/asl_gifs/daily/HELP.gif",
    "PLEASE": "/static/asl_gifs/daily/PLEASE.gif",
    "THANK YOU": "/static/asl_gifs/daily/THANK_YOU.gif",
    "WATER": "/static/asl_gifs/daily/WATER.gif",
    "FOOD": "/static/asl_gifs/daily/FOOD.gif",
    "TIRED": "/static/asl_gifs/daily/TIRED.gif",
    "SLEEP": "/static/asl_gifs/daily/SLEEP.gif",
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
    "EAT": "/static/asl_gifs/daily_verbs/EAT.gif",
    "DRINK": "/static/asl_gifs/daily_verbs/DRINK.gif",
    "WAKE UP": "/static/asl_gifs/daily_verbs/WAKE_UP.gif",
    "GET UP": "/static/asl_gifs/daily_verbs/GET_UP.gif",
    "WASH": "/static/asl_gifs/daily_verbs/WASH.gif",
    "SHOWER": "/static/asl_gifs/daily_verbs/SHOWER.gif",
    "BRUSH TEETH": "/static/asl_gifs/daily_verbs/BRUSH_TEETH.gif",
    "GO": "/static/asl_gifs/daily_verbs/GO.gif",
    "COME": "/static/asl_gifs/daily_verbs/COME.gif",
}

VIDEOS = {
    "alphabet": "https://www.youtube.com/embed/nHtF3bR5Dq4",
    "greetings": "https://www.youtube.com/embed/0FcwzMq4iWg",
    "daily": "https://www.youtube.com/embed/6_gXiBe9y9A",
    "sign_with_robert_intro": "https://www.youtube.com/embed/0FcwzMq4iWg",
}

DAILY_CONVERSATION_VIDEOS = [
    "https://www.youtube.com/embed/6_gXiBe9y9A",
    "https://www.youtube.com/embed/0FcwzMq4iWg",
]
