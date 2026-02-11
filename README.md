# RER Captcha

Questo progetto contiene un'implementazione di un servizio di captcha "CapJS" e un'applicazione di demo per mostrare come integrarlo.

## Demo 001

`demo001` è un'applicazione web minimale in Python/Flask che mostra come integrare il servizio CapJS in un form HTML.

### Funzionamento

L'applicazione `demo001` renderizza una pagina HTML con un form. Il form include il widget CapJS che, una volta risolto, inserisce un token in un campo nascosto. Quando il form viene inviato, il server Flask riceve il token e lo verifica chiamando l'endpoint `/verify` del servizio `capjs`.

### Come eseguire i test

Per eseguire `demo001` è necessario aggiungerlo al file `compose.yml` e poi avviare i servizi con `docker-compose`.

1.  **Aggiungere il servizio `demo001` a `compose.yml`:**

    Aggiungere la seguente definizione di servizio al file `compose.yml`:

    ```yaml
    services:
      # ... (altri servizi come capjs, demo, demo-init)

      demo001:
        build: ./demo001
        ports:
          - "5001:5000"
        environment:
          # Queste variabili devono essere impostate con i valori generati
          # durante l'inizializzazione del servizio capjs.
          SITE_KEY: "your_site_key"  # Sostituire con la SITE_KEY
          SECRET_KEY: "your_secret_key" # Sostituire con la SECRET_KEY
        depends_on:
          - capjs
    ```

2.  **Ottenere `SITE_KEY` e `SECRET_KEY`:**

    Queste chiavi sono generate dal servizio `capjs`. Per ottenerle, è necessario prima avviare `capjs` e `demo-init` e poi leggere i valori dal file `shared/site.json` che viene creato.

    ```bash
    docker-compose up -d capjs demo-init
    # Attendere qualche secondo per l'inizializzazione
    cat shared/site.json
    ```

    Il file `site.json` conterrà un output simile a questo:

    ```json
    {
        "site_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "secret_key": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
    }
    ```

3.  **Aggiornare `compose.yml`:**

    Sostituire `"your_site_key"` e `"your_secret_key"` nel servizio `demo001` in `compose.yml` con i valori ottenuti dal passo precedente.

4.  **Avviare `demo001`:**

    ```bash
    docker-compose up -d demo001
    ```

5.  **Accedere all'applicazione:**

    Aprire il browser e visitare `http://localhost:5001`. Verrà visualizzato il form con il captcha.
