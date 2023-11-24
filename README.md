# 2daw-m12-p1-s1-examples

Exemples de suport per l'sprint 1 del projecte 1 dins del mòdul de projecte (M12) de 2n de DAW.

## Setup

### Python Virtual Environment

Crea l'entorn:

    python3 -m venv .venv

L'activa:

    source .venv/bin/activate

Instal·la el requisits:

    pip install -r requirements.txt

Per a generar el fitxer de requiriments:

    pip freeze > requirements.txt

Per desactivar l'entorn:

    deactivate

### Base de dades

Crea una base de dades SQLite a partir de l'script [0_tables.sql](./sqlite/0_tables.sql). Tens una d'exemple creada amb les dades del fitxer [1_mock_data.sql](./sqlite/1_mock_data.sql). Hi ha dos usuaris de prova i tots dos tenen com a contrasenya `patata`:

* `voltaire@alumnat.cat` que té el rol de `viewer`, sols lectura.
* `edison@alumnat.cat` que té el rol `editor`, per llegir i modificar dades.

### Fitxer de configuració

Crea un fitxer `.env` amb els paràmetres de configuració. Pots fer servir el fitxer [.env.exemple](./.env.exemple).

## Run

Executa:

    flask run --debug

I obre un navegador a l'adreça: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Debug amb Visual Code

Des de l'opció de `Run and Debug`, crea un fitxer animenat `launch.json` amb el contingut següent:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "MY APP",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "wsgi.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
