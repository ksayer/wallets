import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.wallets.factories import TransactionFactory, WalletFactory

register(WalletFactory)
register(TransactionFactory)


@pytest.fixture
def api_client():
    return APIClient()

