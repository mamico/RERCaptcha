import json
from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

# spostare su env
CAPJS_INTERNAL_URL = os.environ.get("CAPJS_INTERNAL_URL", "http://capjs:3000")
CAPJS_PUBLIC_URL = os.environ.get("CAPJS_PUBLIC_URL", "http://localhost:3000")
CAPJS_SITE_KEY = os.environ.get("SITE_KEY")
CAPJS_SECRET = os.environ.get("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visible-it", methods=["GET", "POST"])
def visible_it():
    message = ""
    status_code = 200
    if request.method == "POST":
        token = request.form.get("capjs-token")
        text = request.form.get("text")

        if not token:
            # return "Errore: token mancante", 400
            message = "Errore: token mancante"
            status_code = 400

        res = requests.post(
            f"{CAPJS_INTERNAL_URL}/{CAPJS_SITE_KEY}/siteverify",
            data={"secret": CAPJS_SECRET, "response": token},
            timeout=5
        )
        if res:
            result = res.json()
            if result.get("success"):
                message = f"Captcha OK ✅, campo di testo: {text}, token: {token}, captcha_result: {json.dumps(result)}"
                status_code = 200
            else:
                message = f"Captcha NON valido ❌: {result}, token: {token}, captcha_result: {json.dumps(result)}"
                status_code = 400
        else:
            message = f"Errore non previsto nella verifica del token: {token} status: {res.status_code} text: {res.text}"
            status_code = res.status_code

    return render_template(
      "visible-it.html", 
      capjs_public_url=CAPJS_PUBLIC_URL, 
      site_key=CAPJS_SITE_KEY,
      message=message,
    ), status_code


@app.route("/invisible", methods=["GET", "POST"])
def invisible():
    message = ""
    status_code = 200
    if request.method == "POST":
        token = request.form.get("capjs-token")
        text = request.form.get("text")

        if not token:
            # return "Errore: token mancante", 400
            message = "Errore: token mancante"
            status_code = 400

        res = requests.post(
            f"{CAPJS_INTERNAL_URL}/{CAPJS_SITE_KEY}/siteverify",
            data={"secret": CAPJS_SECRET, "response": token},
            timeout=5
        )
        if res:
            result = res.json()
            if result.get("success"):
                message = f"Captcha OK ✅, campo di testo: {text}, token: {token}, captcha_result: {json.dumps(result)}"
                status_code = 200
            else:
                message = f"Captcha NON valido ❌: {result}, token: {token}, captcha_result: {json.dumps(result)}"
                status_code = 400
        else:
            message = f"Errore non previsto nella verifica del token: {token} status: {res.status_code} text: {res.text}"
            status_code = res.status_code

    return render_template(
      "invisible.html",
      capjs_public_url=CAPJS_PUBLIC_URL,
      site_key=CAPJS_SITE_KEY,
      message=message,
    ), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

