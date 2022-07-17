import pytest
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.conversation import Conversation

from config import config


load_dotenv()

api_id = int(os.getenv("TELEGRAM_APP_ID"))
api_hash = os.getenv("TELEGRAM_APP_HASH")
session_str = os.getenv("TELETHON_SESSION")

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def client() -> TelegramClient:
    client = TelegramClient(
        StringSession(session_str),
        api_id,
        api_hash,
        sequential_updates=True
    )
    await client.connect()

    yield client

    await client.disconnect()
    await client.disconnected

@pytest.fixture(scope="session")
async def conv(client: TelegramClient) -> Conversation:
    async with client.conversation(config['BOT_NAME'], timeout=10) as conv:

        yield conv

        conv.cancel()