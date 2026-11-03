# ✨ Mochi Tasks
### *Minimalist, Interactive Self-Hosted To-Do with a Cute Mascot Companion*

A minimal, refreshing to-do application designed in clean **shades of white**, **light blue**, and warm **coral accents**. It features **Mochi**, a charming animated cartoon companion who cheers you on, celebrates every completed task with confetti, and levels up as you make progress!

---

## 🌸 Key Features

### 1. 🐾 Mochi the Companion (Appreciates Your Progress!)
- **Animated Cartoon Sprite:** Mochi is an interactive anime-styled cloud/blob spirit with expressive blinking eyes, rosy blush, and a little leaf sprout on top.
- **Progress Reactions:**
  - **Task Completion:** When you complete a task, Mochi does a joyful celebration jump, eyes curve into happy crescents (`^ ^`), and colorful confetti bursts across the screen!
  - **Leveling Up:** Completing tasks awards **+25 XP**. Watch Mochi's XP progress bar fill up and level up your companion!
  - **Petting & Encouragement:** Click or pet Mochi anytime to hear a cute sound effect, gain **+3 XP**, and receive encouraging tips (*"Mochi believes in you 100%! 🌈"*, *"Remember to take mini-breaks and smile! 💖"*).

### 2. 🪄 Smart Suggestions Over To-Do
- **Smart Breakdown Button:** Type any task (e.g. *"Study for biology exam"*, *"Clean apartment"*, *"Prepare presentation"*) and click **🪄 Breakdown**. It automatically splits the task into 3 easy, manageable micro-steps!
- **Quick Boost Ideas Carousel:** One-click suggestions right above your list (e.g., *"💧 Drink a tall glass of cold water"*, *"🧘 2-min shoulder stretch"*, *"🌿 Clear 3 things off your desk"*, *"📬 5-min inbox triage"*).

### 3. ⏰ Reminders & Bells
- **Set Reminders:** Add a reminder with date and time when creating or editing a task.
- **Gentle Audio Chimes:** Synthesized natively using the **Web Audio API** (no external audio files required).
- **Desktop Notifications:** Authorize browser alerts for timely reminders even when working in another window.
- **Snooze Support:** One-click Snooze (+15 minutes) or mark as Done directly from the alert toast.

### 4. 🎨 Minimalist Aesthetic
- **Color Palette:** Soft whites (`#ffffff`, `#f8fafc`), airy light blues (`#e0f2fe`, `#bae6fd`, `#38bdf8`), and warm coral/peach accents (`#ff6b6b`).
- **Interactive Checklists:** Smooth checkboxes, subtasks accordion view, live search, and category filters (*Work*, *Study*, *Personal*, *Health*, *Errands*).

---

## 🚀 Quickstart & Self-Hosting

The application is completely self-contained and runs on the **Python standard library** with **zero external dependencies**.

### 1. Run the Server
From the project folder:
```bash
python3 server.py
```
*(Default port: `5000`)*.

To run on a custom port:
```bash
python3 server.py 8080
```

### 2. Open in Your Browser
Navigate to:
```
http://localhost:5000
```
(or `http://127.0.0.1:5000`)

---

## 📁 Project Structure

```
scholars-codex/
├── server.py              # Zero-dependency Python HTTP server & REST API
├── database.py            # SQLite database (tasks, subtasks, Mochi XP & stats)
├── suggestions.py         # Smart breakdown logic & Mochi cheers
├── test_app.py            # Automated test suite
├── minimal_todo.db        # SQLite database (created automatically)
└── static/
    ├── index.html         # Minimal UI with animated SVG Mochi mascot
    ├── style.css          # Shades of white, light blue, and coral accent
    └── app.js             # Companion interactions, confetti, and sound engine
```
