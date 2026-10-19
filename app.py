
from flask import Flask, render_template
from pathlib import Path
import json

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    dashboard_data = load_json("dashboard.json")

    return render_template(
        "dashboard.html",
        data=dashboard_data
    )


@app.route("/analysis")
def analysis():
    analysis_data = load_json("analysis.json")

    return render_template(
        "analysis.html",
        data=analysis_data
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
