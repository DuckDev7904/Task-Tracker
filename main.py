import argparse
import json
import os
import datetime

# Set default filename as a constant
DEFAULT_JSON_FILE = "tasks.json"

class TaskTracker:
    def __init__(self, json_file=DEFAULT_JSON_FILE):
        self.json_file = json_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.json_file):
            with open(self.json_file, "w") as f:
                json.dump([], f)

    def _load_tasks(self):
        with open(self.json_file, "r") as f:
            return json.load(f)

    def _save_tasks(self, tasks):
        with open(self.json_file, "w") as f:
            json.dump(tasks, f, indent=4)

    def add_task(self, description):
        tasks = self._load_tasks()
        task_id = len(tasks) + 1
        now = datetime.datetime.now().isoformat()
        task = {
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": now,
            "updatedAt": now
        }
        tasks.append(task)
        self._save_tasks(tasks)
        print(f"Task added successfully (ID: {task_id})")

    def update_task(self, task_id, new_description):
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updatedAt"] = datetime.datetime.now().isoformat()
                self._save_tasks(tasks)
                print(f"Task {task_id} updated successfully")
                return
        print("Task not found")

    def delete_task(self, task_id):
        tasks = self._load_tasks()
        tasks = [task for task in tasks if task["id"] != task_id]
        self._save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")

    def change_status(self, task_id, status):
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updatedAt"] = datetime.datetime.now().isoformat()
                self._save_tasks(tasks)
                print(f"Task {task_id} marked as {status}")
                return
        print("Task not found")

    def list_tasks(self, status=None):
        tasks = self._load_tasks()
        filtered_tasks = [task for task in tasks if status is None or task["status"] == status]
        if not filtered_tasks:
            print("No tasks found")
        else:
            for task in filtered_tasks:
                print(f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['createdAt']})")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("command", type=str, help="Command to execute (add, update, delete, mark-in-progress, mark-done, list)")
    parser.add_argument("arguments", nargs="*", help="Additional arguments for the command")

    args = parser.parse_args()

    tracker = TaskTracker(DEFAULT_JSON_FILE)

    if args.command == "add":
        if not args.arguments:
            print("Error: Missing task description")
        else:
            tracker.add_task(" ".join(args.arguments))

    elif args.command == "update":
        if len(args.arguments) < 2:
            print("Error: Missing task ID or new description")
        else:
            tracker.update_task(int(args.arguments[0]), " ".join(args.arguments[1:]))

    elif args.command == "delete":
        if not args.arguments:
            print("Error: Missing task ID")
        else:
            tracker.delete_task(int(args.arguments[0]))

    elif args.command == "mark-in-progress":
        if not args.arguments:
            print("Error: Missing task ID")
        else:
            tracker.change_status(int(args.arguments[0]), "in-progress")

    elif args.command == "mark-done":
        if not args.arguments:
            print("Error: Missing task ID")
        else:
            tracker.change_status(int(args.arguments[0]), "done")

    elif args.command == "list":
        if not args.arguments:
            tracker.list_tasks()
        else:
            status = args.arguments[0]
            if status not in ["todo", "in-progress", "done"]:
                print("Error: Invalid status. Use 'todo', 'in-progress', or 'done'")
            else:
                tracker.list_tasks(status)

    else:
        print("Error: Unknown command")


if __name__ == "__main__":
    main()
