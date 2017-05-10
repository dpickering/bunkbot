import json
from discord.ext import commands
from .util.cog_wheel import CogWheel

CRYPTO_DESCRIPTION = """Retrieve the current price of BTC"""

BPI_API = "http://api.coindesk.com/v1/bpi/"


class Crypto(CogWheel):
    def __init__(self, bot, fiat_currency="USD"):
        CogWheel.__init__(self, bot)
        self.fiat = fiat_currency

    """
    Dynamic property that will be used to
    find a current cryptocurrency price
    """
    @property
    def curr_price_bpi_api(self):
        return BPI_API + "currentprice/" + self.fiat + ".json"

    """
    Executable command which will
    display current BTC price
    """
    @commands.command(pass_context=True, cls=None, help=CRYPTO_DESCRIPTION)
    async def btc(self, ctx):
        try:
            await self.bot.send_typing(ctx.message.channel)
            print(self.curr_price_bpi_api)
            curr_btc_price_result = self.http_get(self.curr_price_bpi_api)
            print(curr_btc_price_result)
            # await self.send_message_plain("FOO")
            await self.send_message("Current BTC price", "TEST TEST", None, "Price info courtesy of Coindesk", None)
        except Exception as e:
            print(e)
            await self.handle_error(e)


def setup(bot):
    bot.add_cog(Crypto(bot))
