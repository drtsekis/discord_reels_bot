import discord,os
import platform,aiosqlite
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
tsekis = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

@tsekis.event
async def on_ready():
    print(f'Logged in as {tsekis.user}!')


@tsekis.event
async def setup_hook():
    print(f"\033[0m======================")
    for extension in os.listdir(f"cogs"):
        if extension.endswith(".py"):
            await tsekis.load_extension(f"cogs.{extension[:-3]}")
            print(f"\033[92m cogs.{extension[:-3]} Loaded")
    print(f"\033[0m======================")
    # await tsekis.tree.sync()

    database_folder = 'data'
    database_filename = 'database.db'
    database_path = os.path.join(database_folder, database_filename)

    # General Database#
    async with aiosqlite.connect(database_path) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS duty(
            staff_name TEXT,
            staff_id INT,
            start_time TEXT,
            duty_status TEXT,
            total_time TEXT
            )
            """)
        await db.commit()
        await db.execute("""
        CREATE TABLE IF NOT EXISTS reels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            image_url TEXT,
            datetime INTEGER,
            likes INT DEFAULT 0
            )
            """)
        await db.commit()
        await db.execute("""
        CREATE TABLE IF NOT EXISTS reel_likes (
            user_id  INTEGER,
            image_url  TEXT,
            UNIQUE(user_id, image_url)
            )
            """)
        await db.commit()


tsekis.run("TOKEN", reconnect=True)
