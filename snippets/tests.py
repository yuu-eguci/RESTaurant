from unittest import mock

import pytest
from django.core.management import call_command
from django.test import Client

URL = "/commands/samplecommand/"


def test_samplecommand_writes_current_time(capsys):
    call_command("samplecommand")

    assert "timezone.now(): " in capsys.readouterr().out


@pytest.mark.django_db
def test_samplecommand_endpoint_does_not_run_on_get(admin_client):
    with mock.patch("snippets.management.commands.samplecommand.Command.handle") as handle:
        response = admin_client.get(URL)

    assert response.status_code == 405
    handle.assert_not_called()


@pytest.mark.django_db
def test_samplecommand_endpoint_rejects_anonymous_user(client):
    response = client.post(URL)

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_samplecommand_endpoint_rejects_non_staff_user(client, django_user_model):
    client.force_login(django_user_model.objects.create_user("user", password="pw"))

    response = client.post(URL)

    assert response.status_code == 403


@pytest.mark.django_db
def test_samplecommand_endpoint_runs_command_for_staff_user(admin_client):
    response = admin_client.post(URL)

    assert response.status_code == 200
    assert response.json() == {"result": None}


@pytest.mark.django_db
def test_server_error_does_not_leak_details(admin_user):
    client = Client(raise_request_exception=False)
    client.force_login(admin_user)

    with mock.patch(
        "snippets.management.commands.samplecommand.Command.handle",
        side_effect=RuntimeError("very-internal-detail"),
    ):
        response = client.post(URL)

    assert response.status_code == 500
    body = response.content.decode()
    assert "very-internal-detail" not in body
    assert "Traceback" not in body
    assert "SECRET_KEY" not in body
