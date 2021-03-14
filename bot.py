import discord
import requests
import json
import discord.utils
import random
import string
import asyncio
from discord.ext import commands

Version = 'v1.0.2.7 - Alpha.4'

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")



with open('usercash.json', 'r') as f:
    usercashjson = json.load(f)



def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check
@bot.command()
@commands.cooldown(2, 10, commands.BucketType.user)
async def work(ctx):
    authorid = str(ctx.author.id)
    cashearned = ''.join(random.choice(string.digits) for i in range(3))
    await ctx.send(f"Goodjob, you earned ${cashearned} at work today")
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    usercashjson[authorid] += int(cashearned)
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
    print(authorid)
@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def mine(ctx):
    rustypickaxe = discord.utils.get(ctx.author.guild.roles, name="Rusty Pickaxe")
    steelpickaxe = discord.utils.get(ctx.author.guild.roles, name="Steel Pickaxe")
    goldenpickaxe1 = discord.utils.get(ctx.author.guild.roles, name="Golden Pickaxe")
    magmaritepickaxe = discord.utils.get(ctx.author.guild.roles, name="Magmarite Pickaxe")
    with open('items.json', 'r') as f:
        itemjson = json.load(f)
    with open("mineraldata.json", 'r') as f:
        mineraljson = json.load(f)
    author = str(ctx.author.id)
    if rustypickaxe in ctx.author.roles:
        await ctx.send("You're `Rusty Pickaxe` mined three rubies! ")
        itemjson[author][0]['rubies'] += 3
        with open('items.json', 'w') as f:
            json.dump(itemjson, f, indent=4)
    elif steelpickaxe in ctx.author.roles:
        await ctx.send("You're `Steel Pickaxe` mined six rubies! ")
        itemjson[author][0]['rubies'] += 6
        with open('items.json', 'w') as f:
            json.dump(itemjson, f, indent=4)
    if goldenpickaxe1 in ctx.author.roles:
        randommineral_goldpick = random.choice(['magmarite', "saphire", "alumanite"])
        await ctx.send(f"You're `Golden Pickaxe` mined thirteen rubies and 3 {randommineral_goldpick}")
        mineraljson[author][0][randommineral_goldpick] += 3
        itemjson[author][0]['rubies'] += 13
        with open('items.json', 'w') as f:
            json.dump(itemjson, f, indent=4)
        with open('mineraldata.json', 'w') as f:
            json.dump(mineraljson, f, indent=4)
    if magmaritepickaxe in ctx.author.roles:
        randommineral_magmarpick = random.choice(['magmarite', "saphire", "hellian", "alumanite"])
        await ctx.send(f"You're `Magmarite Pickaxe` mined fifty rubies and six {randommineral_magmarpick}")
        mineraljson[author][0][randommineral_magmarpick] += 6
        itemjson[author][0]['rubies'] += 50
        with open('items.json', 'w') as f:
            json.dump(itemjson, f, indent=4)
        with open('mineraldata.json', 'w') as f:
            json.dump(mineraljson, f, indent=4)
    else:
        await ctx.send("You just mined one ruby! ")
        itemjson[author][0]['rubies'] += 1
        with open('items.json', 'w') as f:
            json.dump(itemjson, f, indent=4)
@mine.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You are missing the `pickaxe` role;  you can buy it in the shop!")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, you're on cooldown!  Chill out before you overwork yourself.")
@work.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, you're on cooldown!  Chill out before you overwork yourself.")
@bot.command()
async def sellrubies(ctx):
    authorid = str(ctx.author.id)
    with open("items.json", 'r') as f:
        itemjson = json.load(f)
    if itemjson[authorid][0]["rubies"] >= 1:
        await ctx.send(f"Sold: {itemjson[authorid][0]['rubies']} Rubies")
        for i in range(itemjson[authorid][0]["rubies"]):
            with open('usercash.json', 'r') as f:
                usercashjson = json.load(f)
            itemjson[authorid][0]["rubies"] -= 1
            usercashjson[authorid] += 250
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
            with open('items.json', 'w') as f:
                json.dump(itemjson, f, indent=4)
    else:
        await ctx.send("You don't have any `rubies` to sell!  Do $mine to collect them!")
@bot.command()
async def bal(ctx):
    authorid = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    embed = discord.Embed(title=f'{ctx.author}\'s Balance', description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name="Balance", value=f"${usercashjson[str(ctx.author.id)][authorid]}")
    await ctx.send(embed=embed)
@bot.command()
async def shop(ctx):
    embed = discord.Embed(title=f"Shop", description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name="pickaxe", value="$5,000", inline=False)
    embed.add_field(name="Gun", value="$5,000", inline=False)
    embed.add_field(name='Weedfarm Business', value="$50,000", inline=False)
    embed.add_field(name="Meth Lab", value="$100,000", inline=False)
    embed.add_field(name="Methlab Trailer", value="$2,500", inline=False)
    embed.add_field(name="King Monke", value="$3,000,000", inline=False)
    await ctx.send(embed=embed)
    await ctx.send("To purchase an item, do $buy(item) all in one word, no capitals.")
@bot.command()
async def buygun(ctx):
    author = str(ctx.author.id)
    global usercash, gun
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if usercashjson[str(ctx.author.id)][str(ctx.author.id)] >= 5000:
        usercashjson[str(ctx.author.id)] -= 5000
        with open('usercash.json', 'r') as f:
            usercashjson = json.load(f)
            with open('items.json', 'r') as f:
                itemsjson = json.load(f)
        itemsjson[author][0]["gun"] += 1
        with open('items.json', 'w') as f:
            json.dump(itemsjson, f, indent=4)
        usercashjson[author] -= 5000
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
        await ctx.send("Purchased `gun`, this will protect you against robbers and attackers!")
        gun += 1
    else:
        await ctx.send("Sorry, you do not have enough money to purchase this item.")
@bot.command()
async def buyweedfarm(ctx):
    global weedfarm
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    authorid = str(ctx.author.id)
    if usercashjson[str(ctx.author.id)][str(ctx.author.id)] >= 50000:
        if itemsjson[authorid][0]["weedfarm"] ==1:
            await ctx.send("Sorry, you already have a weed farm.")
        else:
            with open('usercash.json', 'r') as f:
                usercashjson = json.load(f)
            usercashjson[authorid][str(ctx.author.id)] -= 50000
            itemsjson[authorid][0]["weedfarm"] += 1
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
            with open('items.json', 'w') as f:
                json.dump(itemsjson, f, indent=4)
            await ctx.send("You just purchased your very first `weed farm`  here you can produce weed, do it manually or purchase workers to produce weed for you!")
            embed = discord.Embed(title="Weed Farm Statistics", description=f"**Version: {Version}**", color=0x00ff00)
            embed.add_field(name=f"Worker Statistics", value=f"Worker Amount: NULL")
            embed.add_field(name=f"Cash Per Cycle Statistics", value=f"Producing: ${cpc}")
            await ctx.send(embed=embed)
            await ctx.send("""
```   Commands:
$weedfarmstats - Provides the statistics of your weed farm
$buyweedfarmworker - Purchases a worker for your weed farm
$collectcashweedfarm - Collects the cash from your weed farm
$weedfarm_help
```
""")
    else:
        await ctx.send("Pfft, you need more cash to buy this!  It costs $50000 to open up a weed farm.")
@bot.command()
async def weedfarmstats(ctx):
    global cpc
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    if itemsjson[str(ctx.author.id)][0]["weedfarm"] >= 1:
        embed = discord.Embed(title="Weed Farm Statistics", description=f"**Version: {Version}**", color=0x00ff00)
        embed.add_field(name=f"Worker Statistics", value=f"Worker Amount: NULL")
        embed.add_field(name=f"Cash Per Cycle Statistics", value=f"Producing: ${itemsjson[str(ctx.author.id)][0]['cpc']}")
        await ctx.send(embed=embed)
@bot.command()
async def buyweedfarmworker(ctx):
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if usercashjson[str(ctx.author.id)][str(ctx.author.id)] >= 1000:
        itemsjson[str(ctx.author.id)][0]['cpc'] += 125
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] -= 1000
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
        with open('items.json', 'w') as f:
            json.dump(itemsjson, f, indent=4)
        with open('items.json', 'r') as f:
            itemsjson = json.load(f)
        await ctx.send("Purchased 1 Worker")
        embed = discord.Embed(title="Weed Farm Statistics", description=f"**Version: {Version}**", color=0x00ff00)
        embed.add_field(name=f"Worker Statistics", value=f"Worker Amount: NULL")
        embed.add_field(name=f"Cash Per Cycle Statistics", value=f"Producing: ${itemsjson[str(ctx.author.id)][0]['cpc']}")
        await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def sellweed(ctx):
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    usercashjson[str(ctx.author.id)] += itemsjson[str(ctx.author.id)][0]['cpc']
    await ctx.send(f"Wow Boss, you collected ${itemsjson[str(ctx.author.id)][0]['cpc']} from your weed business!")
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
@sellweed.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, let your weed grow!  Collect cash from your weed farm every 60 seconds!!")
@bot.command()
async def weedfarm_help(ctx):
    await ctx.send("""
```   Commands:
$weedfarmstats - Provides the statistics of your weed farm
$buyweedfarmworker - Purchases a worker for your weed farm
$collectcashweedfarm - Collects the cash from your weed farm
$weedfarm_help
```""")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Command List", description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name="Commands", value="""
    $work - allocates you to work for a set amount of cash twice per minute
    $mine - with a `pickaxe` you can mine rubies which can then be sold for $$$
    $shop - displays the shop
    $updates - displays the update log
    $crime - commits a ***legal*** activity
    $gamble (amount) - Gambles a set amount of cash, 50/50 chance to fill your pockets; or leak them.
    $rob @person - Robs someone, easy cash, easy guap.
    $buy(item) - Purchases an item, no capitals, no spaces.
    $give (amount) @person - Gives cash to whoever you ping!
    $prestige - Shows your current prestige
    $beg - Asks a random person for money
    $inventory - Shows all your current items, (DOES NOT SHOW ORES)
    $sellrubies - Sells your rubies
    $forgerecipes - Shows all the forging Recipes
    $forge (pickaxe name) - Forges a pickaxe
    """)
    embed.set_footer(text=f"Version: {Version}", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    embed1 = discord.Embed(title="Command List Page two", description=f"**Version: {Version}**", color=0x00ff00)
    embed1.add_field(name="Command Page 2", value="""
    $upgradepickaxe - Upgrades your current pickaxe
    $weedfarmstats - Provides the statistics of your `Weed Farm`
    $buyweedfarmworker - Purchases a worker for your `Weed Farm`
    $collectcashweedfarm - Collects the cash from your `Weed Farm`
    $weedfarm_help - Displays all the commands for the `Weed Farm`
    $buymethlab - Purchases a `Methlab`
    $collectmeth - Collects meth from your trailers
    $sellmeth (amount)- Sells all your `Meth baggies`
    $buymethlabtrailer (amount) - Purchases a `Methlab Trailer`
    $methlabstats - Displays the statis of your `Methlab`
    """)
    embed1.set_footer(text=f"Version: {Version}", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed1.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed1)

@bot.command()
async def updates(ctx):
    embed = discord.Embed(title="Update 2.6.1", description=f"**Version: v.{Version}**", color=0x00ff00)
    embed.set_author(name=f"Requested by: {ctx.author.name}",icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"Version: {Version}",
                     icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed.add_field(name="**Added**", value="", inline=False)
    await ctx.send(embed=embed)
@commands.cooldown(6, 60, commands.BucketType.user)
@bot.command()
async def crime(ctx):
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    chances = [1, 2]
    arrestrate = ''.join(random.choice(string.digits)for i in range(2))
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if int(arrestrate) >= 90:
        if itemsjson[str(ctx.author.id)][0]["gun"] >= 1:
            await ctx.send("You decide to bring your 9mm out!  You're in a live shootout with the police!")
            win = random.choice(chances)
            if win == 2:
                await ctx.send("You won!  You shot his leg then bit his ear!  Ran away with $3000")
                usercashjson[ctx.author.id][str(ctx.author.id)] += 3000
                json.dump(usercashjson, f, indent=4)
            else:
                await ctx.send("You lost:(  He shot your ear then bit your leg, those hospital fees gon be expensive, -$5000")
                usercashjson[str(ctx.author.id)][str(ctx.author.id)]  -= 5000
                json.dump(usercashjson, f, indent=4)
        else:
            await ctx.send("**You have been arrested, lost $10000**")
            usercashjson[str(ctx.author.id)][str(ctx.author.id)] -= 10000
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 80:
        await ctx.send("You robbed a casino  Stole $2450!")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] += 2450
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 70:
        await ctx.send("You robbed a train!  Stole $1500")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] += 1500
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 60:
        await ctx.send("You robbed a bar!  Stole $1000")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)]  += 1000
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 50:
        await ctx.send("You robbed your Grandmas house!  Stole  all her rubies!")
        itemsjson[str(ctx.author.id)][0]["rubies"] += 5
        with open('items.json', 'w') as f:
            json.dump(itemsjson, f, indent=4)
    elif int(arrestrate) >= 40:
        await ctx.send("You robbed Jess's house!  Stole her vibra-, $34")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)]  += 34
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 30:
        await ctx.send("You robbed WRLD's!  Stole his Supreme Water Bottle, $100")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)]  += 100
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 20:
        await ctx.send("You robbed WRLD's!  Stole his Supreme Water Bottle, $100")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] += 100
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    elif int(arrestrate) >= 10:
        await ctx.send("You robbed Tristian's trailor!  He had no money:( ")
    elif int(arrestrate) >= 0:
        await ctx.send("You robbed my house?!  You lost $1250!!!")
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] -= 1250
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
@crime.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, buddy, stop stealing, you're on cooldown!")
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def rob(ctx, member: discord.Member):
    robee = member.id
    cashstolen = ''.join(random.choice(string.digits) for i in range(4))
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if int(cashstolen) >= usercashjson[str(robee)][str(robee)]:
        while int(cashstolen) > usercashjson[str(robee)][str(robee)]:
            cashstolen = ''.join(random.choice(string.digits) for i in range(4))
    usercashjson[str(robee)][str(robee)] -= int(cashstolen)
    usercashjson[str(ctx.author.id)][str(ctx.author.id)] += int(cashstolen)
    await ctx.send(f"**You stole ${cashstolen}, stash it in the warehouse Bain!**")
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
@rob.error
async def error_clear(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Stop robbing people!  You're on cooldown for 120 Seconds!!11!")
@bot.command()
async def buymethlab(ctx):
    author = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if usercashjson[author][str(ctx.author.id)] >= 100000:
        with open('items.json', 'r') as f:
            itemsjson = json.load(f)
        if itemsjson[author][0]["methlab"] >= 1:
            await ctx.send("Sorry, you already have a `methlab`!")
        itemsjson[author][0]['methlab'] += 1
        usercashjson[str(ctx.author.id)][str(ctx.author.id)] -= 100000
        await ctx.send("You just purchased your very first methlab!  You can see all the commands with $methlab_help!")
        with open('items.json', 'w') as f:
            json.dump(itemsjson, f, indent=4)
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    else:
        await ctx.send("Sorry!  You need $100000 to purchase the `meth lab`")
@bot.command()
async def buymethlabtrailer(ctx, amounttobuy: int):
    mpc = 0
    author = str(ctx.author.id)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if usercashjson[author][str(ctx.author.id)] >= amounttobuy * 2500:
        if itemsjson[author][0]["methlab"] == 1:
            await ctx.send(f"Purchased: {amounttobuy} Trailer/s")
            for i in range(amounttobuy):
                itemsjson[author][0]["methtrailers"] += 1
                usercashjson[author][str(ctx.author.id)] -= 2500
            embed = discord.Embed(title="Meth Lab Statistics", description=f"**Version: {Version}**", color=discord.Color.green())
            embed.add_field(name=f"Trailer Statistics", value=f"Trailer Amount: {itemsjson[author][0]['methtrailers']}")
            for i in range(itemsjson[author][0]["methtrailers"]):
                mpc += 1
            embed.add_field(name=f"MBs Per Cycle Statistics", value=f"Producing: {mpc} MPC")
            await ctx.send(embed=embed)
            with open('items.json', 'w') as f:
                json.dump(itemsjson, f, indent=4)
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
        else:
           await ctx.send("You don't have a `methlab`, buy one with $buymethlab!")
    else:
        await ctx.send("Sorry!  You do not have enough money to purchase this!  $2500")
@buymethlabtrailer.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, the trailer companies are getting sus of you!  Slowdown!")
@bot.command()
async def methlab_help(ctx):
    await ctx.send("""
```Commands:
$buymethlabtrailer
$buymethlab
$collectmeth
$sellmeth
$methlab_help
$methlabstats
```
""")
@bot.command()
@commands.cooldown(3, 60, commands.BucketType.user)
async def methlabstats(ctx):
    author = str(ctx.author.id)
    mpc = 0
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if itemsjson[author][0]["methlab"]:
        embed = discord.Embed(title="Meth Lab Statistics", description=f"**Version: {Version}**",
                              color=discord.Color.green())
        embed.add_field(name=f"Trailer Statistics", value=f"Trailer Amount: {itemsjson[author][0]['methtrailers']}")
        embed.add_field(name=f"MBs Per Cycle Statistics", value=f"Producing: {itemsjson[author][0]['methtrailers']} MPC")
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not own a `methlab`, buy one with $buymethlab!")
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def collectmeth(ctx):
    author = str(ctx.author.id)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    itemsjson[author][0]["methbags"] += itemsjson[author][0]["methtrailers"]
    with open('items.json', 'w') as f:
        json.dump(itemsjson, f, indent=4)
    await ctx.send(f"Collected: {itemsjson[author][0]['methtrailers']} Methbags")
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
@bot.command()
async def sellmeth(ctx, amounttosell: int):
    sold = 0
    author = str(ctx.author.id)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if itemsjson[author][0]["methlab"]:
        if itemsjson[author][0]["methbags"] >= 1:
            itemsjson[author][0]['methbags'] -= amounttosell
            usercashjson[author][str(ctx.author.id)] += 1000 * amounttosell
            with open('items.json', 'w') as f:
                json.dump(itemsjson, f, indent=4)
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
            await ctx.send(f"Sold: {amounttosell} Methbags for ${amounttosell * 1000}")
        else:
            await ctx.send("You don't have any `methbags`!  Go collect them with $collectmeth")
    else:
        await ctx.send("You do not own a `methlab`, buy one with $buymethlab!")
@sellmeth.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, no way you have ***that*** much meth, you're on cooldown!")
@collectmeth.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, no way you have ***that*** much meth, you're on cooldown!")
@bot.command()
@commands.cooldown(1, 20)
async def beg(ctx):
    author = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    begcash = ''.join(random.choice(string.digits) for i in range(3))
    usercashjson[author][str(ctx.author.id)] += int(begcash)
    await ctx.send(f"Fineee :rolling_eyes:, ig ill give u cash ${begcash}")
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
@beg.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa poor begger, you're on cooldown! ")
@commands.cooldown(2, 60)
@bot.command()
async def scam(ctx, member: discord.Member):
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    options = ["rubies", "methbags"]
    chosenoption = random.choice(options)
    amountstolen = random.choice(string.digits)
    while int(amountstolen) > itemsjson[str(member.id)][0]["rubies"]:
        amountstolen = random.choice(string.digits)
    if int(amountstolen) == 0:
        amountstolen = 1
    itemsjson[str(member.id)][0][chosenoption] -= int(amountstolen)
    itemsjson[str(ctx.author.id)][0][chosenoption] += int(amountstolen)
    await ctx.send(f'You stole {amountstolen} {chosenoption} from {member.name}')
    with open('items.json', 'w') as f:
        json.dump(itemsjson, f, indent=4)
@scam.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa, you're on cooldown!  Please stop scamming for a bit")
@bot.command()
async def gamble(ctx):
    author = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    betamount = int(ctx.message.content[8:])
    if usercashjson[author][str(ctx.author.id)] < betamount:
        await ctx.send("Sorry!  You don't have that much cash!  *bum*")
    else:
        chance = random.choice([1, 2])
        if chance == 2:
            await ctx.send("Generating chance. . .")
            await asyncio.sleep(1)
            usercashjson[author][str(ctx.author.id)] += betamount
            await ctx.send("You won!  Nice on ya lad!")
        else:
            await ctx.send("Generating chance. . .")
            await asyncio.sleep(1)
            usercashjson[author][str(ctx.author.id)] -= betamount
            await ctx.send("You lost!  Wanna rob the Casino and get your money back?  Do $heist casino!")
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
@bot.command()
async def upgradepickaxe(ctx):
    rustypickaxe = discord.utils.get(ctx.author.guild.roles, name="Rusty Pickaxe")
    steelpickaxe = discord.utils.get(ctx.author.guild.roles, name="Steel Pickaxe")
    goldenpickaxe = discord.utils.get(ctx.author.guild.roles, name="Golden Pickaxe")
    txt = discord.utils.get(ctx.author.guild.channels, name='general')
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    author = str(ctx.author.id)
    if rustypickaxe in ctx.author.roles:
        if usercashjson[author][str(ctx.author.id)] >= 15000:
            await ctx.author.add_roles(steelpickaxe)
            await ctx.author.remove_roles(rustypickaxe)
            await ctx.send("Upgraded pickaxe to `Steel Pickaxe`!")
            usercashjson[author][str(ctx.author.id)] -= 15000
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
    if steelpickaxe in ctx.author.roles:
        if usercashjson[author][str(ctx.author.id)] >= 17500:
            await ctx.author.add_roles(goldenpickaxe)
            await ctx.author.remove_roles(steelpickaxe)
            await ctx.send("Upgraded pickaxe to `Golden Pickaxe`!")
            usercashjson[author][str(ctx.author.id)] -= 17500
            with open('usercash.json', 'w') as f:
                json.dump(usercashjson, f, indent=4)
            await ctx.send("Too upgrade your tools from here, you need to collect minerals only obtainable through mining, crafting recipes will be available if you do $forgelist.")
@bot.command()
async def forgerecipes(ctx):
    pickaxerecips = """
Magmarite Pickaxe - 15 Magmarite, 9 Sapphire
Hellian Pickaxe - 16 Magmarite, 13 Sapphire, 4 Hellian
    """
    embed = discord.Embed(title="Forging Recipes", description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name=f"Pickaxe Recipes", value=f"{pickaxerecips}")
    embed.set_footer(text=f"Version: {Version}",
                     icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
@bot.command()
async def give(ctx, amounttogive: int, member: discord.Member):
    author = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    if usercashjson[author][str(ctx.author.id)] >= amounttogive:
        usercashjson[author][str(ctx.author.id)] -= amounttogive
        usercashjson[str(member.id)][str(ctx.author.id)] += amounttogive
        embed = discord.Embed(title="Give Cash", description=f"**Version: {Version}**", color=0x00ff00)
        embed.add_field(name=f"Cash Given", value=f"${amounttogive}")
        embed.set_footer(text=f"Version: {Version}",
                         icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
        embed.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('usercash.json', 'w') as f:
            json.dump(usercashjson, f, indent=4)
    else:
        ctx.send("You don't have enough cash to send to them!")
@bot.command()
async def forge(ctx, pickaxe: str):
    print(pickaxe)
    if pickaxe == "magmaritepickaxe":
        author = str(ctx.author.id)
        with open("mineraldata.json", 'r') as f:
            mineralsjson = json.load(f)
        if mineralsjson[author][0]["magmarite"] >= 15:
            if mineralsjson[author][0]["saphire"] >= 9:
                goldenpickaxe = discord.utils.get(ctx.author.guild.roles, name="Golden Pickaxe")
                if goldenpickaxe in ctx.author.roles:
                    await ctx.send("You forged a `Magmarite Pickaxe`!")
                    role = discord.utils.get(ctx.author.guild.roles, name="Magmarite Pickaxe")
                    await ctx.author.add_roles(role)
                    mineralsjson[author][0]["magmarite"] -= 15
                    mineralsjson[author][0]["saphire"] -= 9
                    await ctx.author.remove_roles(goldenpickaxe)
                    with open('mineraldata.json', 'w') as f:
                        json.dump(mineralsjson, f, indent=4)
                else:
                    await ctx.send("You need a `Golden Pickaxe` to forge the `Magmarite Pickaxe`!")
            else:
                await ctx.send("You don't have enough `Sapphire!`, do $mine with a Pickaxe to collect some!")
        else:
            await ctx.send("You don't have enough `Magmarite!`, do $mine with a Pickaxe to collect some!")
    if pickaxe == "hellianpickaxe":
        author = str(ctx.author.id)
        with open("mineraldata.json", 'r') as f:
            mineralsjson = json.load(f)
        if mineralsjson[author][0]["magmarite"] >= 16:
            if mineralsjson[author][0]["saphire"] >= 13:
                if mineralsjson[author][0]["hellian"] >= 4:
                    magmarpick = discord.utils.get(ctx.author.guild.roles, name="Magmarite Pickaxe")
                    if magmarpick in ctx.author.roles:
                        await ctx.send("You forged a `Hellian Pickaxe`!")
                        role = discord.utils.get(ctx.author.guild.roles, name="Hellian Pickaxe")
                        await ctx.author.add_roles(role)
                        mineralsjson[author][0]["magmarite"] -= 16
                        mineralsjson[author][0]["saphire"] -= 13
                        mineralsjson[author][0]['hellian'] -= 4
                        await ctx.author.remove_roles(magmarpick)
                        with open('mineraldata.json', 'w') as f:
                            json.dump(mineralsjson, f, indent=4)
                    else:
                        await ctx.send("You need a `Magmarite Pickaxe` to forge the `Hellian Pickaxe`!")
                else:
                    await ctx.send("You don't have enough `Hellian!`, do $mine with a Pickaxe to collect some!")
            else:
                await ctx.send("You don't have enough `Sapphire!`, do $mine with a Pickaxe to collect some!")
        else:
            await ctx.send("You don't have enough `Magmarite!`, do $mine with a Pickaxe to collect some!")
@bot.command()
async def buykingmonke(ctx):
    author = str(ctx.author.id)
    with open('usercash.json', 'r') as f:
        usercashjson = json.load(f)
    role = discord.utils.get(ctx.author.guild.roles, name="👑King Monk👑")
    if usercashjson[author][str(ctx.author.id)] >= 3000000:
        await ctx.author.add_roles(role)
    else:
        await ctx.send("You cannot afford King Monke")
@bot.command()
async def bananaphone(ctx):
    role = discord.utils.get(ctx.author.guild.roles, name="👑King Monk👑")
    if role in ctx.author.roles:
        for i in range(100):
            await ctx.send(":banana:")
def verifycheck(message):
    global captcha
    if message.content != captcha:
        return TypeError
    return message.content == captcha
@bot.command()
async def verify(ctx):
    global captcha
    captcha = ''.join(random.choice(string.ascii_letters) for i in range(6))
    role = discord.utils.get(ctx.author.guild.roles, name='verified')
    embed = discord.Embed(title="Captcha Verification", description="*Please complete this captcha to get access to the server*", color=discord.Color.purple())
    embed.add_field(name="Captcha Provided", value=f"{captcha}")
    await ctx.send(embed=embed)
    try:
        await bot.wait_for('message', check=verifycheck, timeout=5)
        if TypeError:
            await ctx.send('failed')
    except asyncio.TimeoutError:
        await ctx.send("**The verification token has expired!  Please send $verify to start a new one.**")
    else:
        await ctx.author.add_roles(role)
@bot.command()
async def inventory(ctx):
    author = str(ctx.author.id)
    with open('items.json', 'r') as f:
        itemsjson = json.load(f)
    embed = discord.Embed(title="Prestige", description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name="Inventory Items ", value=f"""
Rubies: {itemsjson[author][0]["rubies"]}
Weed Farms: {itemsjson[author][0]["weedfarm"]}
Meth Labs: {itemsjson[author][0]["methlab"]}
Meth baggies: {itemsjson[author][0]["methbags"]}
Meth Trailers: {itemsjson[author][0]["methtrailers"]}
""")
    embed.set_footer(text=f"Version: {Version}", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
@bot.command()
async def prestige(ctx):
    with open("presteige.json", 'r') as f:
        prestigejson = json.load(f)
    embed = discord.Embed(title="Prestige", description=f"**Version: {Version}**", color=0x00ff00)
    embed.add_field(name="Prestige", value=f"{prestigejson[str(ctx.author.id)]}")
    embed.set_footer(text=f"Version: {Version}", icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    embed.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
@bot.command()
async def start(ctx):
    with open("mineraldata.json", 'r') as f:
        mineraljson = json.load(f)
    with open("usercash.json", 'r') as f:
        usercashjson = json.load(f)
    mineraljson[str(ctx.author.id)] = [
        {
            "saphire": 0,
            "magmarite": 0,
            "alumanite": 0,
            "hellian": 0,
            "ECOi": 0,
            "fishre": 0
        }
    ]
    author = str(ctx.author.id)
    usercashjson[author] = {author: 0}
    with open('mineraldata.json', 'w') as f:
        json.dump(mineraljson, f, indent=4)
    with open('usercash.json', 'w') as f:
        json.dump(usercashjson, f, indent=4)
bot.run('ODE5ODA3NDUzMDAzNjQ0OTM4.YEr_MA.LUkEjizVbf8e1TSRDBZ2OTdcJLo')
