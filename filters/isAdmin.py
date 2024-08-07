from aiogram.types import Message
from aiogram.filters import BaseFilter

from main.config import ADMIN1, ADMIN2, ADMIN3


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admins_list = [ADMIN1, ADMIN2, ADMIN3]

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins_list
