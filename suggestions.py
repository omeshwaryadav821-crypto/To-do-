"""
Smart suggestions and mascot cheers for Mochi Tasks.
"""

import re
import random

QUICK_SUGGESTIONS = [
    {"title": "Drink a glass of water 💧", "category": "Health"},
    {"title": "5-minute stretch break 🧘", "category": "Health"},
    {"title": "Clear and wipe desk 🌿", "category": "Personal"},
    {"title": "10-minute focused inbox check 📬", "category": "Work"},
    {"title": "Quick walk outside 🚶", "category": "Health"},
    {"title": "Read 5 pages of a book 📖", "category": "Personal"}
]

CHEERS = [
    "Yay! You crushed it! 🎉",
    "Great job! So proud of you! ✨",
    "Another task done! You're on fire! 🌟",
    "Woohoo! Check that off! 💖",
    "Boom! +20 XP! Keep the streak going! 🚀",
    "Look at your momentum! High five! 🐾"
]

PET_CHEERS = [
    "Hehe, that tickles! 🌸",
    "Purrr~ You're doing awesome today! ✨",
    "Mochi believes in you 100%! 🌈",
    "Stay hydrated and keep smiling! 💧",
    "Cheering for you from the sidelines! 📣"
]

def get_quick_suggestions():
    return QUICK_SUGGESTIONS

def get_random_cheer():
    return random.choice(CHEERS)

def get_pet_cheer():
    return random.choice(PET_CHEERS)

def break_down_task(title):
    t = (title or "").lower()
    
    if any(k in t for k in ["study", "exam", "read", "learn", "homework", "class"]):
        return [
            {"id": 1, "text": "Set a 25-minute focus timer and open materials", "completed": False},
            {"id": 2, "text": "Review and summarize 2-3 key concepts", "completed": False},
            {"id": 3, "text": "Test self on key questions", "completed": False}
        ]
    elif any(k in t for k in ["clean", "wash", "tidy", "dishes", "laundry", "room"]):
        return [
            {"id": 1, "text": "Put away misplaced items first", "completed": False},
            {"id": 2, "text": "Wipe down primary surface or counter", "completed": False},
            {"id": 3, "text": "Take out trash or put laundry away", "completed": False}
        ]
    elif any(k in t for k in ["write", "essay", "email", "report", "doc", "draft"]):
        return [
            {"id": 1, "text": "Jot down a quick 3-bullet outline", "completed": False},
            {"id": 2, "text": "Write unedited rough first draft", "completed": False},
            {"id": 3, "text": "Quick proofread and hit send/save", "completed": False}
        ]
    elif any(k in t for k in ["gym", "workout", "run", "walk", "exercise"]):
        return [
            {"id": 1, "text": "Put on athletic shoes and warm up 3 mins", "completed": False},
            {"id": 2, "text": "Complete 15-20 min active routine", "completed": False},
            {"id": 3, "text": "Hydrate and stretch", "completed": False}
        ]
    else:
        return [
            {"id": 1, "text": "Gather tools and remove distractions", "completed": False},
            {"id": 2, "text": f"Work on core action of '{title.strip()}' for 15 mins", "completed": False},
            {"id": 3, "text": "Review result and check it off", "completed": False}
        ]
