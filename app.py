from flask import Flask, render_template, jsonify
import subprocess
import sys
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent

process = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():

    global process

    if process is not None and process.poll() is None:
        return jsonify({
            "message": "Virtual Mouse is already running"
        })

    try:
        process = subprocess.Popen(
            [
                sys.executable,
                str(BASE_DIR / "main.py")
            ],
            cwd=str(BASE_DIR)
        )

        return jsonify({
            "message": "Virtual Mouse started successfully"
        })

    except Exception as error:
        return jsonify({
            "message": str(error)
        }), 500


@app.route("/stop", methods=["POST"])
def stop():

    global process

    if process is not None and process.poll() is None:

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        process = None

        return jsonify({
            "message": "Virtual Mouse stopped"
        })

    return jsonify({
        "message": "Virtual Mouse is not running"
    })


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)