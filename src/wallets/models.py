from decimal import Decimal

from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(
        max_digits=64,
        decimal_places=18,
        default=Decimal('0'),
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(condition=models.Q(balance__gte=0), name='balance_gte_zero'),
        ]

    def __str__(self):
        return f"Wallet: {self.label}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    txid = models.CharField(max_length=66, unique=True)
    amount = models.DecimalField(
        max_digits=64,
        decimal_places=18,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(condition=~models.Q(amount=0), name='amount_non_zero'),
        ]

    def __str__(self):
        return f"Transaction: {self.txid}"
