from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
app = Flask(__name__)
CORS(app)

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

@app.route("/")
def home():
    return "Welcome to the Productivity Assistant Backend!"

@app.route("/tasks/prioritize", methods=["POST"])
def prioritize_tasks():
    tasks = request.json.get("tasks", [])
    if not tasks:
        return jsonify({"error": "No tasks provided"}), 400
    
    tasks_formatted = "\n".join([f"- {task}" for task in tasks])
    print(tasks_formatted)
    prompt = (
        "You are a helpful assistant. Prioritize the following tasks based on importance and deadlines. "
        "Only use the tasks provided in the list. Do not add, modify, or elaborate on the tasks. "
        "Return the response in the format: '1. Task A, 2. Task B, 3. Task C'.\n\n"
        f"Tasks:\n{tasks_formatted}"
    )


    try:
        response = generator(prompt, max_length=150, num_return_sequences=1, truncation=True)
        prioritized_tasks = response[0]["generated_text"].strip()
        lines = prioritized_tasks.split("\n")
        prioritized_tasks_cleaned = "\n".join(
            line for line in lines if line.strip().startswith(("- ", "1.", "2.", "3."))
        )
        return jsonify({"prioritized_tasks": prioritized_tasks_cleaned})
    except Exception as e:
        import traceback
        return jsonify({"error": traceback.format_exc()}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
