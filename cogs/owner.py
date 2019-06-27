from discord.ext import commands
import discord
import sys


class OwnerCog(commands.Cog, name='Owner Commands', command_attrs={'hidden': True}):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    async def load_cog(self, ctx, *, cog: str):
        """Load a Cog"""
        try:
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload')
    async def unload_cog(self, ctx, *, cog: str):
        """Unload a Cog"""
        try:
            self.bot.unload_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload')
    async def reload_cog(self, ctx, *, cog: str):
        """Reload a Cog"""
        try:
            self.bot.unload_extension("cogs." + cog)
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner('Owner only.')
        return True

    @commands.command(name='join')
    async def join_voice_channel(self, ctx, *, channel_name: str):
        """Join a Voice Channel by name"""
        voice_channels = [x for x in ctx.guild.voice_channels]
        for channel in voice_channels:
            if channel_name.lower() in channel.name.lower():
                await channel.connect()

    @commands.command(name='leave')
    async def leave_voice_channel(self, ctx, *, channel_name: str):
        """Leave a Voice Channel"""
        voice_clients = [x for x in self.bot.voice_clients]
        for client in voice_clients:
            if channel_name.lower() in client.channel.name.lower():
                await client.disconnect()

    @commands.command(aliases=['quit'])
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await self.bot.logout()
        sys.exit(0)

    @commands.command(name='game')
    async def change_game(self, ctx, *, game_name: str):
        """Change bot's currently playing game name"""
        await self.bot.change_presence(activity=discord.Game(name=game_name))

    @commands.command(name='status')
    async def change_status(self, ctx, status: str = ""):
        """Change bot's status between: offline, idle, dnd and online"""
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)

    @commands.command(name='name')
    async def change_name(self, ctx, *, name = None):
        """Change bot's name in the guild"""
        await ctx.guild.me.edit(nick=name)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
