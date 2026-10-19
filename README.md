RESTaurant
===

Django Rest framework + Azure App Service + MySQL + CI/CD by GitHub Actions = test

- Docker: 対応!
- Python: 3.14!
- Linter: Ruff!
- Test: pytest + pytest-django!
- Django: 5.2 LTS!
- Django REST framework: 3.18!

## パッと実行してみたい

```bash
docker compose up --build
# http://localhost:8000/ で API root が見られます。

# 別ターミナルで、ログイン用の管理ユーザを作ります。
docker compose exec web uv run python manage.py createsuperuser --username admin --email admin@example.com
```

lint と test も Docker で回せます。

```bash
docker compose run --rm web uv run ruff check .
docker compose run --rm web uv run ruff format --check .
docker compose run --rm web uv run pytest
```

![readme](https://user-images.githubusercontent.com/28250432/104155388-73050300-542a-11eb-9e16-a9d3fae927d8.png)

## Installation (Docker を使わない場合)

[uv](https://docs.astral.sh/uv/) を使います。

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser --email admin@example.com --username admin
uv run python manage.py runserver
```

## 環境変数

| 名前 | 用途 |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django の SECRET_KEY。開発用設定 (`RESTaurant.settings`) では未設定なら起動時にランダム生成します (runserver の autoreload では同じ値を引き継ぎます)。本番用設定 (`RESTaurant.production`) では必須です。 |
| `WEBSITE_HOSTNAME` | App Service が自動で設定します。これがあると `RESTaurant.production` が使われます。 |
| `DJANGO_DATABASE_NAME` / `DJANGO_DATABASE_USER` / `DJANGO_DATABASE_PASSWORD` / `DJANGO_DATABASE_SERVER` | 本番用 MySQL の接続情報です。 |

## What are included

- [Official tutorials](https://www.django-rest-framework.org/tutorial/quickstart/)
- Continuous deployment and schedule api call using GitHub Actions
    - CI (`.github/workflows/ci.yml`): push と pull request で Ruff と pytest を回し、 Docker image の build も確認します。
    - Azure App Service へのデプロイ (`.github/workflows/workflow.yml`) と定期実行 (`.github/workflows/schedule.yml`) は、 push のたびに勝手に動かないよう手動実行 (`workflow_dispatch`) のみにしています。
    - デプロイには GitHub secrets の `DJANGO_SECRET_KEY` が必要です (App Service のアプリ設定に渡します)。
- Custom command
    - `/commands/samplecommand/` と `/commands/executetrade/` は管理ユーザ (staff) しか呼べません。 `schedule.yml` は Basic 認証 (`APP_SERVICE_COMMAND_USER` secret に `user:password`) で呼びます。
    - リンクを開いただけで動かないよう、 POST でしか動きません。
