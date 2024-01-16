import interactions
from interactions import listen
import random

token_file = open("token.txt")
bot_token = token_file.read()

bot = interactions.Client(intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT, token=bot_token, 
                           sync_interactions=True)

# delete_unused_application_cmds=True // on startup to reset any dup commands
# debug_scope=1133920869773746359   //  debug scope to test server for insta sync commands

@listen()



@interactions.slash_command(
    name="dev_exit_command",
    description="quits the bot",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
)
async def exit_command_run(ctx: interactions.SlashContext):
    await ctx.send(ctx.author.mention + " quit the bot, Goodbye!" + (" (" + ctx.bot.owner.mention + " bot is down)"))
    await bot.stop()
    #exit()
    

@interactions.slash_command(
    name="hello",
    description="Sends a hello mesasge"
)
async def hello_command(ctx: interactions.SlashContext):
    await ctx.send("Hello!")

@interactions.slash_command(
    name="vx",
    description="fixes twitter embed",
)
@interactions.slash_option(
    name="link",
    description="twitter.com or x.com link",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
async def vx_embed(ctx: interactions.SlashContext, link: str):
    if "twitter" in link:
        link = link.replace("twitter", "vxtwitter")
    elif "x" in link:
        link = link.replace("x", "fixvx")
    else:
        link = "invalid link submitted"
    await ctx.send(link, silent=True)


# @listen(interactions.api.events.MessageCreate)
# async def fixembed(message):
#     if message.content.startswith("https://x"):
#         msg = message.content.replace("x", "fixvx")
#         msg = await message.channel.send(msg)
#     elif message.content.startswith("https://twitter"):
#         msg = message.content.replace("twitter", "vxtwitter")
#         msg = await message.channel.send(msg)

@listen("on_message_create")
async def fix_embed(event):
    fixed = event.message.content
    if "//twitter.com/" in fixed:
        fixed = fixed.replace("twitter", "vxtwitter")
        await event.message.reply(fixed, allowed_mentions=interactions.AllowedMentions(replied_user=False), silent=True)
    elif "//x.com/" in fixed:
        fixed = fixed.replace("x", "fixvx")
        await event.message.reply(fixed, allowed_mentions=interactions.AllowedMentions(replied_user=False), silent=True)

@interactions.slash_command(
    name="returnstring",
    description="returns the inputted string",
    scopes=[1133920869773746359],
)
@interactions.slash_option(
    name="text",
    description="String to respond with",
    opt_type=interactions.OptionType.STRING,
    required=True,
)
async def return_command(ctx: interactions.SlashContext, text: str):
    await ctx.send(f"You sent the string '{text}'!")


@interactions.slash_command(
    name="number",
    description="Picks random number between values"
)
@interactions.slash_option(
    name="high_num",
    description="Upper bound for generator",
    required=True,
    opt_type=interactions.OptionType.INTEGER,
)
@interactions.slash_option(
    name="low_num",
    description="Lower bound for generator, 0 by default",
    opt_type=interactions.OptionType.INTEGER,
)
async def num_gen(ctx: interactions.SlashContext, high_num: int, low_num: int = 0):
    await ctx.send(random.randint(low_num, high_num), silent=True)

@interactions.slash_command(
    name="coinflip",
    description="Flips a coin",
)
async def coin_flip(ctx: interactions.SlashContext):
    coin = random.choice(["Heads", "Tails"])
    await ctx.send(coin, silent=True)

bot.start()
# while True:
#     try:
#         bot.start()
#     except Exception as e:
#         print(e)