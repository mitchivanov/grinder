# Generated by Django 5.1.2 on 2024-10-24 03:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradingStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('strategy_type', models.CharField(choices=[('GRID', 'Grid Trading')], max_length=20)),
                ('symbol', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('RUNNING', 'Running'), ('STOPPED', 'Stopped'), ('ERROR', 'Error')], default='STOPPED', max_length=20)),
                ('asset_a_funds', models.DecimalField(decimal_places=8, max_digits=20)),
                ('asset_b_funds', models.DecimalField(decimal_places=8, max_digits=20)),
                ('grids', models.IntegerField()),
                ('deviation_threshold', models.DecimalField(decimal_places=4, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=8, max_digits=20)),
                ('quantity', models.DecimalField(decimal_places=8, max_digits=20)),
                ('status', models.CharField(max_length=50)),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.tradingstrategy')),
            ],
        ),
    ]