from typing import Callable, Dict, Any, Awaitable
import asyncio

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage
    
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user.id
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode())  == 1:
                await self.storage.redis.set(name=user, value=0, ex=2)
                return await event.answer("Не спамь!")
            return
        result = await handler(event, data)
        await self.storage.redis.set(name=user, value=1, ex=3)
        return result