import discord

class TuxEmbeds:
    def set_default_footer(
        self, 
        original_embed: discord.Embed, 
        user: discord.User
    ) -> discord.Embed:
        """
        Sets the footer to an embed.
        
        Parameters:
            original_embed (discord.Embed): The original embed.
            user (discord.User): The user that executed the command.

        Example Usage:
            embed = discord.Embed(...)
            set_default_footer(embed, ctx.user)
        """
        original_embed.set_footer(
            text=f"Requested by {user.display_name}",
            icon_url=user.display_avatar
        )

        return original_embed
