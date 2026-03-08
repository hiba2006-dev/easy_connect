import os
import requests

# Create a folder to save the GIFs
os.makedirs("static/asl_gifs/alphabet", exist_ok=True)
os.makedirs("static/asl_gifs/greetings", exist_ok=True)
os.makedirs("static/asl_gifs/daily", exist_ok=True)
os.makedirs("static/asl_gifs/daily_verbs", exist_ok=True)

# 1️⃣ Alphabet
ASL_ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
for letter in ASL_ALPHABET:
    url = f"https://www.lifeprint.com/asl101/fingerspelling/abc-gifs/{letter.lower()}.gif"
    r = requests.get(url)
    with open(f"static/asl_gifs/alphabet/{letter}.gif", "wb") as f:
        f.write(r.content)
    print(f"Downloaded {letter} alphabet GIF")

# 2️⃣ Greetings Vocabulary
GREETINGS_VOCABULARY = {
    "HELLO": "hello.gif",
    "GOODBYE": "goodbye.gif",
    "NICE TO MEET YOU": "nicetomeetyou.gif",
    "WHAT'S YOUR NAME?": "name.gif",
    "MY NAME IS": "mynameis.gif",
    "HOW ARE YOU?": "howareyou.gif",
    "I'M FINE": "fine.gif",
    "THANK YOU": "thankyou.gif",
    "PLEASE": "please.gif",
}

for word, filename in GREETINGS_VOCABULARY.items():
    url = f"https://www.lifeprint.com/asl101/gifs/{filename}"
    r = requests.get(url)
    safe_name = word.replace(" ", "_").replace("'", "").replace("?", "")
    with open(f"static/asl_gifs/greetings/{safe_name}.gif", "wb") as f:
        f.write(r.content)
    print(f"Downloaded {word} greeting GIF")

# 3️⃣ Daily Vocabulary
DAILY_VOCABULARY = {
    "HUNGRY": "hungry.gif",
    "THIRSTY": "thirsty.gif",
    "BATHROOM": "bathroom.gif",
    "HELP": "help.gif",
    "PLEASE": "please.gif",
    "THANK YOU": "thankyou.gif",
    "WATER": "water.gif",
    "FOOD": "food.gif",
    "TIRED": "tired.gif",
    "SLEEP": "sleep.gif",
}

for word, filename in DAILY_VOCABULARY.items():
    url = f"https://www.lifeprint.com/asl101/gifs/{filename}"
    r = requests.get(url)
    safe_name = word.replace(" ", "_").replace("'", "").replace("?", "")
    with open(f"static/asl_gifs/daily/{safe_name}.gif", "wb") as f:
        f.write(r.content)
    print(f"Downloaded {word} daily GIF")

# 4️⃣ Daily Verbs
MORE_DAILY_VERBS = {
    "EAT": "eat.gif",
    "DRINK": "drink.gif",
    "WAKE UP": "wakeup.gif",
    "GET UP": "getup.gif",
    "WASH": "wash.gif",
    "SHOWER": "shower.gif",
    "BRUSH TEETH": "brushtheeth.gif",
    "GO": "go.gif",
    "COME": "come.gif",
}

for word, filename in MORE_DAILY_VERBS.items():
    url = f"https://www.lifeprint.com/asl101/gifs/{filename}"
    r = requests.get(url)
    safe_name = word.replace(" ", "_").replace("'", "").replace("?", "")
    with open(f"static/asl_gifs/daily_verbs/{safe_name}.gif", "wb") as f:
        f.write(r.content)
    print(f"Downloaded {word} verb GIF")

print("✅ All Lifeprint GIFs downloaded successfully!")