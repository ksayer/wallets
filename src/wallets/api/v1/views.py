from rest_framework import mixins, viewsets

from wallets.api.v1.serializers import TransactionSerializer, WalletSerializer
from wallets.models import Transaction, Wallet
from wallets.services.create_transaction import create_transaction


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    ordering_fields = ["label", "balance"]
    filterset_fields = {
        "balance": ("exact", "lt", "gt", "gte", "lte"),
        "label": ("exact", "iexact", "contains", "icontains"),
    }


class TransactionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = ["txid", "amount"]
    filterset_fields = {
        "amount": ("exact", "lt", "gt", "gte", "lte"),
        "txid": ("exact",),
        "wallet__id": ("exact",),
    }

    def perform_create(self, serializer):
        return create_transaction(
            wallet_id=serializer.validated_data['wallet'].id,
            amount=serializer.validated_data['amount'],
            txid=serializer.validated_data['txid'],
        )
