""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import platform
import random
from discord.utils import get, format_dt
from discord import app_commands
from typing import Optional, Union
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    # Message context menu command
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

        :param interaction: The application command interaction.
        :param message: The message that is being interacted with.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Message without spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        Grabs the ID of the user.

        :param interaction: The application command interaction.
        :param user: The user that is being interacted with.
        """
        embed = discord.Embed(
            description=f"The ID of {user.mention} is `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="hostinfo",description="Information about the host's computer")
    @commands.guild_only()
    async def hostinfo(self,ctx):
        """
        A useful command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@466778567905116170>")

        embed.set_footer(text=f"Made By | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name='userinfo',
        description='Get info on a user')
    async def userinfo(self, context: Context, *, member: discord.Member=None):
        """
        Get some useful (or not) information about the bot.

        :param user: The user to get info for.
        """
        if member is None:
            member = context.author
        elif member is not None:
            member = member

        info_embed = discord.Embed(title=f"{member.name}'s User Info", description="Information about this user")
        info_embed.set_thumbnail(url=member.avatar)
        info_embed.add_field(name="Name: ", value=member.name)
        info_embed.add_field(name="web status", value=member.web_status)
        info_embed.add_field(name="On Mobile? ", value=member.is_on_mobile())
        info_embed.add_field(name="True Mobile Status ", value=member.mobile_status)
        info_embed.add_field(name="Status: ", value=member.status)
        info_embed.add_field(name="Desktop Status: ", value=member.desktop_status)
        info_embed.add_field(name="roles: ", value=member.roles)
        info_embed.add_field(name="Joined this Server: ", value=member.joined_at)
        info_embed.add_field(name="Nickname", value=member.nick)
        info_embed.add_field(name="Highest Role: ", value=member.top_role)
        info_embed.add_field(name="Avatar: ", value=member.avatar)
        info_embed.add_field(name="Created At: ", value=member.created_at.__format__("%A, %d, %B %Y @ %H:%M:%S"))
        info_embed.add_field(name="Discriminator: ", value=member.discriminator)
        info_embed.add_field(name="Bot?", value=member.bot)
        info_embed.add_field(name="ID: ", value=member.id)
        info_embed.add_field(name="Current Activities", value=member.activities)
        info_embed.add_field(name="Mentionable String", value=member.mention)

        await context.send(embed=info_embed)
    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        embed = discord.Embed(
            description="Just a bot.",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Hello there!", value="I am a bot.", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=True,
        )
        embed.add_field(
            name="Servers:",
            value=f"{context.bot.guilds}",
            inline=True
        )
        embed.add_field(
            name="Owner:",
            value=f"<@{context.bot.owner_id}>",
            inline=True
        )
        embed.add_field(
            name="Bot ID:",
            value=f"{context.bot.application_id}",
            inline=True
        )
        embed.set_footer(text=f"Requested by {context.author.id}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @commands.cooldown(1, 14, commands.BucketType.user)
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displayin [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        embed = discord.Embed(
            description=f"Invite me by clicking [here]({self.bot.config['invite_link']}).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    async def server(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        embed2 = discord.Embed(
            title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
        )
        user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
        if user_is_blacklisted:

            print("here!")
            await context.send(embed=embed2)
            return
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"The question was: {question}")
        await context.send(embed=embed)

    # @commands.hybrid_command(
    #     name="bitcoin",
    #     description="Get the current price of bitcoin.",
    # )
    # async def bitcoin(self, context: Context) -> None:
    #     """
    #     Get the current price of bitcoin.

    #     :param context: The hybrid command context.
    #     """
    #     # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
    #     # embed2 = discord.Embed(
    #     #     title="Command failed!", description="Haha you're blacklisted, so you can't use this command.:", color=0xBEBEFE
    #     # )
    #     # user_is_blacklisted = await self.bot.database.is_blacklisted(context.author.id)
    #     # if user_is_blacklisted:

    #     #     print("here!")
    #     #     await context.send(embed=embed2)
    #     #     return
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(
    #             "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    #         ) as request:
    #             if request.status == 200:
    #                 data = await request.json(
    #                     content_type="application/javascript"
    #                 )  # For some reason the returned content is of type JavaScript
    #                 embed = discord.Embed(
    #                     title="Bitcoin price",
    #                     description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
    #                     color=0xBEBEFE,
    #                 )
    #             else:
    #                 embed = discord.Embed(
    #                     title="Error!",
    #                     description="There is something wrong with the API, please try again later",
    #                     color=0xE02B2B,
    #                 )
    #             await context.send(embed=embed)

    @commands.hybrid_command(name="banner", description="Display the banner.")
    @commands.cooldown(1, 14, commands.BucketType.user)
    async def banner(self, ctx: Context, user: Optional[Union[discord.Member, discord.User]]) -> None:
        if not user: 
            user = ctx.author
        user = await self.bot.fetch_user(user.id)
        if banner := user.banner:
            await ctx.send(banner.url)
        else:
            await ctx.send("This user doesn't have a banner.")
    @commands.hybrid_command(name="emojiinfo", aliases=["ei"])
    @commands.cooldown(1, 14, commands.BucketType.user)
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.ext.commands.errors.EmojiNotFound:
            return await ctx.reply("I couldn't find this emoji in the givin guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
    **General:**
    **- Name:** {emoji.name}
    **- Id:** {emoji.id}
    **- URL:** [Link To Emoji]({emoji.url})
    **- Author:** {emoji.user.mention}
    **- Time Created:** {creation_time}
    **- Usable by:** {can_use_emoji}
    
    **Other:**
    **- Animated:** {is_animated}
    **- Managed:** {is_managed}
    **- Requires Colons:** {requires_colons}
    **- Guild Name:** {emoji.guild.name}
    **- Guild Id:** {emoji.guild.id}
    """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))
