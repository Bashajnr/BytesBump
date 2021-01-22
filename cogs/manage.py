import discord
import asyncio
from discord.ext import commands
from asyncio import sleep

def convert(time): #makes life easier and looks better overall
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)

class Events(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    
    #e
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        switch = {
            commands.TooManyArguments: "You have given to many arguments\nPlease use the command as directed",
            commands.BotMissingPermissions: "I am missing permissions.",
            commands.CheckAnyFailure: "An unknown error has occured.",
            commands.errors.NSFWChannelRequired: "You must use this in a channel marked ***NSFW***",
            commands.errors.NoPrivateMessage: "This user has blocked me or does not accept private messages.",
            discord.ext.commands.DisabledCommand: "This command is disabled",
            discord.errors.Forbidden: "I do not have permission to use this command"
        }

        global time
        if isinstance(error, commands.CommandNotFound):
            pass #this is just to make sure it doesnt send a message when command not found
        elif isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after
            time = convert(time)
            x = time.split(":") #this fuckwad of an if statement checks hours minutes seconds, etc
            if x[1] != '0' and x[2] != '0':
                if x[1] == 1:
                    message = f'Retry this command after **{x[1]}** hour(s) and **{x[2]}** minutes!'
                else:
                    message = f'Retry this command after **{x[1]}** hour(s) and **{x[2]}** minutes!'
            elif x[1] == '0' and x[2] != '0' and x[3] != 0:
                message = f'Retry this command after **{x[2]}** minutes and **{x[3]}** seconds!'
            elif x[3] != '0' and x[1] == '0' and x[2] == '0':
                message = f'Retry this command after **{x[3]}** seconds!'
            msg = await ctx.send(message)
            await sleep(3)
            await msg.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = await ctx.send("**You have made an error.**\n\n{}".format(error.param))
            await sleep(3) #missing params, can get rid of
            await msg.delete()
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            msg = await ctx.send('The cog {} is already loaded.'.format(error.args[0]))
            await sleep(3) #cog is already loaded
            await msg.delete()
        elif isinstance(error, commands.MissingPermissions):
            msg = await ctx.send('You need **{}** perms to complete this actions.'.format(error.missing_perms[0]))
            await sleep(3) #user missing perms
            await msg.delete()
        elif isinstance(error, commands.BotMissingAnyRole):
            msg = await ctx.send('**Woops!**\n\nLooks like i am missing the {} role.'.format(error.missing_role))
            await sleep(3) #bot missing role
            await msg.delete()
        elif isinstance(error, commands.errors.NotOwner):
            msg = await ctx.send('Only **{}** can use this command.'.format(ctx.guild.owner))
            await sleep(3) #owner only commmands
            await msg.delete()
        else:
            await ctx.send(switch.get(type(error), "an unknown error occured"), delete_after=3.0)
        #uncomment to log every error
        # print(error)

def setup(bot):
    bot.add_cog(Events(bot))