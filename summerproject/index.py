import asyncio
import discord
from discord.channel import VoiceChannel
from discord.ext import commands
import random
import json
import os
import youtube_dl
import ffmpeg
import translate
from translate import Translator
from discord.ext.commands.converter import RoleConverter, _get_from_guilds
from discord.gateway import DiscordClientWebSocketResponse



os.chdir("C:\\Users\\unibl\\OneDrive\\Desktop\\summerproject")

shop = [{"name":"deathnote", "price": 100000,"description":"Forged by a Shinigami"},
        {"name": "manga", "price": 400, "description": "Part of a manga set"},
        {"name": "vandal", "price": 2900, "description": "Vandal from valorant"},]

if os.path.exists(os.getcwd() +"/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {'Token': "", "Prefix": "k."}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

class Music(commands.Cog):
    def __init__(self, client):
        self.bot = client

help_command = commands.DefaultHelpCommand(
    no_category = "Kasumi's commands"
)


client = commands.Bot(command_prefix = 'k.', help_command = help_command, intents= discord.Intents.all())


@client.event
async def on_member_join(member):
    embed = discord.Embed(title = f'Welcome to {member.guild.name}!')
    embed.colour = discord.Colour.orange()
    embed.description = f'Welcome {member.mention} to {member.guild.name} hope you enjoy your stay and remember to follow the rules :heart:'
    await member.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Still on cooldown**, please try again in {:.2f}s :alarm_clock:'.format(error.retry_after)
        await ctx.send(msg)
    
@client.event
async def on_ready():
    print('hey master')
    await client.load_extension('music')
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"on {len(client.guilds)} servers | k.help"))

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass
    
    else:
        
        with open('reactrole.json')as react_file:
            
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

        
        with open('reactrole.json')as react_file:
            
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command(aliases = ['trans'])
async def translate(ctx, lang, *, text):
    # create translator object and translate the text
    translator = Translator(to_lang=lang)
    translation = translator.translate(text)
    
    # create embed and send translated text
    embed = discord.Embed(
        title=f"Translated to {lang}",
        description=translation,
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    
@client.command()
async def owner(ctx):
    await ctx.send('my owner is the lovely Milo.#3281')

@client.command()
async def searchghosthunters(ctx):
    await ctx.send("<@1080682019161387048>" + ctx.author.mention + " requests to play phas anyone care to join")

@client.command()
@commands.has_guild_permissions(administrator=True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("you need to type the channels name after the command")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        channel_position = channel.position 
        await ctx.send("A tactical nuke is dropping in 10 seconds evacuate to the nearest bunker :radioactive:")
        await asyncio.sleep(10)
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        await channel.edit(position=channel_position, sync_permissions=True)
        await new_channel.send(ctx.message.author.name + " has decided to drop a tactical nuke on this chat cleaning it of all its messages")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")

@client.command(aliases = ['inv', 'bag'])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    emb = discord.Embed(title = "inventory", color = discord.Color.orange())
    for item in bag:
        name = item["item"]
        amount = item ['amount']
    
        emb.add_field(name = name,value = amount)
    await ctx.send(embed=emb)

@client.command()
async def store(ctx):
    em = discord.Embed(title = "Store:", color = discord.Color.orange())

    for item in shop:
        name = item["name"]
        price = item["price"]
        desc= item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)

@client.command()
async def dice(ctx):
    number = [" 1 ",
              " 2 ",
              " 3 ",
              " 4 ",
              " 5 ",
              " 6 "]
    em = discord.Embed(title = f"Your dice rolls a {random.choice(number)}", color = discord.Color.orange())
    await ctx.send(embed=em)



@client.command(aliases= ['ohayo', 'gm'])
async def goodmorning(ctx):
    await ctx.send('Good morning <3')
    
@client.command(aliases=['hi', 'hello', 'hey'])
async def _hey(ctx):
    responses = ['Hey whats up!',
                 'Yeah what is it?',
                 'Oh hey I hope you are having a good day!',
                 'Dō shita no!',]

    await ctx.send(random.choice(responses))

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                  'Without a doubt',
                  'Yes - Forsure',
                  'Most likely',
                  'yes',
                  'signs point towards yes',
                  'replay hazy, try again',
                  'ask again later please <3',
                  'I cant ruin the surprise :face_with_hand_over_mouth:',
                  'I cant say that I know sorry',
                  'Dont count on it happening',
                  'how about no',
                  'from my experiences no',
                  'the pointer is pointing towards no',  
                  'Nah chief aint happening',]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')\


@client.command(aliases=['rr'])
@commands.has_guild_permissions(manage_roles=True)
async def reactionrole(ctx, emoji, role: discord.Role,*,message):
    
    emb = discord.Embed(description=message)  
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {
            'role_name' :role.name,
            'role_id' :role.id,
            'emoji' :emoji,
            'message_id' :msg.id
        }
        data.append(new_react_role)

    
    with open('reactrole.json','w')as j:
        json.dump(data,j,indent=4)

@client.command()
#add more to hugs list later
async def hug(ctx, user1: discord.Member):
    if user1 == ctx.message.author:
        await ctx.channel.send(ctx.message.author.mention + 'do you need a hug :pleading_face:')
        return
        
    else:
                hugs = ['https://cdn.weeb.sh/images/rJaog0FtZ.gif',
                  'https://cdn.weeb.sh/images/BJoC__XvZ.gif',
                  'https://cdn.weeb.sh/images/BkBs2uk_b.gif',
                  'https://cdn.weeb.sh/images/S1gUsu_Qw-.gif',
                  'https://cdn.weeb.sh/images/S1gUsu_Qw-.gif',
                  'https://cdn.weeb.sh/images/Sk2gmRZZG.gif',
                  'https://cdn.weeb.sh/images/r1G3xCFYZ.gif',
                  'https://cdn.weeb.sh/images/Bk5haAocG.gif',
                  'https://cdn.weeb.sh/images/HJTWcTNCZ.gif',
                  'https://cdn.weeb.sh/images/ryPix0Ft-.gif',
                  'https://cdn.weeb.sh/images/BkuUhO1OW.gif',
                  'https://cdn.weeb.sh/images/rkN2u_XP-.gif',
                  'https://cdn.weeb.sh/images/Hy0KO_7DZ.gif',
                  'https://cdn.weeb.sh/images/HkRwnuyuW.gif',  
                  'https://cdn.weeb.sh/images/ByPGRkFVz.gif',]
                url = random.choice(hugs)
                embed=discord.Embed(title = ctx.message.author.name + " sends hugs to " + user1.name + " awwwwwwww :heart:!!! ", color = discord.Color.dark_red())
                embed.set_image(url = random.choice(hugs))
                
                await ctx.channel.send(embed=embed)
@client.command()
#add more to hugs list later
async def slap(ctx, user1: discord.Member):
    if user1 == ctx.message.author:
        await ctx.channel.send(ctx.message.author.mention + 'dont hit yourself stupid :broken_heart:')
        return
        
    else:
                slaps = ['https://media.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif',
                        'https://media.tenor.com/yJmrNruFNtEAAAAM/slap.gif',
                        'https://media.tenor.com/FJsjk_9b_XgAAAAM/anime-hit.gif',
                        'https://media.tenor.com/XiYuU9h44-AAAAAM/anime-slap-mad.gif',
                        'https://media.tenor.com/5eI0koENMAAAAAAM/anime-hit.gif',
                        'https://media.tenor.com/klNTzZNDmEgAAAAM/slap-hit.gif',
                        'https://media.tenor.com/8f8ciLp9_T0AAAAM/anime-slap.gif',
                        'https://media.tenor.com/aP7Du3RWX6YAAAAM/slap-anime.gif',
                        'https://media.tenor.com/bW9sL6u6V7AAAAAM/fly-away-slap.gif',
                        'https://media.tenor.com/8SoReGELlnAAAAAM/anime-girl-slap.gif',
                        'https://media.tenor.com/VTM2thD8QBsAAAAM/anime-mad.gif',
                        

                  ]
                url = random.choice(slaps)
                embed=discord.Embed(title = ctx.message.author.name + " slapped " + user1.name + " HEADSHOT ")
                embed.set_image(url = random.choice(slaps))
                
                await ctx.channel.send(embed=embed)


@client.command()
async def kill(ctx, user1: discord.Member):
    if user1 == ctx.message.author:
        await ctx.channel.send(ctx.message.author.mention + 'dont do it please :broken_heart:')
        return
        
    else:
        #make more kill gifs
                kills = ['https://media1.tenor.com/images/a80b2bf31635899ac0900ea6281a41f6/tenor.gif?itemid=5535365',
                         'https://media1.tenor.com/images/bb4b7a7559c709ffa26c5301150e07e4/tenor.gif?itemid=9955653',
                         'https://media1.tenor.com/images/eb7fc71c616347e556ab2b4c813700d1/tenor.gif?itemid=5840101',
                         'https://media1.tenor.com/images/9395ec23c0503169a4f6a15d7a03d002/tenor.gif?itemid=21280823',
                         'https://media.tenor.com/images/02ef4da0bd033a4e024d1916a1542a5a/tenor.gif',
                         'https://media.tenor.com/images/16623d39acb89d455a5c6e4efec8da8f/tenor.gif',
                         'https://media1.tenor.com/images/b09175c956f2ac8020fc08de2deca21a/tenor.gif?itemid=17870589',
                         'https://media1.tenor.com/images/560c804176fd19aa9bb8a4d32f1a3041/tenor.gif?itemid=17608722',
                         'https://media.tenor.com/images/47698b115e4185036e95111f81baab45/tenor.gif',
                         'https://media.tenor.com/images/3f9e6d5315b421c11cff659cd4a7a25e/tenor.gif',
                         'https://media.tenor.com/images/b09b36ae92b2b5c6da7212472514063d/tenor.gif',
                         'https://media1.tenor.com/images/b221fb3f50f0e15b3ace6a2b87ad0ffa/tenor.gif?itemid=8576304',
                         ]
                url = random.choice(kills)
                embed=discord.Embed(title = ctx.message.author.name + " insta kills " + user1.name + " what a blow :right_facing_fist: ", color = discord.Color.orange())
                embed.set_image(url = random.choice(kills))
                
                await ctx.channel.send(embed=embed)


@client.command()
async def freevbucks(ctx):
    await ctx.channel.send('the virus.... i mean vbucks have been added to your computer')

@client.command()
#add more to kisses list
async def kiss(ctx, user1: discord.Member):
    if user1 == ctx.message.author:
        await ctx.channel.send(ctx.message.author.mention + 'im sorry you cant do that... im sure someone else will though <3')
        return
        
    else:
                kisses = ['https://cdn.weeb.sh/images/ry-r3TuD-.gif',
                  'https://cdn.weeb.sh/images/SJSr3TOv-.gif',
                  'https://cdn.weeb.sh/images/H1Gx2aOvb.gif',
                  'https://cdn.weeb.sh/images/rkde2aODb.gif',
                  'https://cdn.weeb.sh/images/r1VWnTuPW.gif',
                  'https://cdn.weeb.sh/images/Bkuk26uvb.gif',
                  'https://cdn.weeb.sh/images/ByVQha_w-.gif',
                  'https://cdn.weeb.sh/images/Sy6Ai6ODb.gif',
                  'https://cdn.weeb.sh/images/ByTBhp_vZ.gif',
                  'https://cdn.weeb.sh/images/SJINn6OPW.gif',
                  'https://cdn.weeb.sh/images/ryoW3T_vW.gif',
                  'https://cdn.weeb.sh/images/rJ6PWohA-.gif',
                  'https://cdn.weeb.sh/images/SydfnauPb.gif',
                  'https://cdn.weeb.sh/images/BJv0o6uDZ.gif',  
                  'https://cdn.weeb.sh/images/BJMX2TuPb.gif',]
                url = random.choice(kisses)
                embed=discord.Embed(title = ctx.message.author.name + " kisses " + user1.name + " things are heating up in here :smirk:")
                embed.set_image(url = random.choice(kisses))

                await ctx.channel.send(embed=embed)

@client.command()
async def randomanime(ctx):
    #add more animes
    animes = ['Deca-Dance',
              'Violet Evergarden',
              'Fate series',
              'Wolf Children',
              'Slam dunk',
              'Bakuman',
              'Love is war',
              'Soul eater/Soul eater not',
              'Blue exorcist',
              'welcome to the nhk',
              'love live superstar',
              'Dr stone',
              'After school dice club'
              'K-on',
              'Date a live',
              '.hack series',
              'Mob psycho 100',
              'Neon Genesis Evangelion',
              'Future diary',
              "Wise man's granchild",
              'Full metal alchemist',
              'Arms alchemy',
              'Scorching ping pong girls',
              'The Asterik War',
              'Maquia: When the promised flower blooms',
              'konosuba',
              'Nana',
              'New game',
              'Engaged to the unidentified',
              'Witch hunter robin']
    emb = discord.Embed(description = f"Your random anime is ``{random.choice(animes)}`` hope you enjoy it!!!")
    emb.colour = discord.Colour.orange()
    await ctx.channel.send(embed = emb)

@client.command(aliases = ['gn'])
async def goodnight(ctx):
    await ctx.send('Goodnight darling :heart: ')


@client.command()
async def slot(ctx,amount = None):
    await open_account(ctx.author)
    
    if amount == None:
        await ctx.send("You have to gamble with something")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount >bal[0]:
        await ctx.send("You cant gamble what you dont have!")
        return
    
    if amount == 0:
        await ctx.send("You try to gamble with nothing but the dealers stare at you weirdly")
        return
    
    if amount <0:
        await ctx.send("You can not gamble with the house's money")
        return
    
    emoji = [':partying_face:', ':zany_face:', ':face_with_monocle:', ':flushed:', ':nerd:']
    first = random.choice(emoji)
    second = random.choice(emoji)
    third = random.choice(emoji)

    em = discord.Embed(title = f"{first} | {second} | {third}")
    await ctx.send(embed = em)

    if first == second == third:
        await update_bank(ctx.author, 2*amount)
        await ctx.send("winner winner winner your bet has just been doubled and deposited into your account")
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send ("sorry you lost")
@client.command()
async def test(ctx):
    await ctx.send(f'all systems working test is complete with latency being {round(client.latency * 1000)}ms all systems are ready to go')

@client.command(aliases = ['bal'])
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s account balance", color = discord.Color.orange())
    em.add_field(name = "Bank Balance",value = bank_amt)
    await ctx.send(embed = em)

@client.command()
@commands.cooldown(1,1800,commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101) + 50

    hours = ["1",
             "2",
             "3",
             "4",
             "5",]

    await ctx.send(f"After {random.choice(hours)} hours of begging you have earned {earnings} kasumi coins!!")
    
    users[str(user.id)]["bank"] += earnings
    
    with open('bank.json','w')as f:
        json.dump(users,f)

@client.command()
@commands.cooldown(1,1800,commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(2001) + 500

    hours = ["1",
             "2",
             "3",
             "4",
             "5",]
    job = ['Police Officer',
           'Investor',
           'Model',
           'Mechanic',
           'Racer',
           'Farmer',
           'Gamer',
           'Streamer']

    em = discord.Embed(description = (f"After {random.choice(hours)} hours of working as a {random.choice(job)} you have earned {earnings} kasumi coins!!"), color = discord.Color.orange() )
    await ctx.send(embed = em)
    
    users[str(user.id)]["bank"] += earnings
    
    with open('bank.json','w')as f:
        json.dump(users,f)


@client.command()
async def pay(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("You cant pay someone nothing thats mean :(")
        return
    
    bal = await update_bank(ctx.author)
    
    amount = int(amount)
    
    if amount>bal[0]:
        await ctx.send("You do not have enough money sorry :(")
        return
    
    if amount == 0:
        await ctx.send("why would you pay someone nothing thats mean")
        return

    if amount<0:
        await ctx.send("You cant pay someone negative amounts of cash that would be hacking")
        return
    
    await update_bank(ctx.author, -1*amount,"bank")
    await update_bank(member,amount,"bank")
    
    await ctx.send(f"You paid {member.mention} {amount} kasumi coins!")
    
    await update_bank(ctx)

@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def fight(ctx,amount = None):
    await open_account(ctx.author)
    
    if amount == None:
        await ctx.send("You have to gamble with something")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount >bal[0]:
        await ctx.send("You cant gamble what you dont have!")
        return
    
    if amount == 0:
        await ctx.send("You try to gamble with nothing but the dealers stare at you weirdly")
        return
    
    if amount <0:
        await ctx.send("You can not gamble with the house's money")
        return
    
    emoji = ['win', 'lose']
    result = random.choice(emoji)
    
    fighters = ['ken kaneki', 'light yagami', 'mike tyson', 'bakugou', 'mob']
    fighter = random.choice(fighters)

    if result == 'win':
        await update_bank(ctx.author, 1*amount)
        await ctx.send(f"You won your fight against {fighter} congrats")
    if result == "lose":
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f"You lost your fight against {fighter} you gotta train harder")


@client.command()
async def takeover(ctx):
    await ctx.send('this world belongs to me kasumi')

@client.command(aliases = ["who is kory"])
async def whoiskory(ctx):
    await ctx.send("kory is a philosophical man who enjoys video games and anime ") 


@client.command()
async def blush(ctx):
    blushes = ["https://i.giphy.com/media/klmpEcFgXzrYQ/200w.webp",
               "https://media.giphy.com/media/4orREzKni7BTi/giphy.gif",
               "https://media.giphy.com/media/4RK7EnRhtkat2/giphy.gif",
               "https://media.giphy.com/media/dkvGrfQ6ryIAU/giphy.gif",
               "https://media.giphy.com/media/6MyjVUoNqFsm4/giphy.gif",
               "https://media.giphy.com/media/1gbQIeNzZxcSk/giphy.gif",
               "https://media.giphy.com/media/T3Vvyi6SHJtXW/giphy.gif",
               "https://media.giphy.com/media/UrPxdGW62TDtS/giphy.gif",
               "https://media.giphy.com/media/ulWUgCk4F1GGA/giphy.gif",
               "https://media.giphy.com/media/UxR7XvbAFqS6Q/giphy.gif",
               "https://media.giphy.com/media/12DrHDhr5dTjgs/giphy.gif",
               "https://media.giphy.com/media/cxRGi2nJb3cBy/giphy.gif"]   
    embed = discord.Embed(title = f"{ctx.author.name} is blushing", color = discord.Color.orange())
    embed.set_image(url = random.choice(blushes))
    await ctx.channel.send(embed = embed)



    

    



    

@client.command(aliases = ["rob"])
@commands.cooldown(1,1800,commands.BucketType.user)
async def steal(ctx):

    await open_account(ctx.author)
    
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(1001) + 100

    people = ["Kory",
             "Jaquaviontavious",
             "Bakugou",
             "A Grandma",
             "Your Math Teacher",
             "Hisoka",
             "candice",
             "Light Yagami",
             "Eren Yeager"]

    
    users[str(user.id)]["bank"] += earnings
    
    with open('bank.json','w')as f:
        json.dump(users,f)

    emb = discord.Embed(description = f"You stole {earnings} kasumi coins from {random.choice(people)} better hope they dont catch you", color = discord.Color.orange() )
    
    await ctx.send(embed=emb)

@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That product is not in stock")
        if res[1]==2:
            await ctx.send(f"You do not have enough money to pay for this")
            return
    await ctx.send(f"You just bought {amount} {item} thanks for your purchase!")

@client.command()
async def koryplaylist(ctx):
    await ctx.send('because you wanted to know what kory listens to heres his playlist https://open.spotify.com/playlist/6Fgu5hJu4HU1XvfXsBqS0V?si=fa743ce97f2e4889')
    
async def open_account(user):
    
    users = await get_bank_data()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["bank"] = 0
    
    with open("bank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "bank"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    
    with open("bank.json","w") as f:
        json.dump(users,f)
    
    bal = [users[str(user.id)]["bank"]]
    return bal
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ == name
            price = item["price"]
            break
    
    if name == None:
        return [False,1]
    
    cost = price*amount

    users = await get_bank_data()
    
    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]['bag']:
            n = thing['item']
            if n == item_name:
                old_amt = thing['amount']
                new_amt = old_amt + amount
                users[str(user.id)]['bag'][index]['amount'] = new_amt
                t = 1
                break
            index +=1
        if t == None:
            obj = {"item":item_name, "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]
    with open("bank.json","w")as f:
        json.dump(users,f)
    
    await update_bank(user,cost*-1,"bank")

    return[True,"Worked"]

async def update_bank(user,change = 0,mode = "bank"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    
    with open("bank.json","w") as f:
        json.dump(users,f)
    
    bal = [users[str(user.id)]["bank"]]
    return bal

token = configData['Token']


client.run(token)
