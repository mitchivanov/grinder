from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TradingStrategySerializer, TradeLogSerializer
from .models import TradingStrategy, TradeLog
from rest_framework import viewsets
from rest_framework.decorators import action
from .services.strategy_service import StrategyService
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
import time

class TradingStrategyViewSet(viewsets.ModelViewSet):
    queryset = TradingStrategy.objects.all()
    serializer_class = TradingStrategySerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        strategy = self.get_object()
        try:
            strategy.status = 'RUNNING'
            strategy.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"strategy_{strategy.id}",
                {
                    "type": "strategy_update",
                    "data": {
                        "type": "status",
                        "data": {"status": "RUNNING"},
                        "message": "Strategy started",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            )
            
            # Добавляем запись в лог
            TradeLog.objects.create(
                strategy=strategy,
                action='START',
                price=0,
                quantity=0,
                status='COMPLETED'
            )
            
            return Response({'status': 'Strategy started'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        strategy = self.get_object()
        try:
            # Синхронно обновляем статус
            strategy.status = 'STOPPED'
            strategy.save()
            
            # Отправляем обновление через WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"strategy_{strategy.id}",
                {
                    "type": "strategy_update",
                    "data": {
                        "type": "status",
                        "data": {"status": "STOPPED"},
                        "message": "Strategy stopped",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            )
            
            return Response({'status': 'Strategy stopped'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class TradeLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TradeLogSerializer

    def get_queryset(self):
        queryset = TradeLog.objects.all()
        strategy_id = self.request.query_params.get('strategy_id', None)
        if strategy_id is not None:
            queryset = queryset.filter(strategy_id=strategy_id)
        return queryset

class StrategyListView(ListView):
    model = TradingStrategy
    template_name = 'strategy_list.html'
    context_object_name = 'strategies'

class StrategyDetailView(DetailView):
    model = TradingStrategy
    template_name = 'strategy_detail.html'
    context_object_name = 'strategy'

class StrategyCreateView(CreateView):
    model = TradingStrategy
    fields = ['name', 'strategy_type', 'symbol', 'asset_a_funds', 'asset_b_funds', 'grids', 'deviation_threshold']
    template_name = 'strategy_create.html'
    success_url = reverse_lazy('strategy_list')

