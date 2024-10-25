from django.db import models


class TradingStrategy(models.Model):
    STRATEGY_TYPES = [
        ('GRID', 'Grid Trading'),
        # Добавьте другие типы стратегий при необходимости
    ]

    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('STOPPED', 'Stopped'),
        ('ERROR', 'Error'),
    ]

    name = models.CharField(max_length=100)
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_TYPES)
    symbol = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='STOPPED')
    asset_a_funds = models.DecimalField(max_digits=20, decimal_places=8)
    asset_b_funds = models.DecimalField(max_digits=20, decimal_places=8)
    grids = models.IntegerField()
    deviation_threshold = models.DecimalField(max_digits=5, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    def start(self):
        """Запуск стратегии"""
        if self.status != 'RUNNING':
            self.status = 'RUNNING'
            self.save()
            return True
        return False

    def stop(self):
        """Остановка стратегии"""
        if self.status == 'RUNNING':
            self.status = 'STOPPED'
            self.save()
            return True
        return False

    def get_parameters(self):
        """Получение параметров стратегии"""
        return {
            'symbol': self.symbol,
            'asset_a_funds': float(self.asset_a_funds),
            'asset_b_funds': float(self.asset_b_funds),
            'grids': self.grids,
            'deviation_threshold': float(self.deviation_threshold),
        }

class TradeLog(models.Model):
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)  # buy/sell
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.strategy.symbol} - {self.action} at {self.price}"
