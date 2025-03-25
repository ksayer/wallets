import factory

from wallets import models


class WalletFactory(factory.django.DjangoModelFactory):
    label = factory.Faker("name")
    balance = factory.Faker("pydecimal", positive=True, left_digits=10, right_digits=18)

    class Meta:
        model = models.Wallet


class TransactionFactory(factory.django.DjangoModelFactory):
    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Faker("name")
    amount = factory.Faker("pydecimal", positive=True, left_digits=10, right_digits=18)

    class Meta:
        model = models.Transaction
