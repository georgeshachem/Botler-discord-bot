import discord
from discord.ext import commands
import json
import traceback
from os import listdir
from os.path import isfile, join

with open('resources/config.json') as data_file:
    config = json.load(data_file)


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = config['prefixes']

    if not message.guild:
        return '&'

    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix,
                   description=config['description'])

bot.cogs_dir = config['cogs_dir']

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(bot.cogs_dir) if isfile(join(bot.cogs_dir, f))]:
        try:
            bot.load_extension(bot.cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.run(config['token'])
