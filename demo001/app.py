import json
from flask import Flask, render_template, request
import requests
import os
import secrets

app = Flask(__name__)

# spostare su env
CAPJS_INTERNAL_URL = os.environ.get("CAPJS_INTERNAL_URL", "http://capjs:3000")
CAPJS_PUBLIC_URL = os.environ.get("CAPJS_PUBLIC_URL", "http://localhost:3000")
CAPJS_SITE_KEY = os.environ.get("SITE_KEY")
CAPJS_SECRET = os.environ.get("SECRET_KEY")

def get_random_urlsafe_string(length):
    return secrets.token_urlsafe(length)[:length]

def configure_app_headers(app):
    def _make_nonce():
        if not getattr(request, 'csp_nonce', None):
            request.csp_nonce = get_random_urlsafe_string(18)
        request.csp_nonce_cap = get_random_urlsafe_string(18)
        print(f"Nonce: {request.csp_nonce}")
    def _add_security_headers(resp):
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        # resp.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'strict-dynamic'"
        # resp.headers["Content-Security-Policy"] = "script-src 'strict-dynamic'"
        # resp.headers["Content-Security-Policy"] = f"script-src {CAPJS_PUBLIC_URL}; script-src-elem "
        # resp.headers["Content-Security-Policy"] = "script-src ; script-src-elem "  
        resp.headers["Content-Security-Policy"] = "script-src {CAPJS_PUBLIC_URL}"  
        csp_header = resp.headers.get('Content-Security-Policy')
        if csp_header and 'nonce' not in csp_header:
            resp.headers['Content-Security-Policy'] = \
                csp_header.replace('script-src ', f"script-src 'nonce-{request.csp_nonce}' 'nonce-{request.csp_nonce_cap}' ")
            # csp_header = resp.headers.get('Content-Security-Policy')
            # resp.headers['Content-Security-Policy'] = \
            #     csp_header.replace('script-src-elem ', f"script-src-elem 'nonce-{request.csp_nonce}' ")
        return resp
    app.before_request(_make_nonce)
    app.after_request(_add_security_headers)

configure_app_headers(app)


@app.route("/")
def index():
    return render_template("index.html", capjs_public_url=CAPJS_PUBLIC_URL)

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
            status_code = 404  # altri errrori vengonoinetercettati da LBL res.status_code
        else:
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
                    status_code = 404  # altri errrori vengonoinetercettati da LBL res.status_code
            else:
                message = f"Errore non previsto nella verifica del token: {token} status: {res.status_code} text: {res.text}"
                status_code = 404  # altri errrori vengonoinetercettati da LBL res.status_code

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
            # return "Errore: token mancante", 400 (400 viene intercettato da LBL)
            message = "Errore: token mancante"
            status_code = 404
        else:
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
                    status_code = 404
            else:
                message = f"Errore non previsto nella verifica del token: {token} status: {res.status_code} text: {res.text}"
                status_code = 404  # altri errrori vengonoinetercettati da LBL res.status_code

    return render_template(
      "invisible.html",
      capjs_public_url=CAPJS_PUBLIC_URL,
      site_key=CAPJS_SITE_KEY,
      message=message,
    ), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

