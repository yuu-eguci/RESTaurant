import importlib
import os
from unittest import mock

import pytest
from django.core.management import call_command

PRODUCTION_ENV = {
    "WEBSITE_HOSTNAME": "restaurant.example.com",
    "DJANGO_DATABASE_NAME": "restaurant",
    "DJANGO_DATABASE_USER": "restaurant",
    "DJANGO_DATABASE_PASSWORD": "dummy-password",
    "DJANGO_DATABASE_SERVER": "db.example.com",
}


def load_settings(module_name, env):
    with mock.patch.dict(os.environ, env, clear=True):
        return importlib.reload(importlib.import_module(module_name))


def test_settings_reads_secret_key_from_environment():
    settings = load_settings("RESTaurant.settings", {"DJANGO_SECRET_KEY": "from-env"})

    assert settings.SECRET_KEY == "from-env"


def test_settings_generates_random_secret_key_without_environment():
    first = load_settings("RESTaurant.settings", {}).SECRET_KEY
    second = load_settings("RESTaurant.settings", {}).SECRET_KEY

    assert len(first) >= 50
    assert first != second


def test_settings_keeps_generated_secret_key_in_environment_for_autoreload():
    with mock.patch.dict(os.environ, {}, clear=True):
        settings = importlib.reload(importlib.import_module("RESTaurant.settings"))

        # NOTE: runserver の autoreload で起動する子プロセスは環境変数を引き継ぎます。
        assert os.environ["DJANGO_SECRET_KEY"] == settings.SECRET_KEY


def test_production_requires_secret_key():
    with pytest.raises(KeyError, match="DJANGO_SECRET_KEY"):
        load_settings("RESTaurant.production", PRODUCTION_ENV)


def test_production_uses_secret_key_from_environment_and_disables_debug():
    production = load_settings(
        "RESTaurant.production",
        {**PRODUCTION_ENV, "DJANGO_SECRET_KEY": "production-secret"},
    )

    assert production.SECRET_KEY == "production-secret"
    assert production.DEBUG is False
    assert production.ALLOWED_HOSTS == ["restaurant.example.com"]
    assert production.SESSION_COOKIE_SECURE is True
    assert production.CSRF_COOKIE_SECURE is True
    assert production.CSRF_TRUSTED_ORIGINS == ["https://restaurant.example.com"]


@pytest.mark.django_db
def test_migrations_are_in_sync_with_models():
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)
