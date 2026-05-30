import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from mail import send_test

load_dotenv()

app = Flask(__name__)


@app.post("/mail/test")
def mail_test():
    data = request.get_json(force=True, silent=True) or {}
    to = data.get("to", "user@example.test")
    subject = data.get("subject", "Flask + Mailexam")
    body = data.get("body", "Mailexam test from Flask")

    send_test(to=to, subject=subject, body=body)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    host = os.environ.get("HTTP_HOST", "127.0.0.1")
    port = int(os.environ.get("HTTP_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
