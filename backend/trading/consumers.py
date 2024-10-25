from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import time

class TradingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.strategy_id = self.scope['url_route']['kwargs']['strategy_id']
        self.group_name = f"strategy_{self.strategy_id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        # Обработка входящих сообщений (если необходимо)
        pass

    async def strategy_update(self, event):
        data = event.get('data', {})
        message_type = data.get('type', None)
        
        message_handlers = {
            'status': self.handle_status,
            'initialization': self.handle_initialization,
            'grid_levels': self.handle_grid_levels,
            'order_sizes': self.handle_order_sizes,
            'price_update': self.handle_price_update,
            'active_orders': self.handle_active_orders,
            'trade': self.handle_trade,
            'order_placed': self.handle_order_placed,  # Новый обработчик
            'error': self.handle_error
        }
        
        handler = message_handlers.get(message_type)
        if handler:
            await handler(data.get('data', {}))
        else:
            await self.send_json({
                'type': 'error',
                'data': {'message': f"Неизвестный тип сообщения: {message_type}"}
            })

    async def handle_status(self, data):
        await self.send_json({
            'type': 'status',
            'data': data
        })

    async def handle_initialization(self, data):
        await self.send_json({
            'type': 'initialization',
            'data': {
                'message': data.get('message'),
                'initial_price': data.get('initial_price')
            }
        })

    async def handle_grid_levels(self, data):
        await self.send_json({
            'type': 'grid_levels',
            'data': {
                'message': data.get('message'),
                'buy_levels': data.get('buy_levels'),
                'sell_levels': data.get('sell_levels')
            }
        })

    async def handle_order_sizes(self, data):
        await self.send_json({
            'type': 'order_sizes',
            'data': {
                'message': data.get('message'),
                'buy_sizes': data.get('buy_sizes'),
                'sell_sizes': data.get('sell_sizes')
            }
        })

    async def handle_price_update(self, data):
        await self.send_json({
            'type': 'price_update',
            'data': {
                'current_price': data.get('current_price'),
                'deviation': data.get('deviation'),
                'initial_price': data.get('initial_price')
            }
        })

    async def handle_active_orders(self, data):
        await self.send_json({
            'type': 'active_orders',
            'data': {
                'buy_positions': data.get('buy_positions', []),
                'sell_positions': data.get('sell_positions', [])
            }
        })

    async def handle_trade(self, data):
        await self.send_json({
            'type': 'trade',
            'data': {
                'type': data.get('type'),
                'price': data.get('price'),
                'quantity': data.get('quantity')
            }
        })

    async def handle_order_placed(self, data):
        await self.send_json({
            'type': 'order_placed',
            'data': {
                'order_type': data.get('order_type'),
                'price': data.get('price'),
                'quantity': data.get('order_size')
            }
        })

    async def handle_error(self, data):
        await self.send_json({
            'type': 'error',
            'data': {'message': data.get('error', 'Неизвестная ошибка')}
        })
