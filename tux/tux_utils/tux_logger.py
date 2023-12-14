import os
import logging
import colorlog
from discord.ext import commands

# ==================
# Usage Instructions
# ==================
# Hey contributor, Ty here! To use the logger in your cog files, please follow these steps:

# 1. Import the logger by adding the following line at the top of your main bot file:
#    from your_module_name import logger

# 2. Once imported, you can use the logger to log messages in your code. For example:
#    logger.info("This is an information message.")
#    logger.warning("This is a warning message.")
#    logger.error("This is an error message.")
#    logger.debug("This is a debug message.")

# I love you all and thank you for contributing <3
# =========================
# End of Usage Instructions
# =========================


class TuxLogger(logging.Logger):
    def __init__(self,
                 name,
                 project_logging_level=logging.INFO):
        """
        Constructor for the custom logger class.

        Parameters:
        - name: The name of the logger.
        - project_logging_level: The logging level for the project (default is INFO).
        """
        super().__init__(name, level=project_logging_level)
        self._setup_logging()

    def _setup_logging(self):
        """
        Set up the logging configuration for the custom logger.
        """
        log_format = '%(asctime)s [%(log_color)s%(levelname)s%(reset)s]: %(message)s'
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(log_format))
        self.addHandler(handler)

        file_handler = logging.FileHandler(
                os.path.join(log_dir, 'bot.log'),
                mode='a'
        )
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
        self.addHandler(file_handler)


class LoggingCog(commands.Cog):
    def __init__(self,
                 bot,
                 discord_logging_level=logging.WARNING):
        """
        Constructor for the LoggingCog class.

        Parameters:
        - bot: The Discord bot instance.
        - discord_logging_level: The logging level for the Discord library (default is WARNING).
        """
        self.bot = bot
        self.discord_logging_level = discord_logging_level

        discord_logger = logging.getLogger('discord')
        discord_logger.setLevel(self.discord_logging_level)


logger = TuxLogger(__name__)


async def setup(bot,
                project_logging_level=logging.DEBUG,
                discord_logging_level=logging.WARNING):
    """
    Asynchronous function to set up the LoggingCog and add it to the Discord bot.

    Parameters:
    - bot: The Discord bot instance.
    - project_logging_level: The logging level for the project (default is DEBUG).
    - discord_logging_level: The logging level for the Discord library (default is WARNING).
    """
    global logger
    log_cog = LoggingCog(
        bot,
        discord_logging_level
    )
    logger.setLevel(project_logging_level)
    await bot.add_cog(log_cog)
