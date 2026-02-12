# CapJS Service

Il servizio `capjs` è il cuore del sistema RER Captcha. Gestisce la generazione delle sfide captcha e la verifica dei token risolti.

## API Endpoints

### 1. Verifica Token

Verifica se un token inviato dal client è valido.

- **URL**: `/:site_key/siteverify`
- **Metodo**: `POST`
- **Parametri (Form Data)**:
  - `secret`: La `SECRET_KEY` del sito.
  - `response`: Il token generato dal widget CapJS.
- **Risposta**:
  ```json
  {
    "success": true | false,
    "challenge_ts": "timestamp",
    "hostname": "hostname",
    "error-codes": [...] //opzionale
  }
  ```

## Configurazione

Il servizio può essere configurato tramite variabili d'ambiente:

- `PORT`: Porta su cui il servizio ascolta (default: `3000`).
- `DATABASE_URL`: URL per la connessione al database (se applicabile).

## Deployment

Il servizio è containerizzato tramite Docker. Vedere il file `Dockerfile` nella directory `standalone` per i dettagli della build.

In ambiente di sviluppo, viene solitamente eseguito insieme a un container `nginx` che funge da reverse proxy per gestire il traffico pubblico e fornire gli asset statici del widget.

## Widget Client-side

Per integrare il widget nel frontend, è necessario caricare lo script JavaScript fornito dal servizio (solitamente tramite il proxy Nginx).

Esempio di caricamento:

```html
<script src="http://localhost:3000/api.js" async defer></script>
```

_(Nota: L'URL esatto dipende dalla configurazione del proxy)_
