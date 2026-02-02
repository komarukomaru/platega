import asyncio
from typing import Callable, Dict, Any, Union, Awaitable
from .models import CallbackPayload, PaymentStatus

class PlategaWebhookHandler:
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._any_handler: Union[Callable, None] = None

    def on(self, status: PaymentStatus):
        def decorator(func: Callable[[CallbackPayload], Any]):
            self._handlers[status.value] = func
            return func
        return decorator

    def handle_all(self):
        def decorator(func: Callable[[CallbackPayload], Any]):
            self._any_handler = func
            return func
        return decorator

    async def process_webhook(self, payload: Union[Dict[str, Any], CallbackPayload]):
        if isinstance(payload, dict):
            payload = CallbackPayload(**payload)
        
        status = payload.status
        handler = self._handlers.get(status.value)

        if handler:
            if asyncio.iscoroutinefunction(handler):
                await handler(payload)
            else:
                handler(payload)
        
        if self._any_handler:
            if asyncio.iscoroutinefunction(self._any_handler):
                await self._any_handler(payload)
            else:
                self._any_handler(payload)
