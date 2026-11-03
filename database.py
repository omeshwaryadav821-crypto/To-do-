"""
Simple, robust SQLite database for Mochi Minimal To-Do.
Zero-dependency, uses standard library sqlite3.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minimal_todo.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Tasks table - simple and bulletproof
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                status TEXT DEFAULT 'pending',
                reminder_at TEXT,
                subtasks_json TEXT DEFAULT '[]',
                created_at TEXT NOT NULL
            )
        """)
        
        # Creature stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creature_stats (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                xp INTEGER DEFAULT 20,
                level INTEGER DEFAULT 1
            )
        """)
        
        # Ensure creature exists
        cursor.execute("SELECT COUNT(*) as count FROM creature_stats WHERE id = 1")
        if cursor.fetchone()["count"] == 0:
            cursor.execute("INSERT INTO creature_stats (id, xp, level) VALUES (1, 20, 1)")
            
        # Seed starter tasks if empty
        cursor.execute("SELECT COUNT(*) as count FROM tasks")
        if cursor.fetchone()["count"] == 0:
            now = datetime.now().isoformat()
            starter = [
                ("Welcome to Mochi Tasks! ✨", "General", "pending", None, json.dumps([{"id": 1, "text": "Check off this task to see Mochi celebrate!", "completed": False}]), now),
                ("Drink a glass of water 💧", "Health", "pending", None, "[]", now),
                ("Plan top 3 priorities for today 🎯", "Work", "pending", None, "[]", now)
            ]
            cursor.executemany("""
                INSERT INTO tasks (title, category, status, reminder_at, subtasks_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, starter)
            
        conn.commit()

def get_all_tasks(filter_status=None, search=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if filter_status and filter_status != 'all':
            query += " AND status = ?"
            params.append(filter_status)
            
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")
            
        query += " ORDER BY CASE status WHEN 'pending' THEN 1 ELSE 2 END, id DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        tasks = []
        for r in rows:
            t = dict(r)
            try:
                t["subtasks"] = json.loads(t.get("subtasks_json") or "[]")
            except Exception:
                t["subtasks"] = []
            tasks.append(t)
        return tasks

def get_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            return None
        t = dict(row)
        try:
            t["subtasks"] = json.loads(t.get("subtasks_json") or "[]")
        except Exception:
            t["subtasks"] = []
        return t

def create_task(title, category="General", reminder_at=None, subtasks=None):
    if not title or not title.strip():
        raise ValueError("Title is required")
        
    title = title.strip()
    category = category or "General"
    subtasks = subtasks if isinstance(subtasks, list) else []
    subtasks_json = json.dumps(subtasks)
    now = datetime.now().isoformat()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, category, status, reminder_at, subtasks_json, created_at)
            VALUES (?, ?, 'pending', ?, ?, ?)
        """, (title, category, reminder_at, subtasks_json, now))
        task_id = cursor.lastrowid
        
        # Reward creature 5 XP for creating a task
        cursor.execute("UPDATE creature_stats SET xp = xp + 5 WHERE id = 1")
        conn.commit()
        
    return get_task(task_id)

def toggle_task(task_id):
    task = get_task(task_id)
    if not task:
        return None, None
        
    new_status = "completed" if task["status"] == "pending" else "pending"
    xp_delta = 20 if new_status == "completed" else -20
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        
        # Update creature XP & Level
        cursor.execute("SELECT xp FROM creature_stats WHERE id = 1")
        cur_xp = max(0, cursor.fetchone()["xp"] + xp_delta)
        new_level = (cur_xp // 100) + 1
        cursor.execute("UPDATE creature_stats SET xp = ?, level = ? WHERE id = 1", (cur_xp, new_level))
        conn.commit()
        
    return get_task(task_id), get_creature_stats()

def update_task_subtasks(task_id, subtasks):
    subtasks_json = json.dumps(subtasks if isinstance(subtasks, list) else [])
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET subtasks_json = ? WHERE id = ?", (subtasks_json, task_id))
        conn.commit()
    return get_task(task_id)

def delete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_due_reminders():
    now_iso = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE reminder_at IS NOT NULL 
              AND reminder_at != ''
              AND reminder_at <= ?
              AND status = 'pending'
            ORDER BY reminder_at ASC
        """, (now_iso,))
        return [dict(r) for r in cursor.fetchall()]

def snooze_task_reminder(task_id, new_iso):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET reminder_at = ? WHERE id = ?", (new_iso, task_id))
        conn.commit()
    return get_task(task_id)

def clear_task_reminder(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET reminder_at = NULL WHERE id = ?", (task_id,))
        conn.commit()
    return get_task(task_id)

def get_creature_stats():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT xp, level FROM creature_stats WHERE id = 1")
        row = cursor.fetchone()
        if not row:
            return {"name": "Mochi", "xp": 20, "level": 1, "progress_pct": 20}
        xp = row["xp"]
        level = (xp // 100) + 1
        progress_pct = xp % 100
        return {
            "name": "Mochi",
            "xp": xp,
            "level": level,
            "progress_pct": progress_pct
        }

def pet_creature():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE creature_stats SET xp = xp + 3 WHERE id = 1")
        conn.commit()
    return get_creature_stats()
