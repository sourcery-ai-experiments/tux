import discord
from discord import Embed, app_commands
from discord.ext import commands
from loguru import logger

from tux.utils.embeds import EmbedCreator
from tux.utils.pagination import InteractionListMenuView

des_ids = [
    [1175177565086953523, "_kde"],
    [1175177703066968114, "_gnome"],
    [1175177036990533795, "_i3"],
    [1175222139046080582, "_hyprland"],
    [1175177087183769660, "_sway"],
    [1175243354557128765, "_xfce"],
    [1175220317174632489, "_dwm"],
    [1175177142108160121, "_bspwm"],
    [1181288708977205318, "_cinnamon"],
    [1175242546012753941, "_xmonad"],
    [1175241189935550554, "_awesome"],
    [1175245686489501726, "_mate"],
    [1175241537689489408, "_qtile"],
    [1175221470587256852, "_emacs"],
    [1175240614124732487, "_herbstluft"],
    [1175219898113331331, "_icewm"],
    [1175337897180803082, "_openbox"],
    [1175336806963744788, "_wayfire"],
    [1185972642260455445, "_berry"],
    [1192097654818226256, "_leftwm"],
    [1192149690096033882, "_budgie"],
    [1196324646170148925, "_riverwm"],
    [1212033435858898995, "_enlightenment"],
    [1212031657805221930, "_stumpwm"],
]

distro_ids = [
    [1227797149706879047, ""],
    [1223679701122551891, ""],
    [1224789424240459889, ""],
    [1223693433772707880, ""],
    [1223693380739924018, ""],
    [1223693346699214999, ""],
    [1223693813415936030, ""],
    [1223687364736712737, ""],
    [1224049583919857664, ""],
    [1224060704970248222, ""],
    [1232404504331161691, ""],
    [1232404504331161691, ""],
    [1232404490808856596, ""],
    [1232404477315907584, ""],
    [1232404453894918215, ""],
    [1232404354925854801, ""],
    [1224853095033606186, ""],
    [1232405040589836410, ""],
    [1232405056268271627, ""],
    [1232405210949746788, ""],
    [1232405261730447391, ""],
    [1232405297226842202, ""],
    [1232405397965373502, ""],
    [1232405452944576522, ""],
    [1232405490143854644, ""],
    [1232405533944709241, ""],
    [1232405623207891056, ""],
    # [1175176142899122246, "_arch"],
    # [1175176866928263220, "_debian"],
    # [1175176922460860517, "_fedora"],
    # [1175176812293271652, "_ubuntu"],
    # [1175235143707918436, "_windows"],
    # [1175176279616663573, "_gentoo"],
    # [1175227850119458897, "_freebsd"],
    # [1175177831551086593, "_nixos"],
    # [1175178088347344916, "_void"],
    # [1175176981936087161, "_opensuse"],
    # [1175244437530611712, "_macos"],
    # [1175241975818092564, "_alpine"],
    # [1175177993526726717, "_linuxmint"],
    # [1175221054684286996, "_openbsd"],
    # [1176533514385096714, "_bedrock"],
    # [1178347402730688542, "_endeavouros"],
    # [1178391378812735508, "_artix"],
    # [1182152672447569972, "_slackware"],
    # [1178347123905929316, "_popos"],
    # [1175177750143848520, "_kisslinux"],
    # [1180570700734546031, "tux"],
    # [1191106506276479067, "_garuda"],
    # [1192177499413684226, "_asahi"],
    # [1207599112585740309, "_fedoraatomic"],
]

lang_ids = [
    [1175612831996055562, "_python"],
    [1175612831861837864, "_bash"],
    [1175612831941525574, "_html"],
    [1175612831115260006, "_javascript"],
    [1175612831652139008, "_c"],
    [1175612832029609994, "_cplusplus"],
    [1175612831790534797, "_lua"],
    [1175612831631155220, "_rust"],
    [1175612831907979336, "_java"],
    [1175612831798939648, "_csharp"],
    [1178389324098699294, "_php"],
    [1175612831798931556, "_haskell"],
    [1175612831727632404, "_ruby"],
    [1175612831828295680, "_kotlin"],
    [1175739620437266443, "_go"],
    [1175612831731822734, "_lisp"],
    [1175612831920558191, "_perl"],
    [1185975879231348838, "_asm"],
    [1175612830389633164, "_ocaml"],
    [1175612831727620127, "_erlang"],
    [1175612831287218250, "_zig"],
    [1175612831878615112, "_julia"],
    [1175612831429824572, "_crystal"],
    [1175612831761182720, "_elixir"],
    [1207600618542206976, "_clojure"],
]

vanity_ids = [
    [1179277471883993219, "wheel"],
    [1197348658052616254, "mag"],
    [1175237664811790366, "regional_indicator_e"],
    [1186473849294962728, "smirk_cat"],
    [1180568491527516180, "supertuxkart"],
    [1179551412070404146, "100"],
    [1183896066588950558, "rabbit"],
    [1192245668534833242, "cd"],
    [1179551519624925294, "hugging"],
    [1183897526613577818, "hdtroll"],
    [1175756229168079018, "_git"],
    [1197353868103782440, "goblin"],
    [1202544488262664262, "bar_chart"],
    [1186473904773017722, "man_mage"],
    [1208233484230074408, "ghost"],
    [1217601089721995264, "old_man"],
    [1217866697751400518, "ear_of_rice"],
    [1212039041269366854, "chess_pawn"],
]

misc_ids = [
    [1182069378636849162, "_vsc"],
    [1180571441276649613, "_nvim"],
    [1180660198428393643, "_emacs"],
    [1192140446919561247, "_gnunano"],
    [1193242175295729684, "_kate"],
    [1192135710443065345, "_micro"],
    [1193241331221405716, "_jetbrains"],
    [1185974067472380015, "_helix"],
    [1192139311919935518, "_kakoune"],
    [1187804435578093690, "_ed"],
    [1189236454153527367, "_gecko"],
    [1189236400571301958, "_chromium"],
]

# # TODO: Figure out how to make this work without hard coding the roles and emojis.


# class RoleCount(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot

#     @app_commands.command(name="rolecount", description="Shows the number of users in each role.")
#     @app_commands.describe(which="Which option to list!")
#     @app_commands.choices(
#         which=[
#             app_commands.Choice(name="Distro", value="ds"),
#             app_commands.Choice(name="Language", value="lg"),
#             app_commands.Choice(name="DE/WM", value="de"),
#             app_commands.Choice(name="Misc", value="misc"),
#             app_commands.Choice(name="Vanity", value="vanity"),
#         ]
#     )
#     async def rolecount(
#         self, interaction: discord.Interaction, which: discord.app_commands.Choice[str]
#     ) -> None:
#         embed = EmbedCreator.create_info_embed(
#             title="Role Count",
#             description=f"Here is the number of users in each {which.name} role.",
#             interaction=interaction,
#         )

#         if interaction.guild:
#             match which.value:
#                 case "ds":  # Distros
#                     roles_emojis = distro_ids

#                 case "lg":  # Languages
#                     roles_emojis = lang_ids

#                 case "de":  # DE/WMs
#                     roles_emojis = des_ids

#                 case "misc":  # Misc roles
#                     roles_emojis = misc_ids

#                 case "vanity":  # Vanity roles
#                     roles_emojis = vanity_ids

#                 case _:  # Default case
#                     roles_emojis = []

#             for role_emoji in roles_emojis:
#                 role_id = int(role_emoji[0])
#                 role = interaction.guild.get_role(role_id)
#                 emoji = None

#                 if role:
#                     emoji = role.unicode_emoji or discord.utils.get(
#                         self.bot.emojis, name=role_emoji[1]
#                     )

#                 if role and emoji:
#                     embed.add_field(
#                         name=f"{emoji!s} {role.name}",
#                         value=f"{len(role.members)} users",
#                         inline=True,
#                     )
#                 else:
#                     missing = "Role" if role is None else "Emoji"
#                     logger.warning(
#                         f"Cannot find {missing} with ID {role_emoji[0]} or name {role_emoji[1]}"
#                     )

#         await interaction.response.send_message(embed=embed)

#         logger.info(f"{interaction.user} requested role count for {which.name}.")


# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(RoleCount(bot))


# class RoleCount(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot

#     @app_commands.command(name="rolecount", description="Shows the number of users in each role.")
#     @app_commands.describe(which="Which option to list!")
#     @app_commands.choices(
#         which=[
#             app_commands.Choice(name="Distro", value="ds"),
#             app_commands.Choice(name="Language", value="lg"),
#             app_commands.Choice(name="DE/WM", value="de"),
#             app_commands.Choice(name="Misc", value="misc"),
#             app_commands.Choice(name="Vanity", value="vanity"),
#         ]
#     )
#     async def rolecount(
#         self, interaction: discord.Interaction, which: discord.app_commands.Choice[str]
#     ) -> None:
#         if interaction.guild:
#             match which.value:
#                 case "ds":  # Distros
#                     roles_emojis = distro_ids
#                 case "lg":  # Languages
#                     roles_emojis = lang_ids
#                 case "de":  # DE/WMs
#                     roles_emojis = des_ids
#                 case "misc":  # Misc roles
#                     roles_emojis = misc_ids
#                 case "vanity":  # Vanity roles
#                     roles_emojis = vanity_ids
#                 case _:  # Default case
#                     roles_emojis = []

#             pages: list[discord.Embed] = []

#             embed = EmbedCreator.create_info_embed(
#                 title=f"{which.name} Roles",
#                 description="Number of users in each role",
#                 interaction=interaction,
#             )

#             role_count = 0

#             for role_emoji in roles_emojis:
#                 role_id = int(role_emoji[0])
#                 if role := interaction.guild.get_role(role_id):
#                     if role_count >= 25:
#                         pages.append(embed)
#                         embed = EmbedCreator.create_info_embed(
#                             title=f"{which.name} Roles",
#                             description="Number of users in each role",
#                             interaction=interaction,
#                         )
#                         role_count = 0

#                     emoji = role.unicode_emoji or discord.utils.get(
#                         self.bot.emojis, name=role_emoji[1]
#                     )

#                     embed.add_field(
#                         name=f"{emoji!s} {role.name}",
#                         value=f"{len(role.members)} users",
#                         inline=True,
#                     )
#                     role_count += 1

#             if role_count > 0:
#                 pages.append(embed)

#             if pages:
#                 paginator = InteractionListMenuView(user_id=interaction.user.id, listmenu=pages)
#                 await paginator.start(interaction.response)
#             else:
#                 await interaction.response.send_message(
#                     "No roles found to display.", ephemeral=True
#                 )

#         logger.info(f"{interaction.user} requested role count for {which.name}.")


# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(RoleCount(bot))


class RoleCount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roles_emoji_mapping = {
            "ds": distro_ids,
            "lg": lang_ids,
            "de": des_ids,
            "misc": misc_ids,
            "vanity": vanity_ids,
        }

    @app_commands.command(name="rolecount", description="Shows the number of users in each role.")
    @app_commands.describe(which="Which option to list!")
    @app_commands.choices(
        which=[
            app_commands.Choice(name="Distro", value="ds"),
            app_commands.Choice(name="Language", value="lg"),
            app_commands.Choice(name="DE/WM", value="de"),
            app_commands.Choice(name="Misc", value="misc"),
            app_commands.Choice(name="Vanity", value="vanity"),
        ]
    )
    async def rolecount(
        self, interaction: discord.Interaction, which: discord.app_commands.Choice[str]
    ) -> None:
        if interaction.guild:
            roles_emojis = self.roles_emoji_mapping.get(which.value, [])
            await self.process_roles(interaction, roles_emojis, which)

        logger.info(f"{interaction.user} requested role count for {which.name}.")

    async def process_roles(
        self,
        interaction: discord.Interaction,
        roles_emojis: list[tuple[str, str]],
        which: discord.app_commands.Choice[str],
    ) -> None:
        pages = []
        role_count = 0
        embed = self.create_embed(interaction, which)

        for role_emoji in roles_emojis:
            role_id = int(role_emoji[0])
            if role := interaction.guild.get_role(role_id):
                role_count, embed = self.format_embed(
                    embed, interaction, role, role_count, role_emoji, which, pages
                )

        if embed.fields:
            pages.append(embed)

        await self.send_response(interaction, pages)

    def format_embed(self, embed, interaction, role, role_count, role_emoji, which, pages):
        if role_count >= 25:
            pages.append(embed)
            embed = self.create_embed(interaction, which)
            role_count = 0

        emoji = role.unicode_emoji or discord.utils.get(self.bot.emojis, name=role_emoji[1])

        embed.add_field(
            name=f"{emoji!s} {role.name}",
            value=f"{len(role.members)} users",
            inline=True,
        )
        role_count += 1

        return role_count, embed

    def create_embed(self, interaction, which):
        return EmbedCreator.create_info_embed(
            title=f"{which.name} Roles",
            description="Number of users in each role",
            interaction=interaction,
        )

    async def send_response(self, interaction: discord.Interaction, pages: list[Embed]):
        if pages:
            paginator = InteractionListMenuView(user_id=interaction.user.id, listmenu=pages)
            await paginator.start(interaction.response)
        else:
            await interaction.response.send_message("No roles found to display.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleCount(bot))
