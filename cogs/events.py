import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('-----------------------')
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('-----------------------')
        game = discord.Game(name="&help | {} servers".format(len(self.bot.guilds)))
        await self.bot.change_presence(activity=game)


def setup(bot):
    bot.add_cog(Events(bot))
