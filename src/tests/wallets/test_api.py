# type: ignore
import uuid
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from typing import Type

import pytest
from rest_framework.test import APIClient

from tests.wallets.factories import TransactionFactory, WalletFactory
from wallets.models import Wallet


def wallet_json(label: str, balance: Decimal | None = None, wallet_id: int | None = None):
    data = {
        "data": {
            "type": "wallets",
            "attributes": {
                "label": label,
            },
        }
    }
    if balance is not None:
        data["data"]["attributes"]["balance"] = balance
    if wallet_id is not None:
        data["data"]["id"] = wallet_id
    return data


def post_transaction_json(txid: str, amount: Decimal, wallet_id: int):
    return {
        "data": {
            "type": "transactions",
            "attributes": {
                "txid": txid,
                "amount": amount,
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": wallet_id}}},
        }
    }


@pytest.mark.django_db
def test__wallets__create(api_client: APIClient):
    resp = api_client.post("/api/v1/wallets/", wallet_json("label", Decimal(777)))

    assert resp.status_code == 201
    assert resp.json()["data"]["attributes"]["label"] == "label"
    assert resp.json()["data"]["attributes"]["balance"] == "0.000000000000000000"


@pytest.mark.django_db
def test__wallets__retrieve(api_client: APIClient, wallet_factory: Type[WalletFactory]):
    wallet = wallet_factory()
    resp = api_client.get(f"/api/v1/wallets/{wallet.id}/")
    assert resp.status_code == 200
    assert resp.json()["data"]["attributes"]["balance"] == str(wallet.balance)


@pytest.mark.django_db
def test__wallets__list(api_client: APIClient, wallet_factory: Type[WalletFactory]):
    wallet_factory()
    resp = api_client.get("/api/v1/wallets/")

    assert resp.status_code == 200
    assert resp.json()["meta"]["pagination"]["count"] == 1


@pytest.mark.django_db
def test__wallets__update(api_client: APIClient, wallet_factory: Type[WalletFactory]):
    wallet = wallet_factory()
    resp = api_client.put(f"/api/v1/wallets/{wallet.id}/", wallet_json("label", Decimal(777), wallet.id))

    assert resp.status_code == 200, resp.data
    assert resp.json()["data"]["attributes"]["label"] == "label"
    assert resp.json()["data"]["attributes"]["balance"] == str(wallet.balance)


@pytest.mark.django_db
def test__transactions__create(api_client: APIClient, wallet_factory: Type[WalletFactory]):
    wallet = wallet_factory(balance=500)
    api_client.post("/api/v1/transactions/", post_transaction_json("tx1", Decimal(500), wallet.id))
    resp = api_client.post("/api/v1/transactions/", post_transaction_json("tx2", Decimal(-1000), wallet.id))

    assert resp.status_code == 201
    wallet = Wallet.objects.get(id=wallet.id)
    assert wallet.balance == 0


@pytest.mark.django_db
def test__transactions__create__balance_error(api_client: APIClient, wallet_factory: Type[WalletFactory]):
    wallet = wallet_factory(balance=500)
    resp = api_client.post("/api/v1/transactions/", post_transaction_json("tx3", Decimal(-1000), wallet.id))

    assert resp.status_code == 400, resp.data
    wallet = Wallet.objects.get(id=wallet.id)
    assert wallet.balance == 500


@pytest.mark.django_db(transaction=True)
def test__transactions__concurrent_withdraws__should_not_go_negative(
    api_client: APIClient,
    wallet_factory: Type[WalletFactory],
):
    wallet = wallet_factory(balance=500)
    threads = 100

    def withdraw():
        return api_client.post(
            "/api/v1/transactions/",
            post_transaction_json(str(uuid.uuid4()), Decimal("-400"), wallet.id)
        )

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(withdraw) for _ in range(threads)]

    responses = [f.result() for f in futures]
    statuses = [resp.status_code for resp in responses]
    client_errors = [400] * (threads - 1)
    assert sorted(statuses) == [201, *client_errors]

    wallet.refresh_from_db()
    assert wallet.balance >= 0


@pytest.mark.django_db
def test__transactions__get(api_client: APIClient, transaction_factory: Type[TransactionFactory]):
    transaction = transaction_factory()
    resp = api_client.get(f"/api/v1/transactions/{transaction.id}/")

    assert resp.status_code == 200
    assert resp.json()["data"]["attributes"]["amount"] == str(transaction.amount)


@pytest.mark.django_db
def test__transactions__list(api_client: APIClient, transaction_factory: Type[TransactionFactory]):
    transaction_factory()
    resp = api_client.get("/api/v1/transactions/")

    assert resp.status_code == 200
    assert resp.json()["meta"]["pagination"]["count"] == 1
