# json_validation.py

import json

def validate_json_structure(json_data: str) -> bool:
    """
    Validiert die Struktur des JSON-Strings 'json_data'. 
    Gibt True zurück, wenn alles in Ordnung ist, andernfalls False.
    """
    try:
        lesson_data = json.loads(json_data)

        # 1) Top-Level "lesson"
        if "lesson" not in lesson_data:
            raise ValueError("Missing 'lesson' key in JSON data")

        # 2) Titel prüfen
        if "title" not in lesson_data["lesson"]:
            raise ValueError("Missing 'title' key in 'lesson'")
        if not all(k in lesson_data["lesson"]["title"] for k in ["text", "language_code"]):
            raise ValueError("Lesson 'title' must have 'text' and 'language_code'")

        # 3) Beschreibung prüfen
        if "description" not in lesson_data["lesson"]:
            raise ValueError("Missing 'description' key in 'lesson'")
        if not all(k in lesson_data["lesson"]["description"] for k in ["text", "language_code"]):
            raise ValueError("Lesson 'description' must have 'text' and 'language_code'")

        # 4) Übungen prüfen
        if "exercises" not in lesson_data["lesson"]:
            raise ValueError("Missing 'exercises' key in 'lesson'")
        for exercise in lesson_data["lesson"]["exercises"]:
            if "explanation" not in exercise:
                raise ValueError("Each exercise must have an 'explanation'")
            if not all(k in exercise["explanation"] for k in ["text", "language_code"]):
                raise ValueError("Exercise 'explanation' must have 'text' and 'language_code'")

            if "tasks" not in exercise:
                raise ValueError("Each exercise must have a 'tasks' list")

            # 5) Aufgaben prüfen
            for task in exercise["tasks"]:
                if "teacher_speaks" not in task:
                    raise ValueError("Each task must have 'teacher_speaks'")
                if not all(k in task["teacher_speaks"] for k in ["text", "language_code"]):
                    raise ValueError("'teacher_speaks' must have 'text' and 'language_code'")

                if "student_response_time" not in task:
                    raise ValueError("Each task must have 'student_response_time'")

                if "teacher_solution" not in task:
                    raise ValueError("Each task must have 'teacher_solution'")
                if not all(k in task["teacher_solution"] for k in ["text", "language_code"]):
                    raise ValueError("'teacher_solution' must have 'text' and 'language_code'")

                if "play_separator_tone" not in task:
                    raise ValueError("Each task must have 'play_separator_tone'")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON validation error: {e}")
        return False

    return True
