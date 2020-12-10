import re
import discord
import inspect
from discord.ext import commands


class AdminCog(commands.Cog, name="Admin Commands"):
    def __init__(self, client):
        self.client = client
        self.tonys_a_cunt = [
            "\u0628",
            "\u064d",
            "\u0631",
        ]

    @commands.command(name="run", hidden=True)
    @commands.is_owner()
    async def run(self, ctx, *, code):
        if not isinstance(ctx.channel, discord.DMChannel) or not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.message.delete()
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'bot': self.client,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }
        env.update(globals())
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send(python.format(result))

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        if not isinstance(ctx.channel, discord.DMChannel) or not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.message.delete()
        """Command which Loads a Module."""
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`**\n {type(e).__name__} - {e}')
        else:
            msg = await ctx.send(f"`{cog}` has been loaded!")
            await msg.delete(delay=5)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        if not isinstance(ctx.channel, discord.DMChannel) or not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.message.delete()
        """Command which Unloads a Module."""
        try:
            if cog == "modules.admin":
                msg = await ctx.send("It's not recommended to unload the admin cog.")
                await msg.delete(delay=5)
                return
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`**\n {type(e).__name__} - {e}')
        else:
            msg = await ctx.send(f"`{cog}` has been unloaded!")
            await msg.delete(delay=5)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        if not isinstance(ctx.channel, discord.DMChannel) or not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.message.delete()
        """Command which Reloads a Module."""
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            msg = await ctx.send(f"`{cog}` has been reloaded!")
            await msg.delete(delay=5)

    def filter_message(self, message):
        message = message.replace(" ", "")
        regexes = [  # Probably use this as a config list in a json file
            r"(n|ñ|ń)+.*(i|î|ï|í|ī|ī|į|ì)+.*g{2,}.*(a|à|á|â|ä|æ|ã|å|ā)*.*",
            r"(n|ñ|ń)+.*(i|î|ï|í|ī|ī|į|ì)+.*g{2,}.*(e|è|é|ê|ë|ē|ė|ę)*.*r*.*"
        ]
        for reg in regexes:
            matches = re.finditer(reg, message, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                test = matchNum
            try:
                tester = test
                print("Bad stuff afloat!")
                return True
                break
            except NameError:
                print("Nothing bad here!")
                return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(bad in message.content for bad in self.tonys_a_cunt):
            await message.delete()
            dmchannel = await message.author.create_dm()
            await dmchannel.send("You're a cunt for trying that.")
            return


def setup(client):
    client.add_cog(AdminCog(client))
