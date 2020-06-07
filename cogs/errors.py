import traceback
import sys
from discord.ext import commands
import discord

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            print("Command not found: ", error)
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            return await ctx.send(error)

        else:
            print(error)
            return

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
