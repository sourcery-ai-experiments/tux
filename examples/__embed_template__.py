from datetime import datetime
import discord

def hello_embed(self) -> discord.Embed:
    """
    Create a sample embed.
    You can find the official docs at: https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#discord.Embed

    Notes:
    - This is for documentation purposes.
    """

    """
        The below code creates a simple embed.
        
        The embed is created with:
        - A random color.
        You can read more about colors here: https://discordpy.readthedocs.io/en/latest/api.html?highlight=colour#discord.Colour
        - A title set to "Hello, World!"
        - A description set to "This is a sample embed."
        - And a timestamp set to utcnow, you can use other time formats.
        - See here: https://docs.python.org/3/library/datetime.html
        
        You can also set an image for the embed using an url.
        Example: url="https://pixmap.com/dog.png"
    """
    hello_world: discord.Embed = discord.Embed(
        color=discord.Color.random(),
        title="Hello, World!",
        description="This is a sample embed.",
        timestamp=datetime.utcnow(),
    )

    """
        The rest of the fields are readonly, meaning we can't access them directly.
        But, discord.py offers some methods to edit them indirectly!
        Below are some examples.
        """

    """
        Here, we set the author of the embed.
        You can set this to anything.
        This method takes three parameters
        
        name, with the type of string, which sets the name at the top of the embed,
        url, which sets the url for the name,
        and icon_url, which, if set, will add an icon next to the name.
    """
    hello_world.set_author(
        name="Tux", url="https://mysite.org", icon_url="https://picsum.photos/128"
    )

    """
        Using the add_field method, we can set fields to the embed.

        fields can be inline, which means they will be rendered NEXT to eachother.
        Although, only three fields per row can be rendered that way.
        You can set inline to false to make the next field render below

        NOTE: inline only works on computers, on mobile all fields are rendered below eachother, even inline is set to true.
    """
    hello_world.add_field(
        name="This is some info", value="Description of said info", inline=True
    )

    hello_world.add_field(
        name="This is some info", value="Description of said info", inline=True
    )

    hello_world.add_field(
        name="This is some info", value="Description of said info", inline=False
    )

    """
        With embeds, we can set thumbnails.
        What this means is that we can add a small icon be shown at the top right corner of the embed.
        
        We do this using the set_thumbnail method.
    """
    hello_world.set_thumbnail(url="https://picsum.photos/128")

    """
        We can also set images, which will be a large image rendered at the bottom of the embed.
        We achieve this using the set_image method.
    """
    hello_world.set_image(url="https://picsum.photos/500")

    """
        And finally, we can also set footers.

        Footers are small pieces of text, or an icon that is rendered at the bottom left corner of an embed.
        We do this using the set_footer method.
    """
    hello_world.set_footer(text="Made with love,", icon_url="https://picsum.photos/128")

    return hello_world
