# Importing required dependencies
from bs4 import BeautifulSoup as soup
import requests as req
import discord as dc
import os
import nest_asyncio


# Crawler class for getting the job data
class SXCPCCrawler:

    base_url = ''  # Base url of the site to be crawled

    # Constructor to initialize with the default values
    def __init__(self):
        self.base_url = 'https://sxcpc.blogspot.com/'

    # Function to get the page content and convert it into
    # BeautifulSoup object to be parsed later
    def _getPageContent(self, year='', month=''):

        url = self.base_url + year + month  # Crafting the url

        response = req.get(url)
        page_html = soup(response.text, 'lxml')

        return page_html

    # Method to extract the required info
    def crawl(self, year='', month=''):

        page_html = self._getPageContent(year, month)

        archive = [(item['href'], item.text)
                   for item in page_html.body.find('div', {
                       'id': 'ArchiveList'
                   }).find('ul', {
                       'class': 'posts'
                   }).findAll('a')]

        return archive


crawler = SXCPCCrawler()  # Crawler object
client = dc.Client()  # Discord object

nest_asyncio.apply()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    args = msg.strip().split()
    argc = len(args)

    if msg.startswith('?sxcpc'):
        if argc == 1:
            # Only 1 option - just print latest 10 job post name

            postlist = crawler.crawl()
            count = min(10, len(postlist))

            embed = dc.Embed(title=f'__**Latest {count} Job Post Results:**__',
                             color=0x03f8fc)
            for post in postlist[:count]:
                embed.add_field(
                    name='\u200b',
                    value=
                    f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                    inline=True)
            await message.channel.send(embed=embed)
        elif argc == 2:
            # Only 1 option - just print latest 'm' job post name
            # where m is the 2nd argument supplied

            if (args[1].isnumeric()):
                postlist = crawler.crawl()
                count = min(int(args[1]), len(postlist))
                embed = dc.Embed(
                    title=f'__**Latest {count} Job Post Results:**__',
                    color=0x03f8fc)
                for post in postlist[:count]:
                    embed.add_field(
                        name='\u200b',
                        value=
                        f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                        inline=True)
                await message.channel.send(embed=embed)
            elif (args[1] == 'h'):
                # Display help
                embed = dc.Embed(title=f'__**Usage:**__', color=0x03f8fc)
                embed.add_field(
                    name='\u200b',
                    value='> **?sxcpc**: Displays latest 10 job post.',
                    inline=False)
                embed.add_field(
                    name='\u200b',
                    value='> **?sxcpc [m]**: Displays latest \'m\' job post.',
                    inline=False)
                embed.add_field(name='\u200b',
                                value='> **?sxcpc h**: Displays help.',
                                inline=False)
                embed.add_field(
                    name='\u200b',
                    value='> **?sxcpc i**: Displays bot information.',
                    inline=False)
                embed.add_field(
                    name='\u200b',
                    value=
                    '> **?sxcpc t [yyyy]**: Displays latest 10 job post of the provided year.',
                    inline=False)
                embed.add_field(
                    name='\u200b',
                    value=
                    '> **?sxcpc t [yyyy] [mm]**: Displays latest 10 job post of the provided year and month.',
                    inline=False)
                embed.add_field(
                    name='\u200b',
                    value=
                    '> **?sxcpc [m] t [yyyy]**: Displays latest \'m\' job post of the provided year.',
                    inline=False)
                embed.add_field(
                    name='\u200b',
                    value=
                    '> **?sxcpc [m] t [yyyy] [mm]**: Displays latest \'m\' job post of the provided year and month.',
                    inline=False)
                await message.channel.send(embed=embed)
            elif (args[1] == 'i'):
                # Display bot info
                embed = dc.Embed(title=f'__**Bot Info:**__', color=0x03f8fc)
                embed.add_field(
                    name='\u200b',
                    value=
                    '> **@developer**: thenocturnalguy\n> **@description**: A discord bot to display latest job post on https://sxcpc.blogspot.com\n> **@version**: v1.0.3\n> **@updated_at**: 24.03.2021'
                )

                await message.channel.send(embed=embed)
            else:
                await message.channel.send('Wrong count provided!')

        elif argc > 2:
            # 4 options

            if (args[1] == 't'):
                if (argc == 3):
                    yr = args[2]
                    if (yr.isnumeric()):
                        postlist = crawler.crawl(yr + '/')
                        count = min(10, len(postlist))
                        embed = dc.Embed(
                            title=
                            f'__**Latest {count} Job Post Results of {yr}:**__',
                            color=0x03f8fc)
                        for post in postlist[:count]:
                            embed.add_field(
                                name='\u200b',
                                value=
                                f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                                inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send('Wrong year provided!')
                elif (argc == 4):
                    yr = args[2]
                    mn = args[3]

                    if (yr.isnumeric() and mn.isnumeric()):
                        postlist = crawler.crawl(yr + '/', mn + '/')
                        count = min(10, len(postlist))
                        embed = dc.Embed(
                            title=
                            f'__**Latest {count} Job Post Results of {mn}/{yr}:**__',
                            color=0x03f8fc)
                        for post in postlist[:count]:
                            embed.add_field(
                                name='\u200b',
                                value=
                                f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                                inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(
                            'Wrong year or month provided!')
                else:
                    await message.channel.send('Wrong arguments provided!')
            elif (args[2] == 't'):
                count = args[1]
                if (count.isnumeric()):

                    if (argc == 4):
                        yr = args[3]
                        if (yr.isnumeric()):
                            postlist = crawler.crawl(yr + '/')
                            count = min(int(count), len(postlist))
                            embed = dc.Embed(
                                title=
                                f'__**Latest {count} Job Post Results of {yr}:**__',
                                color=0x03f8fc)
                            for post in postlist[:count]:
                                embed.add_field(
                                    name='\u200b',
                                    value=
                                    f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                                    inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send('Wrong year provided!')
                    elif (argc == 5):
                        yr = args[3]
                        mn = args[4]

                        if (yr.isnumeric() and mn.isnumeric()):
                            postlist = crawler.crawl(yr + '/', mn + '/')
                            count = min(int(count), len(postlist))
                            embed = dc.Embed(
                                title=
                                f'__**Latest {count} Job Post Results of {mn}/{yr}:**__',
                                color=0x03f8fc)
                            for post in postlist[:count]:
                                embed.add_field(
                                    name='\u200b',
                                    value=
                                    f'> ** {post[1]} ** \t\t\t \n > ** [Go to Post]({post[0]}) **',
                                    inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(
                                'Wrong year or month provided!')
                    else:
                        await message.channel.send('Wrong arguments provided!')
                else:
                    await message.channel.send('Wrong count provided!')
            else:
                await message.channel.send('Wrong arguments provided!')
        else:
            await message.channel.send('Wrong arguments provided!')


# Go live!
client.run('ODIzOTQ3MDg5MjIxMzg2MjQw.YFoOhg.XZGf8gpTpn8HgfYuQIbJizTWOjU')
