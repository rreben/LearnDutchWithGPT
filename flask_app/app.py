# app.py
from flask import Flask, request, render_template, redirect, url_for
from flask import send_from_directory
import os
import json

app = Flask(__name__)

DATA_FILE = "data.json"


# Hilfsfunktion zum Laden der JSON-Datei
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# Hilfsfunktion zum Speichern der JSON-Datei
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Endpunkt zum Abrufen der JSON-Daten
@app.route("/", methods=["GET"])
def index():
    data = load_data()
    lesson = data.get("lesson", {})
    title = lesson.get("title", {}).get("text", "")
    description = lesson.get("description", {}).get("text", "")
    exercises = lesson.get("exercises", [])
    return render_template(
        "index.html", title=title, description=description, exercises=exercises
    )


# Endpunkt zum Hinzufügen neuer Daten
@app.route("/add", methods=["POST"])
def add_data():
    data = load_data()
    new_title = request.form.get("new_title")
    new_description = request.form.get("new_description")
    new_exercise = request.form.get("new_exercise")
    if "lesson" not in data:
        data["lesson"] = {"title": {}, "description": {}, "exercises": []}
    if new_title:
        data["lesson"]["title"] = {"text": new_title, "language_code": "de"}
    if new_description:
        data["lesson"]["description"] = {"text": new_description, "language_code": "de"}
    if new_exercise:
        exercise = {
            "explanation": {"text": new_exercise, "language_code": "de"},
            "tasks": []
        }
        data["lesson"]["exercises"].append(exercise)
    save_data(data)
    return redirect(url_for("index"))


# Endpunkt zum Hinzufügen einer neuen Aufgabe zu einer Übung
@app.route("/add_task/<int:exercise_index>", methods=["POST"])
def add_task(exercise_index):
    data = load_data()
    new_task = request.form.get("new_task")
    new_solution = request.form.get("new_solution")
    if "lesson" in data and 0 <= exercise_index < len(data["lesson"]["exercises"]):
        task = {
            "teacher_speaks": {"text": new_task, "language_code": "nl"},
            "student_response_time": 5000,
            "teacher_solution": {"text": new_solution, "language_code": "nl"},
            "play_separator_tone": True
        }
        data["lesson"]["exercises"][exercise_index]["tasks"].append(task)
    save_data(data)
    return redirect(url_for("index"))


# Endpunkt zum Löschen von Daten
@app.route("/delete/<int:exercise_index>", methods=["POST"])
def delete_data(exercise_index):
    data = load_data()
    if "lesson" in data and "exercises" in data["lesson"] and 0 <= exercise_index < len(data["lesson"]["exercises"]):
        data["lesson"]["exercises"].pop(exercise_index)
        save_data(data)
    return redirect(url_for("index"))


# Favicon Route
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
