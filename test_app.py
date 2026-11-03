"""
Automated test suite verifying Mochi Tasks backend and functionality.
"""

import os
import database as db
import suggestions as sug

def test_all():
    print("[1/3] Testing database operations...")
    db.init_db()

    # Initial tasks
    tasks = db.get_all_tasks()
    assert len(tasks) >= 3, f"Expected seeded tasks, got {len(tasks)}"
    print(f"  ✓ Seeded tasks present: {len(tasks)} tasks")

    # Create task
    task = db.create_task("Complete homework assignment", "Study", reminder_at=None, subtasks=[{"id": 1, "text": "Read chapter", "completed": False}])
    assert task is not None
    assert task["title"] == "Complete homework assignment"
    assert len(task["subtasks"]) == 1
    print(f"  ✓ Task created successfully (ID: {task['id']})")

    # Toggle task
    updated, creature = db.toggle_task(task["id"])
    assert updated["status"] == "completed"
    assert creature["xp"] >= 20
    print(f"  ✓ Task toggled to completed, creature rewarded ({creature['xp']} XP, Lv. {creature['level']})")

    # Update subtasks
    updated = db.update_task_subtasks(task["id"], [{"id": 1, "text": "Read chapter", "completed": True}])
    assert updated["subtasks"][0]["completed"] is True
    print("  ✓ Subtask status updated")

    # Pet creature
    pet = db.pet_creature()
    assert pet["xp"] > creature["xp"]
    print(f"  ✓ Creature petted: {pet['xp']} XP")

    # Delete task
    deleted = db.delete_task(task["id"])
    assert deleted is True
    print("  ✓ Task deleted successfully")

    print("\n[2/3] Testing suggestions engine...")
    quick = sug.get_quick_suggestions()
    assert len(quick) >= 4
    print(f"  ✓ Quick suggestions loaded ({len(quick)} ideas)")

    steps = sug.break_down_task("Study for calculus final")
    assert len(steps) == 3
    print(f"  ✓ Task breakdown generated: {len(steps)} steps")

    print("\n[3/3] Checking static files...")
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    for f in ["index.html", "style.css", "app.js"]:
        path = os.path.join(static_dir, f)
        assert os.path.exists(path), f"Missing {f}"
        assert os.path.getsize(path) > 100, f"{f} seems empty"
        print(f"  ✓ {f} verified ({os.path.getsize(path)} bytes)")

    print("\n" + "=" * 50)
    print("✦ ALL TESTS PASSED! APPLICATION FUNCTIONAL ✨")
    print("=" * 50)

if __name__ == "__main__":
    test_all()
