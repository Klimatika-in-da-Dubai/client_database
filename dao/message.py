from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.message import File, Message, MessageFile


class MessageDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Message, session)

    async def attach_file(self, message: Message, file: File):
        await self.add(file)
        message_file = MessageFile(message_id=message.id, file_id=file.id)
        await self.add(message_file)

    async def change_message(self, message_id: str, text: str):
        message: Message = await self.get_by_id(message_id)
        message.text = text
        await self.commit()
