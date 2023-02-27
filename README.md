# Turkey Learning Initiative Telegram Bot

### Instructions

Create your own `.env` file by `cp .env.sample .env` and modify.
Install dependencies
```shell
poetry install
```

Run Telegram Bot
```shell
poetry run bot  # python -m tlibot
```

Run Telegram Bot with FastApi
```shell
poetry run api  # uvicorn api.main:app --reload
```

Test your endpoint:
`http://localhost:8000/say_hello?text=Hello!+Telegram`
