# Importing required dependencies
import discord as dc
import nest_asyncio
from lib.crawler import SXCPCCrawler
from discord.ext import commands as cmd

crawler = SXCPCCrawler()  # Crawler object
client = cmd.Bot(command_prefix='?')  # Discord object

client.remove_command('help')
color = 0x8785ff

nest_asyncio.apply()

# Change the status of the bot
@client.event
async def on_ready():
    await client.change_presence(activity=dc.Activity(
        type=dc.ActivityType.watching,
        name='Over SXC Placement Cell Blog! | Start By: ?help'))


# Help command
@client.command()
async def help(ctx):
    embed = dc.Embed(
        title="** Usage **",
        description=
        "There are only a few easy commands to get started with this bot. ",
        color=color)
   
    embed.add_field(name="?help", value="Displays help", inline=False)
    embed.add_field(name="?info",
                    value="Displays bot information",
                    inline=False)
    embed.add_field(name="?jobs",
                    value="Displays latest 10 job post.",
                    inline=False)
    embed.add_field(name="?jobs [m]",
                    value="Displays latest 'm' job post.",
                    inline=False)

    embed.add_field(name="?jobs t [yyyy]",
                    value="Displays latest 10 job post of the provided year",
                    inline=False)
    embed.add_field(
        name="?jobs t [yyyy] [mm]",
        value="Displays latest 10 job post of the provided year and month",
        inline=False)
    embed.add_field(name="?jobs [m] t [yyyy]",
                    value="Displays latest 'm' job post of the provided year",
                    inline=False)
    embed.add_field(
        name="?jobs [m] t [yyyy] [mm]",
        value="Displays latest 'm' job post of the provided year and month",
        inline=False)
    await ctx.send(embed=embed)


# Info command
@client.command()
async def info(ctx):
    # Display bot info
    embed = dc.Embed(
        title="** SXCCampusing **",
        url="https://sxcpc.blogspot.com",
        description=
        "A simple bot to display latest job posts from St.Xavier's College Placement Cell blog after scraping blog posts.",
        color=color)
    embed.set_author(
        name="thenocturnalguy",
        url="https://thenocturnalguy.epizy.com",
        icon_url=
        "https://warehouse-camo.ingress.cmh1.psfhosted.org/7428b206ebaa1b570184332da79d1c6eefad611b/68747470733a2f2f7365637572652e67726176617461722e636f6d2f6176617461722f65616434376531366638643232393635326463356530323839633061316132333f73697a653d323235"
    )
    embed.set_thumbnail(
        url=
        "https://previews.123rf.com/images/putracetol/putracetol1805/putracetol180507019/101888941-job-search-logo-icon-design.jpg"
    )
    embed.add_field(name="@created_at", value="23.03.2021", inline=True)
    embed.add_field(name="@updated_at", value="26.03.2021", inline=True)
    embed.add_field(name="@version", value="v3.0.0", inline=True)
    embed.add_field(
        name="@github",
        value="https://github.com/thenocturnalguy/sxccampusing-discord-bot",
        inline=True)
    embed.set_footer(text="Thank you! Keep applying for jobs. Best of luck :)")
    await ctx.send(embed=embed)


# Job posts listing command
@client.command()
async def jobs(ctx, *, argsstr=''):
    args = argsstr.strip().split()
    argc = len(args)

    if (argc == 0):

        # Only 1 option - just print latest 10 job post name
        # cmd: ?jobs

        postlist = crawler.crawl_archive()
        count = min(10, len(postlist))

        embed = dc.Embed(title=f'***Latest {count} Job Post Results:***',
                         color=color)
        for post in postlist[:count]:
            embed.add_field(
                name='\u200b',
                value=f'> ** {post[1]} **\n > ** [Go to Post]({post[0]}) **',
                inline=True)

        await ctx.send(embed=embed)

    elif (argc == 1):

        # Only 1 option - just print latest 'm' job post name
        # where m is the 2nd argument supplied
        # cmd: ?jobs 15

        if (args[0].isnumeric()):
            postlist = crawler.crawl_archive()
            count = min(int(args[0]), len(postlist))
            embed = dc.Embed(title=f'***Latest {count} Job Post Results:***',
                             color=color)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} **\n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await ctx.send(embed=embed)
        else:
            ctx.send('Wrong count provided!')

    elif (argc == 2 and args[0] == 't'):

        # cmd: ?jobs t 2020

        yr = args[1]
        if (yr.isnumeric()):
            postlist = crawler.crawl_archive(yr + '/')
            count = min(10, len(postlist))
            embed = dc.Embed(
                title=f'***Latest {count} Job Post Results of {yr}:***',
                color=color)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} ** \n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Wrong year provided!')

    elif (argc == 3 and args[0] == 't'):

        # cmd: ?jobs t 2020 09

        yr = args[1]
        mn = args[2]

        if (yr.isnumeric() and mn.isnumeric()):
            postlist = crawler.crawl_archive(yr + '/', mn + '/')
            count = min(10, len(postlist))
            embed = dc.Embed(
                title=f'***Latest {count} Job Post Results of {mn}/{yr}:***',
                color=color)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} ** \n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Wrong year or month provided!')

    elif (argc == 3 and args[1] == 't'):

        # cmd: ?jobs 15 t 2020

        count = args[0]
        yr = args[2]

        if (not (count.isnumeric())):
            await ctx.send('Wrong count provided!')
        elif (not (yr.isnumeric())):
            await ctx.send('Wrong year provided!')
        else:
            postlist = crawler.crawl_archive(yr + '/')
            count = min(int(count), len(postlist))
            embed = dc.Embed(
                title=f'***Latest {count} Job Post Results of {yr}:***',
                color=color)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} ** \n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await ctx.send(embed=embed)

    elif (argc == 4 and args[1] == 't'):

        # cmd: ?jobs 15 t 2020 09

        count = args[0]
        yr = args[2]
        mn = args[3]

        if (not (count.isnumeric())):
            await ctx.send('Wrong count provided!')
        elif (not (yr.isnumeric())):
            await ctx.send('Wrong year format provided!')
        elif (not (yr.isnumeric())):
            await ctx.send('Wrong month format provided!')
        else:
            postlist = crawler.crawl_archive(yr + '/', mn + '/')
            count = min(int(count), len(postlist))
            embed = dc.Embed(
                title=f'***Latest {count} Job Post Results of {mn}/{yr}:***',
                color=color)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} ** \n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await ctx.send(embed=embed)

    else:
        await ctx.send('Wrong arguments provided!')
