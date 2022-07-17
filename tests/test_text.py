from telethon.tl.custom import Conversation, Message

import pytest

@pytest.mark.anyio
async def test_start(conv: Conversation):
    await conv.send_message('/start')
    resp: Message = await conv.get_response()
    assert "Привет!" in resp.raw_text

@pytest.mark.anyio
async def test_any_text(conv: Conversation):
    await conv.send_message('any_text')
    resp: Message = await conv.get_response()
    assert 'пришлите файл' in resp.raw_text