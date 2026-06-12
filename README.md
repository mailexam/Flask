# Flask + Mailexam

Minimal [Flask](https://flask.palletsprojects.com/) example that sends test mail through [Mailexam](https://mailexam.io/) SMTP via the Python standard library [`smtplib`](https://docs.python.org/3/library/smtplib.html).

Based on the [Mailexam Flask guide](https://wiki.mailexam.ru/en/examples/flask/).

## What you need

- A Mailexam account and a project with SMTP credentials.
- Python 3.10+ and pip.

From your Mailexam welcome email or dashboard:

| Variable | Description |
|----------|-------------|
| `MAILEXAM_LOGIN` | SMTP login (for example, `xxxxx`) |
| `MAILEXAM_PASSWORD` | SMTP password (paired with the login) |
| Host | `{MAILEXAM_LOGIN}.mailexam.io` (built automatically in code) |

## Quick start (host)

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

3. Edit `.env`:

```env
MAILEXAM_LOGIN=YOUR_LOGIN
MAILEXAM_PASSWORD=YOUR_PASSWORD
MAILEXAM_PORT=587
MAIL_FROM=noreply@example.test
```

4. Run the server:

```bash
python app.py
```

The server listens on `http://127.0.0.1:5000` by default.

5. Send a test message:

```bash
curl -X POST http://127.0.0.1:5000/mail/test \
  -H 'Content-Type: application/json' \
  -d '{"to":"user@example.test","subject":"Test","body":"Hello"}'
```

The message appears in the Mailexam dashboard → your project → inbox.

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MAILEXAM_LOGIN` | yes | — | SMTP login; also used to build the host name |
| `MAILEXAM_PASSWORD` | yes | — | SMTP password |
| `MAILEXAM_PORT` | no | `587` | SMTP port (`587`, `2525`, or `25`) |
| `MAIL_FROM` | no | `noreply@example.test` | Sender address (any test address is fine) |
| `HTTP_HOST` | no | `127.0.0.1` | HTTP bind address |
| `HTTP_PORT` | no | `5000` | HTTP listen port |
| `FLASK_DEBUG` | no | `0` | Set to `1` to enable Flask debug mode |

For port **587** the code calls `starttls()` before login. For port **25** it connects without STARTTLS.

## Project layout

```
.
├── requirements.txt
├── mail.py            # smtplib transport and send_test()
├── app.py             # Flask app and POST /mail/test
├── .env.example
├── Dockerfile         # for local debugging only
└── docker-compose.yml
```

## Docker (debugging)

Docker is provided for local debugging. For day-to-day development, run the app on the host with `python app.py` (see above).

```bash
cp .env.example .env
# edit .env with your credentials

docker compose up --build
```

Then call the same endpoint on the mapped port:

```bash
curl -X POST http://127.0.0.1:5000/mail/test \
  -H 'Content-Type: application/json' \
  -d '{"to":"user@example.test","subject":"Test","body":"Hello"}'
```

Inside the container the server binds to `0.0.0.0:5000` so the port mapping works.

## CI

Set these secrets in your CI environment:

```yaml
variables:
  MAILEXAM_LOGIN: $MAILEXAM_LOGIN
  MAILEXAM_PASSWORD: $MAILEXAM_PASSWORD
  MAILEXAM_PORT: "587"
  MAIL_FROM: "noreply@example.test"
```

After sending a message in a test, verify delivery via the [Mailexam API](https://mailexam.io/api).

## Troubleshooting

**TLS or connection error**

- Host must be `{login}.mailexam.io`, where `{login}` matches `MAILEXAM_LOGIN`.
- Login and password must come from the same Mailexam project.
- For port **587** call `starttls()` before `login()`.

**Environment variables not picked up**

- Call `load_dotenv()` before reading `os.environ` (already done in `app.py`).

**Message not in the dashboard**

- Open the inbox of the same Mailexam project.
- Check Flask logs and traceback on send.

**Port already in use**

- Change `HTTP_PORT` in `.env` or pass a different port when starting the app.

## See also

- [Mailexam Flask guide (wiki)](https://wiki.mailexam.ru/en/examples/flask/)
- [FastAPI reference implementation](https://github.com/mailexam/FastAPI) — same `mail.py` module, async route
- [Flask documentation](https://flask.palletsprojects.com/)
- [Mailexam API documentation](https://mailexam.io/api)

## License

Apache 2.0
