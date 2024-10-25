from rest_framework import serializers
from .models import TradingStrategy, TradeLog

class TradingParametersSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    asset_a_funds = serializers.FloatField()
    asset_b_funds = serializers.FloatField()
    grids = serializers.IntegerField()
    deviation_threshold = serializers.FloatField()
    trail_price = serializers.BooleanField()
    only_profitable_trades = serializers.BooleanField()

class TradingStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingStrategy
        fields = '__all__'

class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        fields = '__all__'

class StrategyStartSerializer(serializers.Serializer):
    strategy_id = serializers.IntegerField()
