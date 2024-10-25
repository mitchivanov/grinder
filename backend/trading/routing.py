from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/trading/strategy_(?P<strategy_id>\d+)/$', consumers.TradingConsumer.as_asgi()),
]

