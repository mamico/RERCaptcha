import json
from flask import Flask, render_template_string, request
import requests
import os
import time

app = Flask(__name__)

# spostare su env
CAPJS_INTERNAL_URL = os.environ.get("CAPJS_INTERNAL_URL", "http://capjs:3000")
CAPJS_PUBLIC_URL = os.environ.get("CAPJS_PUBLIC_URL", "http://localhost:3000")
CAPJS_SITE_KEY = os.environ.get("SITE_KEY")
CAPJS_SECRET = os.environ.get("SECRET_KEY")

FORM_TEMPLATE = """
<!doctype html>
<html>
  <body>  
    <h1>Form con CapJS</h1>
    <form action="/" method="post">
      <cap-widget 
        id="cap" 
        data-cap-api-endpoint="{{ capjs_public_url }}/{{site_key}}/"
        data-cap-hidden-field-name="capjs-token"></cap-widget>
      <input type="text" name="username" placeholder="Username"><br><br>
      <br>
      <button type="submit">Invia</button>
    </form>
    <script>
      window.CAP_CUSTOM_WASM_URL = "{{ capjs_public_url }}/assets/cap_wasm.js";
    </script>
    <script src="https://cdn.jsdelivr.net/npm/@cap.js/widget"></script>
    <!-- <script src="{{ capjs_public_url }}/assets/widget.js"></script> -->
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        token = request.form.get("capjs-token")
        username = request.form.get("username")

        if not token:
            return "Errore: token mancante", 400

        resp = requests.post(
            f"{CAPJS_INTERNAL_URL}/verify",
            data={"secret": CAPJS_SECRET, "response": token},
            timeout=5
        )
        result = resp.json()
        if result.get("success"):
            return f"Captcha OK ✅, utente: {username}"
        return f"Captcha NON valido ❌: {result}"

    return render_template_string(
      FORM_TEMPLATE, 
      capjs_public_url=CAPJS_PUBLIC_URL, 
      site_key=CAPJS_SITE_KEY,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

