import sched, time
import discord
from discord.ext import commands

class RemindMe:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = sched.scheduler(time.time, time.sleep)

    @commands.command(pass_context=True)
    async def remindme(self, ctx): 
        await ctx.bot.say("Refactored! Great job kev")

def setup(bot):
    bot.add_cog(RemindMe(bot))