# Demo 001 - Flask Integration

Questa è un'applicazione web minimale scritta in Python usando Flask. Mostra come integrare il widget CapJS e come verificare il token sul lato server.

## Requisiti

- Python 3.x
- Flask
- Requests

## Struttura del Form

Il widget CapJS viene integrato inserendo un elemento `<div>` dedicato e caricando lo script `api.js`.

### Versione Visibile

Vedere il template `templates/visible-it.html`. Il form include:

```html
<div class="capjs-captcha" data-sitekey="{{ site_key }}"></div>
```

### Versione Invisibile

Vedere il template `templates/invisible.html`. Il captcha viene attivato programmaticamente.

## Verifica Lato Server

Quando il form viene inviato, il widget inserisce un token nel campo `capjs-token`. L'applicazione Flask recupera questo token e lo invia al servizio interno `capjs` per la validazione.

Esempio di codice (da `app.py`):

```python
res = requests.post(
    f"{CAPJS_INTERNAL_URL}/{CAPJS_SITE_KEY}/siteverify",
    data={"secret": CAPJS_SECRET, "response": token},
    timeout=5,
)
result = res.json()
if result.get("success"):
    # Token valido!
else:
    # Token non valido
```

## Sicurezza (Content Security Policy)

L'applicazione implementa una CSP rigorosa che richiede l'uso di un `nonce` per gli script e permette l'esecuzione del codice WebAssembly (richiesto da CapJS). Vedere la funzione `configure_app_headers` in `app.py`.
