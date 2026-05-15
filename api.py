from fastapi import FastAPI
import json
import os

app = FastAPI()

def load(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

@app.post("/add")
def add_data(data: dict):
    teachers = load("teachers.json")
    subjects = load("subjects.json")

    teachers.extend(data.get("teachers", []))
    subjects.extend(data.get("subjects", []))

    save("teachers.json", teachers)
    save("subjects.json", subjects)

    return {"status": "ok"}
