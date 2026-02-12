# RER Captcha

RER Captcha è una soluzione di protezione captcha basata sul framework open-source **CapJS**. Questo repository contiene il servizio core e un'applicazione di esempio per facilitare l'integrazione.

## Architettura

Il progetto è composto da due componenti principali:

1.  **[capjs](file:///home/mauro/Work/RER/rercaptcha/capjs/README.md)**: Il servizio core che genera e verifica i captcha.
2.  **[demo001](file:///home/mauro/Work/RER/rercaptcha/demo001/README.md)**: Un'applicazione web Python/Flask che mostra come integrare CapJS in un form reale.

I servizi sono orchestrati tramite Docker Compose per semplificare lo sviluppo e il deployment locale.

## Guida alla Configurazione Rapida

Segui questi passaggi per avviare il sistema e testare la demo.

### 1. Requisiti

- Docker
- Docker Compose

### 2. Inizializzazione delle Chiavi

CapJS richiede una coppia di chiavi (`SITE_KEY` e `SECRET_KEY`) per funzionare. Queste vengono generate automaticamente al primo avvio.

```bash
# Avvia il core e il tool di inizializzazione
docker-compose up -d capjs demo-init
```

Attendi qualche secondo, quindi recupera le chiavi generate:

```bash
cat shared/site.json
```

L'output sarà simile a questo:

```json
{
  "site_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "secret_key": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
}
```

### 3. Configurazione della Demo

Aggiorna il file `compose.yml` (o crea un file `.env` se supportato) con le chiavi ottenute.

```yaml
services:
  demo001:
    build: ./demo001
    ports:
      - "5001:5000"
    environment:
      SITE_KEY: "LA_TUA_SITE_KEY"
      SECRET_KEY: "LA_TUA_SECRET_KEY"
    depends_on:
      - capjs
```

### 4. Avvio della Demo

```bash
docker-compose up -d demo001
```

### 5. Accesso

Visita `http://localhost:5001` per vedere il captcha in azione.

## Documentazione Componenti

- [Documentazione Servizio CapJS](file:///home/mauro/Work/RER/rercaptcha/capjs/README.md)
- [Documentazione Demo Flask](file:///home/mauro/Work/RER/rercaptcha/demo001/README.md)
