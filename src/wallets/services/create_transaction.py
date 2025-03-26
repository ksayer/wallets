from decimal import Decimal

from django.db import transaction
from django.db.models import F
from wallets.models import Transaction, Wallet
from rest_framework_json_api import serializers



def create_transaction(amount: Decimal, wallet_id: int, txid: int):
    """Use select for update to avoid parallel update of wallet balance"""
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(id=wallet_id)
        if wallet.balance + amount < 0:
            raise serializers.ValidationError("Insufficient balance for this transaction")

        Wallet.objects.filter(id=wallet_id).update(
            balance=F("balance") + amount
        )
        Transaction.objects.create(wallet_id=wallet.id, amount=amount, txid=txid)
