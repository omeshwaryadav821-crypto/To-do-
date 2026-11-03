#!/usr/bin/env python3
"""
Mochi Tasks Server - Minimalist, functional self-hosted Python web app.
Zero dependencies. Standard library only (http.server, sqlite3, json).
"""

import sys
import os
import json
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta

import database as db
import suggestions as sug

PORT = 5000
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


class MochiHandler(BaseHTTPRequestHandler):
    """Bulletproof request handler with mandatory Content-Length and CORS."""

    def _send_response_bytes(self, status, content_type, data_bytes):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data_bytes)

    def _send_json(self, data, status=200):
        json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self._send_response_bytes(status, "application/json; charset=utf-8", json_bytes)

    def _send_error(self, message, status=400):
        self._send_json({"error": str(message)}, status=status)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception as e:
            return None

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path == "/api/tasks":
                status = query.get("status", [None])[0]
                search = query.get("search", [None])[0]
                tasks = db.get_all_tasks(filter_status=status, search=search)
                self._send_json(tasks)

            elif path == "/api/reminders/due":
                due = db.get_due_reminders()
                self._send_json(due)

            elif path == "/api/suggestions/quick":
                self._send_json(sug.get_quick_suggestions())

            elif path == "/api/creature":
                self._send_json(db.get_creature_stats())

            elif path.startswith("/api/"):
                self._send_error("API endpoint not found", 404)

            else:
                self._serve_static(path)

        except Exception as e:
            self._send_error(f"Server error: {str(e)}", 500)

    def do_POST(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            body = self._read_json()

            if body is None:
                self._send_error("Invalid JSON body", 400)
                return

            if path == "/api/tasks":
                title = body.get("title", "").strip()
                if not title:
                    self._send_error("Title cannot be empty", 400)
                    return
                category = body.get("category", "General")
                reminder_at = body.get("reminder_at") or None
                subtasks = body.get("subtasks", [])
                new_task = db.create_task(title, category, reminder_at, subtasks)
                creature = db.get_creature_stats()
                self._send_json({"task": new_task, "creature": creature}, 201)

            elif path.startswith("/api/tasks/") and path.endswith("/toggle"):
                parts = path.split("/")
                task_id = int(parts[3])
                task, creature = db.toggle_task(task_id)
                if not task:
                    self._send_error("Task not found", 404)
                    return
                cheer = sug.get_random_cheer() if task["status"] == "completed" else "Task unchecked!"
                self._send_json({"task": task, "creature": creature, "cheer": cheer})

            elif path.startswith("/api/tasks/") and path.endswith("/snooze"):
                parts = path.split("/")
                task_id = int(parts[3])
                minutes = body.get("minutes", 15)
                new_time = (datetime.now() + timedelta(minutes=minutes)).isoformat()
                updated = db.snooze_task_reminder(task_id, new_time)
                self._send_json(updated)

            elif path.startswith("/api/tasks/") and path.endswith("/clear-reminder"):
                parts = path.split("/")
                task_id = int(parts[3])
                updated = db.clear_task_reminder(task_id)
                self._send_json(updated)

            elif path == "/api/suggestions/breakdown":
                title = body.get("title", "")
                steps = sug.break_down_task(title)
                self._send_json({"subtasks": steps})

            elif path == "/api/creature/pet":
                creature = db.pet_creature()
                cheer = sug.get_pet_cheer()
                self._send_json({"creature": creature, "cheer": cheer})

            else:
                self._send_error("Endpoint not found", 404)

        except Exception as e:
            self._send_error(f"Error processing request: {str(e)}", 500)

    def do_PUT(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            body = self._read_json()

            if path.startswith("/api/tasks/") and path.endswith("/subtasks"):
                parts = path.split("/")
                task_id = int(parts[3])
                subtasks = body.get("subtasks", [])
                updated = db.update_task_subtasks(task_id, subtasks)
                self._send_json(updated)
            else:
                self._send_error("Endpoint not found", 404)

        except Exception as e:
            self._send_error(f"Error on PUT: {str(e)}", 500)

    def do_DELETE(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path

            if path.startswith("/api/tasks/"):
                parts = path.split("/")
                if len(parts) == 4 and parts[3].isdigit():
                    task_id = int(parts[3])
                    db.delete_task(task_id)
                    self._send_json({"success": True})
                else:
                    self._send_error("Invalid task ID", 400)
            else:
                self._send_error("Endpoint not found", 404)

        except Exception as e:
            self._send_error(f"Error on DELETE: {str(e)}", 500)

    def _serve_static(self, path):
        clean = "index.html" if path in ["", "/"] else path.lstrip("/")
        full_path = os.path.normpath(os.path.join(STATIC_DIR, clean))

        # Security check: stay within STATIC_DIR
        if not full_path.startswith(STATIC_DIR) or not os.path.exists(full_path) or os.path.isdir(full_path):
            full_path = os.path.join(STATIC_DIR, "index.html")

        if not os.path.exists(full_path):
            self._send_error("Static file not found", 404)
            return

        mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type:
            if full_path.endswith(".css"):
                mime_type = "text/css"
            elif full_path.endswith(".js"):
                mime_type = "application/javascript"
            else:
                mime_type = "text/plain"

        try:
            with open(full_path, "rb") as f:
                content = f.read()
            self._send_response_bytes(200, f"{mime_type}; charset=utf-8", content)
        except Exception as e:
            self._send_error(f"Failed to read file: {str(e)}", 500)

    def log_message(self, format, *args):
        # Quiet clean logging
        pass


def run_server():
    db.init_db()
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, MochiHandler)
    print(f"""
    ========================================================================
       ✨ MOCHI TASKS - SERVER READY ✨
       Minimalist & Reliable To-Do with Mascot Companion
       
       ✦ Web Interface:  http://localhost:{PORT}
       ✦ Local Address:  http://127.0.0.1:{PORT}
       ✦ Database:       {db.DB_PATH}
    ========================================================================
    """)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
