import discord
from discord.ext import commands
import io
import textwrap
import os
import traceback
from contextlib import redirect_stdout
from Admin.admin import Files
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix=Files.config("main","prefix"), intents=intents, case_insensitive=True, owner_ids=Files.config("main", "managers"))
bot.remove_command("help")


def is_owner():
  def predicate(ctx):
    return ctx.author.id in bot.owner_ids
  return commands.check(predicate)

@is_owner()
@bot.command(aliases=["e"])
async def eval(ctx, *, body: str):
    raw = False
    """Evaluates a code"""

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'guild': ctx.message.guild,
        'message': ctx.message,
       }
    env.update(globals())

    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
          ret = await func()
    except Exception:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                if raw:
                  await ctx.send(f"{value}")
                else:
                  await ctx.send(f'```py\n{value}\n```')
        else:
            pass

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over BytesToBits"))

@is_owner()
@bot.command(hidden=True)
async def load(ctx, *, module):
    try:
      bot.load_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Loaded {str(module).capitalize()}", description=f"Successfully loaded cogs.{str(module).lower()}!", color=0x2cf818)
      await ctx.send(embed=embed)

@is_owner()
@bot.command(hidden=True)
async def unload(ctx, *, module):
    try:
      bot.unload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Unloaded {str(module).capitalize()}", description=f"Successfully unloaded cogs.{str(module).lower()}!", color=0xeb1b2c)
      await ctx.send(embed=embed)

@is_owner()
@bot.command(name="reload")
async def _reload(ctx, *, module):
    try:
      bot.reload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Reloaded {str(module).capitalize()}", description=f"Successfully reloaded cogs.{str(module).lower()}!", color=0x00d4ff)
      await ctx.send(embed=embed)

for i in os.listdir("cogs"):
  if i == "staff": pass
  else:
    cog = i[:-3]
    try:
      bot.load_extension(f"cogs.{cog}")
      print(f"Loaded Main.{cog}")
    except Exception as e:
      print(e)
    
bot.run(Files.config("main", "token"))
