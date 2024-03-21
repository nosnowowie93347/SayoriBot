from better_profanity import profanity
from discord.ext.commands import Cog

profanity.load_censor_words_from_file("./data/profanity.txt")


class AutoMod(Cog):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and profanity.contains_profanity(message.content):
            await message.delete()
            await message.channel.send("You can't use that word here.", delete_after=10)


async def setup(bot):
    await bot.add_cog(AutoMod(bot))
