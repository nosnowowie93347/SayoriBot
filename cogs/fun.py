""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
A simple template to start to code your own and personalized discord bot in Python language.

Version: 6.1.0
"""

import random, re, json, os, io, requests, base64
import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import Context


class Choice(discord.ui.View):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**You lost!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        embed2 = discord.Embed(
            title="Command failed!",
            description="Haha you're blacklisted, so you can't use this command.:",
            color=0xBEBEFE,
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command()
    async def xkcd(self, ctx):
        """
        XKCD
        https://xkcd.com/
        """

        url = "https://c.xkcd.com/random/comic/"
        phrase = r"Image URL \(for hotlinking\/embedding\)\:.*"

        async with self.session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")

            img_url_nav_string = soup.find(text=re.compile(phrase))
            img_url = img_url_nav_string.find_next_sibling("a").text

            async with self.session.get(img_url) as response:
                img = io.BytesIO(await response.read())

            await ctx.send(file=discord.File(img, "xkcd.png"))

    @commands.hybrid_command()
    @commands.guild_only()
    async def meme(self, ctx):
        """Have a meme, friend!"""
        embed = discord.Embed(title="Meme", description="Here comes a meme!!")
        async with self.session.get(
            "https://www.reddit.com/r/dankmemes/new.json?sort=hot"
        ) as r:
            res = await r.json()
            embed.set_image(
                url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!",
            description="Haha you're blacklisted, so you can't use this command.:",
            color=0xBEBEFE,
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!",
            description="Haha you're blacklisted, so you can't use this command.:",
            color=0xBEBEFE,
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    @commands.hybrid_command(name="minecraft", aliases=["mcprofile", "mcinfo"])
    @commands.cooldown(1, 14, commands.BucketType.user)
    async def minecraft(self, context: Context, username):
        """
        Shows MC account info, skin and username history
        """
        try:
            uuid = requests.get(
                "https://api.mojang.com/users/profiles/minecraft/{}".format(username)
            ).json()["id"]

            url = json.loads(
                base64.b64decode(
                    requests.get(
                        "https://sessionserver.mojang.com/session/minecraft/profile/{}".format(
                            uuid
                        )
                    ).json()["properties"][0]["value"]
                ).decode("utf-8")
            )["textures"]["SKIN"]["url"]

            names = requests.get(
                "https://api.mojang.com/user/profiles/{}/names".format(uuid)
            ).json()
            history = "**Name History:**\n"
            for name in reversed(names):
                history += name[0] + "\n"

            await context.send(
                "**Username: `{}`**\n**Skin: {}**\n**UUID: {}**".format(
                    username, url, uuid
                )
            )
            await context.send(history)
        except ValueError as e:
            await context.send(e)
            await asyncio.sleep(2)
            await context.send("This means the profile wasn't found...")


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
