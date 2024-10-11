from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import API_HASH, API_ID, LOGGER, BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot Can't Export Invite Link From Force Sub Channel!")
                self.LOGGER.warning(f"Please Double Check The FORCE_SUB_CHANNEL Value And Make Sure Bot Is Admin In Channel With Invite Users Via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER.info("\nBot Stopped. https://t.me/MadflixBots_Support For Support")
                sys.exit()

        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER.warning(a)
                self.LOGGER.warning("Bot Can't Export Invite Link From Force Sub Channel2!")
                self.LOGGER.warning(f"Please Double Check The FORCE_SUB_CHANNEL2 Value And Make Sure Bot Is Admin In Channel With Invite Users Via Link Permission, Current Force Sub Channel2 Value: {FORCE_SUB_CHANNEL2}")
                self.LOGGER.info("\nBot Stopped. https://t.me/MadflixBots_Support For Support")
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Hey 🖐")
            await test.delete()
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning(f"Make Sure Bot Is Admin In DB Channel, And Double Check The CHANNEL_ID Value, Current Value: {CHANNEL_ID}")
            self.LOGGER.info("\nBot Stopped. Join https://t.me/MadflixBots_Support For Support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(f"Bot Running..!\n\nCreated By \nhttps://t.me/Madflix_Bots")
        self.LOGGER.info(f"""ミ💖 MADFLIX BOTZ 💖彡""")
        self.username = usr_bot_me.username

        # Web server initialization
        runner = web.AppRunner(await web_server())
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()

    async def stop(self, *args):
        await super().stop()
        # Clean up the web server
        await self.app.cleanup()
        self.LOGGER.info("Bot Stopped...")

# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
