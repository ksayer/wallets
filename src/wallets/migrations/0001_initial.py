# Generated by Django 5.1.7 on 2025-03-25 18:07

from decimal import Decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=64)),
            ],
            options={
                'ordering': ['-id'],
                'constraints': [models.CheckConstraint(condition=models.Q(('balance__gte', 0)),
                                                       name='balance_gte_zero')],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txid', models.CharField(max_length=66, unique=True)),
                ('amount', models.DecimalField(decimal_places=18, max_digits=64)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallets.wallet')),
            ],
            options={
                'ordering': ['-id'],
                'constraints': [models.CheckConstraint(condition=models.Q(('amount', 0), _negated=True),
                                                       name='amount_non_zero')],
            },
        ),
    ]
