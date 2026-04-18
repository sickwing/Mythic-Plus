import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = int(os.getenv("ROLE_ID", "0"))

#this season dungs
DUNGEONS = [
    "Algeth'ar Academy",
    "Magister's Terrace",
    "Maisara Caverns",
    "Nexus-Point Xenas",
    "Windrunner Spire",
    "Pit of Saron",
    "Seat of the Triumvirate",
    "Skyreach"
]

# modal for key level
class KeyModal(discord.ui.Modal):
    def __init__(self, dungeon_name):
        super().__init__(title="Enter Key Level")
        self.dungeon_name = dungeon_name

        self.level = discord.ui.TextInput(
            label="Key Level",
            placeholder="e.g. 15"
        )
        self.add_item(self.level)

    async def on_submit(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(ROLE_ID)

        embed = discord.Embed(
            title="🔥 Mythic+ Run",
            color=discord.Color.purple()
        )
        embed.add_field(name="🗺 Dungeon", value=self.dungeon_name, inline=False)
        embed.add_field(name="🔑 Key Level", value=f"+{self.level.value}", inline=False)

        content = role.mention if role else ""

        await interaction.response.send_message(content=content, embed=embed)


# 🔹 Dropdown for choosing dung
class DungeonSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=dungeon)
            for dungeon in DUNGEONS
        ]

        super().__init__(
            placeholder="Select a dungeon",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            KeyModal(self.values[0])
        )


# container fro dropdown
class DungeonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DungeonSelect())

@bot.tree.command(name="key", description="Create a Mythic+ announcement")
async def key(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Select a dungeon:",
        view=DungeonView(),
        ephemeral=True  # 
    )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")


bot.run(os.getenv("TOKEN"))
