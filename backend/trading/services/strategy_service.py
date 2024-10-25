from typing import Dict
import asyncio
from .grid_strategy import GridStrategy
from ..models import TradingStrategy

class StrategyService:
    _running_strategies: Dict[int, GridStrategy] = {}

    @classmethod
    async def start_strategy(cls, strategy_id: int):
        strategy = TradingStrategy.objects.get(id=strategy_id)
        if strategy_id in cls._running_strategies:
            raise ValueError("Strategy is already running")

        grid_strategy = GridStrategy(strategy)
        cls._running_strategies[strategy_id] = grid_strategy
        
        # Запускаем стратегию в отдельной корутине
        asyncio.create_task(grid_strategy.execute_strategy())
        
        return grid_strategy

    @classmethod
    async def stop_strategy(cls, strategy_id: int):
        if strategy_id not in cls._running_strategies:
            raise ValueError("Strategy is not running")

        strategy = cls._running_strategies[strategy_id]
        strategy.stop()
        del cls._running_strategies[strategy_id]

