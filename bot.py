"""Railway上で動かすDiscord BOTの基盤コード。"""
import logging
import os
import sys

import discord
from discord import app_commands
from discord.ext import commands

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,  # Railwayのログに表示されるよう標準出力へ
)
log = logging.getLogger("bot")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    log.error("環境変数 DISCORD_TOKEN が設定されていません")
    sys.exit(1)

# 開発中はギルドIDを指定するとスラッシュコマンドが即時反映される(任意)
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
# メッセージ内容を読む場合のみ有効化(Developer Portalでの設定も必要)
# intents.message_content = True


class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        # Cogを増やす場合はここで load_extension する
        # await self.load_extension("cogs.example")
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
        log.info("スラッシュコマンドを同期しました")

    async def on_ready(self) -> None:
        log.info("ログインしました: %s (ID: %s)", self.user, self.user.id)


bot = MyBot()


@bot.tree.command(name="ping", description="BOTの応答速度を確認します")
async def ping(interaction: discord.Interaction) -> None:
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! {latency_ms}ms")


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    log.exception("コマンドエラー", exc_info=error)
    msg = "エラーが発生しました。"
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
