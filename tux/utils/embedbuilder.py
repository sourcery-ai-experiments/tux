import discord
from discord.ext import commands

from tux.utils.constants import Constants as CONST


def base_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    state: str,
) -> discord.Embed:
    embed = discord.Embed()

    embed.color = CONST.EMBED_STATE_COLORS[state]

    embed.set_author(name=state.capitalize(), icon_url=CONST.EMBED_STATE_ICONS[state])

    if ctx and ctx.message:
        embed.timestamp = ctx.message.created_at
    elif interaction:
        embed.timestamp = interaction.created_at
    else:
        embed.timestamp = discord.utils.utcnow()

    if ctx:
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
    elif interaction:
        embed.set_footer(
            text=f"Requested by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url,
        )
    else:
        embed.set_footer(text="", icon_url="")

    return embed


def create_default_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, "DEFAULT")

    embed.title = title
    embed.description = description

    return embed


def create_info_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, "INFO")

    embed.title = title
    embed.description = description

    return embed


def create_error_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, "ERROR")

    embed.title = title
    embed.description = description

    return embed


def create_warning_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, "WARNING")

    embed.title = title
    embed.description = description

    return embed


def create_success_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, "SUCCESS")

    embed.title = title
    embed.description = description

    return embed
