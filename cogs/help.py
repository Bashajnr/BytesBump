import discord
from Admin.admin import Files

commands = discord.ext.commands

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    print(1)
    return await ctx.send(embed=discord.Embed(
      title="Advertiser Bump | Help",
      description=Files.read("Admin/Help/front.page"),
      color=discord.Color.blurple()
    )
    .set_footer(text="Powered by • DumbBot Advertising")
    .set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png")))

def setup(bot):
  bot.add_cog(Help(bot))
