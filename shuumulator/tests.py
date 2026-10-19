import pytest

from shuumulator.models import Stock, Trader, TradingRecord

TRADE = {
    "bought_price": "1000.00",
    "bought_at": "2021-01-11T09:00:00Z",
    "sold_price": "1100.00",
    "sold_at": "2021-01-12T09:00:00Z",
}


@pytest.fixture
def stock(db):
    return Stock.objects.create(code="7203", name="Toyota")


@pytest.fixture
def trader(db):
    return Trader.objects.create(name="shuu")


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/stock/", "/trader/", "/tradingrecord/"])
def test_api_requires_authentication(client, url):
    assert client.get(url).status_code in (401, 403)


def test_tradingrecord_list_returns_related_ids(admin_client, stock, trader):
    TradingRecord.objects.create(stock=stock, trader=trader, **TRADE)

    response = admin_client.get("/tradingrecord/")

    assert response.status_code == 200
    [record] = response.json()["results"]
    assert record["stock"] == stock.id
    assert record["trader"] == trader.id


def test_tradingrecord_can_be_created(admin_client, stock, trader):
    response = admin_client.post(
        "/tradingrecord/",
        {"stock": stock.id, "trader": trader.id, **TRADE},
        content_type="application/json",
    )

    assert response.status_code == 201
    assert TradingRecord.objects.get().stock == stock


@pytest.mark.django_db
def test_executetrade_endpoint_rejects_anonymous_user(client):
    assert client.post("/commands/executetrade/").status_code in (401, 403)


@pytest.mark.django_db
def test_executetrade_endpoint_rejects_non_staff_user(client, django_user_model):
    client.force_login(django_user_model.objects.create_user("user", password="pw"))

    assert client.post("/commands/executetrade/").status_code == 403


@pytest.mark.django_db
def test_executetrade_endpoint_does_not_run_on_get(admin_client):
    assert admin_client.get("/commands/executetrade/").status_code == 405


@pytest.mark.django_db
def test_executetrade_endpoint_runs_command_for_staff_user(admin_client):
    response = admin_client.post("/commands/executetrade/")

    assert response.status_code == 200
    assert response.json() == {"result": None}


def test_tradingrecord_can_be_created_before_selling(admin_client, stock, trader):
    response = admin_client.post(
        "/tradingrecord/",
        {"stock": stock.id, "trader": trader.id, "bought_price": "1000.00", "bought_at": "2021-01-11T09:00:00Z"},
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json()["sold_price"] is None
    assert response.json()["sold_at"] is None
