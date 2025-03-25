from rest_framework import viewsets, mixins

from wallets.models import Wallet, Transaction
from wallets.api.v1.serializers import WalletSerializer, TransactionSerializer


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
