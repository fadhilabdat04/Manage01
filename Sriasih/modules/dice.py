from pyrogram import filters
from pyrogram.types import Message

from Sriasih import SUDOERS, app

__MODULE__ = "Dice"
__HELP__ = """
/dice
    Roll a dice.
    ᴧꝛᴧʙ ꝛᴏʙᴏᴛ | @SiArab_Store ™
"""


@app.on_message(filters.command("dice"))
async def throw_dice(client, message: Message):
    six = (message.from_user.id in SUDOERS) if message.from_user else False

    c = message.chat.id
    if not six:
        return await client.send_dice(c, "🎲")

    m = await client.send_dice(c, "🎲")

    while m.dice.value != 6:
        await m.delete()
        m = await client.send_dice(c, "🎲")
