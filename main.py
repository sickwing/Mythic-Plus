import discord
from discord.ext import commands
import os

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = int(os.getenv("ROLE_ID", "0"))

class KeyModal(discord.ui.Modal, title="Создать Mythic+ ключ"):
    dungeon = discord.ui.TextInput(
        label="Название данжа",
        placeholder="Например: Ruby Life Pools"
    )

    level = discord.ui.TextInput(
        label="Уровень ключа",
        placeholder="Например: 15"
    )

    async def on_submit(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(ROLE_ID)

        embed = discord.Embed(
            title="🔥 Mythic+ Run",
            color=discord.Color.purple()
        )
        embed.add_field(name="🗺 Dungeon", value=self.dungeon.value, inline=False)
        embed.add_field(name="🔑 Key Level", value=f"+{self.level.value}", inline=False)
        embed.add_field(name="👥 Статус", value="Ищем группу!", inline=False)

        content = role.mention if role else ""

        await interaction.response.send_message(
            content=content,
            embed=embed
        )

@bot.tree.command(name="key", description="Создать анонс Mythic+")
async def key(interaction: discord.Interaction):
    await interaction.response.send_modal(KeyModal())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Бот запущен как {bot.user}")

bot.run(os.getenv("TOKEN"))