from django.db import transaction
from django.db.models import F
from rest_framework_json_api import serializers

from wallets.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        wallet_id = validated_data['wallet'].id
        amount = validated_data['amount']

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet_id)
            if wallet.balance + amount < 0:
                raise serializers.ValidationError("Insufficient balance for this transaction")

            Wallet.objects.filter(id=wallet_id).update(
                balance=F("balance") + amount
            )

        return super().create(validated_data)
