import discord, os, sys
import motor.motor_asyncio
import json
from discord.ext import commands
from discord.ext.commands import Context
from SpamFilter import AntiSpam


if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

# you can have as many levels as you like
level = ["Level 1", "Level 2", "Level 3"] #you'll have to create roles (aka the levels) and put them here. So if my roles were Level 1, Level 2, and Level 3, then I'll use this
levelnum = [10,20,30]
bot_channel = 986737668316627004#put the channel ID here. You can get the channel ID by heading over to the channel > right click > copy channel ID
talk_channels = [986737670430543993, 986737668316627004, 986737673609830490] #ID's of every channel wherein you want the bot to allot xp to a user
class Level(commands.Cog):
    """This docstring is to force pylint to shut up about a missing docstring."""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        dictionary_check = False # Default is False, DO NOT USE THIS IF YOUR SERVER IS MULTI-LINGUAL, Checks if any word in the message is present in english dictionary.
        timer_check = True # Default is True, Checks if a member has sent more than 5 messages within 15 seconds, if yes, 6th message is marked as spam.
        content_check = True # Default is True, Checks the message's content and if a letter whose occurance in the content is highest covers more than 85% of the content, it marks the message as spam.
        history_check = True # Default is True, Checks if the message's content is duplicate of the previous message.

        if await AntiSpam(dictionary = dictionary_check,timer = timer_check,content = content_check,history = history_check).check(self.bot, message.channel, message.author):
            return
        if message.channel.id in talk_channels: #to check if it's in the right channel
            stats = await self.bot.connection.find_one({"id":message.author.id}) #replace collection_name with your collection's name
            if not message.author.bot: #to check that it isn't levelling the bot up.
                if stats is None: #to check if they're registered
                    newuser = {"id" : message.author.id, "xp" : 0}
                    await self.bot.connection.insert_one(newuser) #replace collection_name with you collection's name; this is to insert the details into the database
                else: #means that they're registered
                    xp = stats["xp"] + 1 #increases xp by 1
                    await self.bot.connection.update_one({"id":message.author.id}, {"$set":{"xp":xp}}) #replace collection_name with your collection's name; is being ussed to update the databse
                    print(f"You've gained {xp} XP!")
                    #to find what level the user's at
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Congrats! {message.author.mention}! You leveled up to **level: {lvl}**!") #sending an alert when the user levels up
                        #to check if they got a new role or not
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention}. New role: **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar.url)
                                await message.channel.send(embed=embed)
    #to get rank
    @commands.hybrid_command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel: #to check if they're sending it in the right channel
            print("hello! We're here")
            stats = await self.bot.connection.find_one({"id" : ctx.author.id}) #replace collection_name with your collection's name
            if stats is None: #checks if the user has send messages or not. If not then it send the message mentioned below
                embed = discord.Embed(description="You need to send messages to obtain a rank!")
                await ctx.channel.send(embed=embed)
            else: #if the user has send messages to the right channel(s)
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20) #shows boxes (for visual effect)
                rankings = self.bot.colllection.find().sort("xp",-1) #replace collection_name with your collection's name
                async for x in rankings: #to show what rank they are
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                #using this to send all the info
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.channel.send(embed=embed)
#Leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = self.bot.connection.find().sort("xp",-1) #replace collection_name with your collection's name
            i = 1
            embed = discord.Embed(title="Rankings:")
            async for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)#to get rank
    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel: #to check if they're sending it in the right channel
            stats = await self.bot.connection.find_one({"id" : ctx.author.id}) #replace collection_name with your collection's name
            if stats is None: #checks if the user has send messages or not. If not then it send the message mentioned below
                embed = discord.Embed(description="You need to send messages to obtain a rank!")
                await ctx.channel.send(embed=embed)
            else: #if the user has send messages to the right channel(s)
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20) #shows boxes (for visual effect)
                rankings = self.bot.connection.find().sort("xp",-1) #replace collection_name with your collection's name
                async for x in rankings: #to show what rank they are
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                #using this to send all the info
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.channel.send(embed=embed)
#Leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = self.bot.connection.find().sort("xp",-1) #replace collection_name with your collection's name
            i = 1
            embed = discord.Embed(title="Rankings:")
            async for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)
async def setup(bot) -> None:
    await bot.add_cog(Level(bot))
