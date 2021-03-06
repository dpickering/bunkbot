import urllib.request, urllib.parse, re
from bs4 import BeautifulSoup
from discord.ext import commands
from .util.cog_wheel import CogWheel

YOUTUBE_DESCRIPTION = """
    Search for a youtube video with a given query. Display related videos with !more and re-link a related video with !ytl

    Example: !yt heroes of the storm
    Example: !more
    Example: !ytl 2
"""

YT_SEARCH_URL = "https://www.youtube.com/results?search_query="
YT_WATCH_URL = "https://www.youtube.com/watch?v="

class YouTube(CogWheel):
    def __init__(self, bot):
        CogWheel.__init__(self, bot)
        self.ids = []
        self.titles = []

    """
    Executable command method which will
    search and parse out the youtube html
    """
    @commands.command(pass_context=True, cls=None, help=YOUTUBE_DESCRIPTION)
    async def yt(self, ctx):
        try:
            await self.bot.send_typing(ctx.message.channel)
            
            self.ids = []
            self.titles = []
            params = self.get_cmd_params(ctx)

            if len(params) == 0:
                await self.send_message_plain("No youtube query given")
                return

            html = self.parse_query(" ".join(params))
            items = BeautifulSoup(html, "html.parser").find("ol", class_="item-section")
            ahref = BeautifulSoup(str(items), "html.parser").find_all("a")

            title_index = 0
            ahref_index = 0

            while title_index < 5 and ahref_index < len(ahref) - 1:
                result = ahref[ahref_index]
                href = result["href"]
                title = result.get("title")

                if re.match(r'\/watch\?v=(.{11})', href) and title is not None:
                    title_index += 1
                    self.ids.append(href.split("=")[1])
                    self.titles.append("{0}. {1}".format(title_index, title))

                ahref_index += 1

            if (len(self.ids) == 0):
                await self.send_message_plain("No ids found for " + query)
                return

            self.message = await self.send_message_plain(YT_WATCH_URL + self.ids[0])
        except Exception as e:
            await self.handle_error(e)

    """
    Relink a posted related video or
    the original by passing no param or the number 0
    """
    @commands.command(pass_context=True, clas=None, help="Link another youtube result from the last search using the number in the list")
    async def ytl(self, ctx):
        try:
            index = 0
            params = self.get_cmd_params(ctx)

            if len(params) >= 1:
                index = int(params[0])

                if not params[0].isdigit() or index > len(self.ids):
                    await self.send_message_plain("Please enter a valid video number from 0 to 5")
                    return
                else:
                    index -= 1

            self.message = await self.edit_message(self.message, YT_WATCH_URL + self.ids[index])
        except Exception as e:
            await self.handle_error(e)

    """
    Get a list of related videos from the last
    youtube search 
    """
    @commands.command(pass_context=True, clas=None, help=" Get a list of related videos from the last youtube search")
    async def more(self, ctx):
        await self.send_message("Type !ytl 1-5 to link another video\nType !ytl or !ytl 0 to relink the original result\n", "\n".join(self.titles))
        
    """
    Parse the given query string into a encoded url
    and open the url to read the html contents
    """
    def parse_query(self, query):
        query = urllib.parse.quote_plus(query)
        response = urllib.request.urlopen(YT_SEARCH_URL + query)
        html = response.read().decode()
        response.close()
        return html
    

def setup(bot):
    bot.add_cog(YouTube(bot))
