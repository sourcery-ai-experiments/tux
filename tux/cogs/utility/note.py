import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger
import json
import pathlib as path
from tux.utils.constants import Constants as CONST
Path = path.Path
storage_file = Path("config/settings.json")
storage = json.loads(storage_file.read_text())


class Note(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    group = app_commands.Group(name="note", description="Note Commands")
    @staticmethod
    def create_embed(
        title: str = "", description: str = "", color: int = CONST.COLORS["SUCCESS"]
    ) -> discord.Embed:
        """Utility method for creating a basic embed structure."""
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_author(name="Info", icon_url="https://cdn3.emoji.gg/emojis/3228-info.png")
        return embed
    
    @group.command(name="write", description="")
    
    async def write(self, interaction: discord.Interaction, user: discord.Member, note: str):
      user_id = user.id
      data = {
        "user": user_id,
        "note": note

       
      }
      
      embed = self.create_embed("Note Added", f"Note added for {user.display_name}")
      
      
      with Path.open(storage_file, "w") as file:
        json.dump(data,file, indent=4)
      logger.info("Note added")
      await interaction.response.send_message(embed=embed)
      
    @group.command(name="read", description="")
    async def read(self, interaction: discord.Interaction, user: discord.Member):
      user_id = user.id
      with Path.open(storage_file, "r") as file:
        data = json.load(file)
        user_note = next((entry["note"] for entry in data if entry["user"] == user_id), None)

        if user_note:
            embed = self.create_embed(
                title="Note Found",
                description=f"Note for {user.display_name}: {user_note}",
                color=CONST.COLORS["INFO"]
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(
                title="Note Not Found",
                description=f"No note found for {user.display_name}",
                color=CONST.COLORS["ERROR"],
                
            )
            await interaction.response.send_message(embed=embed)
    @group.command(name="delete", description="Delete a note.")
    async def delete(self, interaction: discord.Interaction, user: discord.Member):
      user_id = user.id
      with Path.open(storage_file, "r") as file:
        data = json.load(file)
      updated_data = [entry for entry in data if entry["user"] != user_id]
      if len(data) == len(updated_data):
        embed = self.create_embed(
            title="Note Delete Error",
            description=f"No note found for {user.display_name}!",
            color=CONST.COLORS["ERROR"]
        )
        logger.error("Note delete error - Note not found")
        await interaction.response.send_message(embed=embed)
      else:
        with Path.open(storage_file, "w") as file:
            json.dump(updated_data, file, indent=4)

        embed = self.create_embed(
            title="Note Deleted",
            description=f"Note deleted for {user.display_name}.",
            color=CONST.COLORS["SUCCESS"]
        )
        logger.info("Note deleted")
        await interaction.response.send_message(embed=embed)
        
      
  
    
    
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Note(bot))