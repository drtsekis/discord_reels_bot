import discord
import os
import aiosqlite
import asyncio
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from typing import Optional
import time
import random

DATABASE_FOLDER = 'data'
DATABASE_FILENAME = 'database.db'
DATABASE_PATH = os.path.join(DATABASE_FOLDER, DATABASE_FILENAME)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

EMBED_COLORS = [
    discord.Color.blue(),
    discord.Color.green(),
    discord.Color.purple(),
    discord.Color.gold(),
    discord.Color.magenta(),
    discord.Color.orange(),
]


class ReelsView(discord.ui.View):
    def __init__(self, reels, client: discord.Client, current_index=0):
        super().__init__(timeout=None)
        self.reels = reels
        self.client = client
        self.current_index = current_index
        self.message: Optional[discord.WebhookMessage] = None
        self.idle_task: Optional[asyncio.Task] = None

        self.update_buttons()

    def update_buttons(self):
        """Enable/disable Previous/Next buttons depending on the current index."""
        self.previous_button.disabled = (self.current_index == 0)
        self.next_button.disabled = (self.current_index == len(self.reels) - 1)

    async def build_embed(self, forced_likes: Optional[int] = None) -> discord.Embed:
        """
        Creates the embed for the current reel (self.current_index).
        forced_likes can override the DB-based like count if we already know the new total.
        """
        user_id, image_url, timestamp, _ = self.reels[self.current_index]
        user = await self.client.fetch_user(user_id)
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        # If we don't have a forced like count, fetch it from the DB
        if forced_likes is None:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(
                    "SELECT likes FROM reels WHERE user_id = ? AND image_url = ?",
                    (user_id, image_url)
                )
                row = await cursor.fetchone()
                forced_likes = row[0] if row else 0

        # Some basic info
        reel_num = self.current_index + 1
        total_reels = len(self.reels)

        embed_color = random.choice(EMBED_COLORS)
        future_timestamp = int(time.time() + 15)

        # A small note for auto-transition (15s)
        auto_transition_text = f"⏱ Auto-switch to the next reel in <t:{future_timestamp}:R>"

        embed = discord.Embed(
            description=f"**{auto_transition_text}**\n",
            color=embed_color
        )
        embed.set_author(name=f"By: {user.name}", icon_url=avatar_url)
        embed.add_field(
            name="👤 Posted by:",
            value=user.mention,
            inline=True
        )
        embed.add_field(
            name=":date: Posted:",
            value=f"<t:{timestamp}:R>",
            inline=True
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=f"Reel {reel_num} / {total_reels}")

        # Update the like button label to show like count
        self.like_button.label = f"{forced_likes} ❤️"
        return embed

    async def update_embed(self, interaction: discord.Interaction, forced_likes: Optional[int] = None):
        """Refreshes the embed and updates the message."""
        embed = await self.build_embed(forced_likes=forced_likes)

        if interaction.response.is_done():
            await interaction.followup.edit_message(self.message.id, embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

        await self.start_idle_timer()

    async def start_idle_timer(self):
        """Cancels old timer, starts a new 15s timer, then auto-goes Next if time runs out."""
        if self.idle_task:
            self.idle_task.cancel()

        self.idle_task = asyncio.create_task(self.idle_logic())

    async def idle_logic(self):
        """The logic for waiting 15s with no button presses, then going to Next or ending."""
        try:
            await asyncio.sleep(15)
        except asyncio.CancelledError:
            return

        if not self.message:
            return

        # Auto next if we haven't reached the end
        if self.current_index < len(self.reels) - 1:
            self.current_index += 1
            self.update_buttons()

            new_embed = await self.build_embed()
            await self.message.edit(embed=new_embed, view=self)
            await self.start_idle_timer()
        else:
            # We are at the last reel; show an ending message
            end_embed = discord.Embed(
                title="**End of Reels**",
                description=(
                    "You have reached the end of the reel list!\n\n"
                    "There are no more Reels to display.\n"
                    "You can upload a new Reel with the command </reels create>."
                ),
                color=discord.Color.orange()
            )
            end_embed.set_author(name="🎉 Congratulations!")
            end_embed.add_field(
                name="🎬 You've seen all the Reels",
                value=(
                    "Enjoyed each moment shared by the users!\n\n"
                    "Check back later for new posts."
                ),
                inline=False
            )
            end_embed.set_footer(text="Thank you for using the Reels Feature! ✨")

            await self.message.edit(embed=end_embed, view=None)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index -= 1
        self.update_buttons()
        await self.update_embed(interaction)

    @discord.ui.button(label="0 ❤️", style=discord.ButtonStyle.success)
    async def like_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        reel = self.reels[self.current_index]
        user_id, image_url, _, _ = reel
        liker_id = interaction.user.id

        async with aiosqlite.connect(DATABASE_PATH) as db:
            # Check if there's already a like from this user
            cursor = await db.execute("""
                SELECT 1 FROM reel_likes
                WHERE user_id = ? AND image_url = ?
            """, (liker_id, image_url))
            existing_like = await cursor.fetchone()

            if not existing_like:
                # Insert a new like record
                await db.execute("""
                    INSERT INTO reel_likes (user_id, image_url)
                    VALUES (?, ?)
                """, (liker_id, image_url))

                # Increase the like count
                await db.execute("""
                    UPDATE reels
                    SET likes = likes + 1
                    WHERE user_id = ? AND image_url = ?
                """, (user_id, image_url))

                # Fetch the new likes value
                cursor = await db.execute("""
                    SELECT likes
                    FROM reels
                    WHERE user_id = ? AND image_url = ?
                """, (user_id, image_url))
                row = await cursor.fetchone()
                new_likes = row[0] if row else 0
                await db.commit()
            else:
                # Already liked; read the current value
                cursor = await db.execute("""
                    SELECT likes
                    FROM reels
                    WHERE user_id = ? AND image_url = ?
                """, (user_id, image_url))
                row = await cursor.fetchone()
                new_likes = row[0] if row else 0

        await self.update_embed(interaction, forced_likes=new_likes)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index += 1
        self.update_buttons()
        await self.update_embed(interaction)


class ReelsCog(commands.GroupCog, name="reels"):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.clean_up_old_reels.start()

    @tasks.loop(minutes=10)
    async def clean_up_old_reels(self):
        # Remove reels older than 24h
        now_ts = int(datetime.now().timestamp())
        cutoff = now_ts - 86400

        async with aiosqlite.connect(DATABASE_PATH) as db:
            # Delete liked reels that are older
            await db.execute("""
                DELETE FROM reel_likes
                WHERE image_url IN (
                    SELECT image_url FROM reels
                    WHERE datetime < ?
                )
            """, (cutoff,))
            # Delete reels older than 24h
            await db.execute("""
                DELETE FROM reels
                WHERE datetime < ?
            """, (cutoff,))
            await db.commit()

    @clean_up_old_reels.error
    async def clean_up_old_reels_error(self, error):
        print(f"clean_up_old_reels task error: {error}")

    @app_commands.command(name="create", description="Create a new Reel with a photo")
    @app_commands.checks.bot_has_permissions(administrator=True, attach_files=True)
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.describe(photo="Upload a photo for the Reel")
    async def create_reel(self, interaction: discord.Interaction, photo: discord.Attachment):
        ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg"]

        if not photo.content_type:
            return await interaction.response.send_message(
                "Please upload only static images (PNG/JPG).",
                ephemeral=True
            )

        if photo.content_type.lower() not in ALLOWED_IMAGE_TYPES:
            return await interaction.response.send_message(
                "Please upload only static images (PNG/JPG). GIFs are not allowed.",
                ephemeral=True
            )

        image_url = photo.url
        user_id = interaction.user.id
        current_timestamp = int(datetime.now().timestamp())

        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute("SELECT * FROM reels WHERE user_id = ?", (user_id,))
            existing_entry = await cursor.fetchone()
            if existing_entry:
                return await interaction.response.send_message(
                    "You have already uploaded a photo. Multiple uploads are not allowed.",
                    ephemeral=True
                )

            await db.execute("""
                INSERT INTO reels (user_id, image_url, datetime, likes)
                VALUES (?, ?, ?, 0)
            """, (user_id, image_url, current_timestamp))
            await db.commit()

        embed_color = random.choice(EMBED_COLORS)
        embed = discord.Embed(
            title="**New Reel Published!**",
            description=(
                "Congratulations! Your new Reel has been uploaded successfully.\n\n"
                "You can view all available Reels by clicking here: </reels view>."
            ),
            color=embed_color
        )
        embed.set_author(
            name=f"Uploaded by: {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.add_field(
            name="Information:",
            value=(
                "• Your Reel will remain **active** for 24 hours.\n"
                "• Other users can **Like** it only once.\n"
                "• You cannot modify your Reel once uploaded."
            ),
            inline=False
        )
        embed.set_image(url=image_url)
        if interaction.guild and interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_footer(text="Thank you for sharing your moment! ✨")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="view", description="View server Reels")
    @app_commands.checks.bot_has_permissions(administrator=True)
    async def view_reel(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute("""
                SELECT user_id, image_url, datetime, likes
                FROM reels
                ORDER BY datetime DESC
            """)
            reels = await cursor.fetchall()

        if not reels:
            return await interaction.followup.send("No available photos at the moment.", ephemeral=True)

        view = ReelsView(reels, client=interaction.client)
        first_embed = await view.build_embed()
        sent_message = await interaction.followup.send(embed=first_embed, view=view, ephemeral=True)
        view.message = sent_message
        await view.start_idle_timer()

    @app_commands.command(name="terms", description="View server Reels terms")
    @app_commands.checks.bot_has_permissions(administrator=True)
    async def reel_terms(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Reels Usage Terms",
            description="Please read the usage terms carefully before uploading a Reel.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="General Terms",
            value=(
                "• Reels must not contain racist, sexist, or hateful content.\n"
                "• Illegal content or content violating personal privacy is not allowed.\n"
                "• Advertising or promotion of products/services is not allowed without permission."
            ),
            inline=False
        )
        embed.add_field(
            name="Rights and Safety",
            value=(
                "We reserve the right to remove any Reel that violates these terms without notice.\n"
                "All Reels must respect copyright laws."
            ),
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReelsCog(bot))
