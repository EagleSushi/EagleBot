import discord
import os
import asyncio
import time
import random
from random import randint
from discord.ext import commands
from PIL import Image, ImageFilter
from io import BytesIO


client = commands.Bot(command_prefix='/')

#reddit API setup

#--------


@client.event
#startup
async def on_ready():
	print('Logged in as {0.user}'.format(client))
	game = discord.Game("Being rate limited by Discord | Alpha v0.9.0")
	await client.change_presence(status=discord.Status.idle, activity=game)


#--------

#demo/test commands


#>test command
@client.command()
async def test(ctx):
	await ctx.send('Test complete')


#>embed test command
@client.command()
async def embedtest(ctx):
	embedVar = discord.Embed(title="Embed tester",
	                         description="Test complete",
	                         color=0x00ff00)
	embedVar.add_field(name="Field1", value="Field1 Value", inline=False)
	embedVar.add_field(name="Field2",
	                   value="<:abduloli:692930720544587865>",
	                   inline=False)
	await ctx.send(embed=embedVar)


#>emote test command
@client.command()
async def emojitest(ctx):
	await ctx.send('<:abduloli:692930720544587865>')


#--------

#utility commands


#>ping test command
@client.command()
async def ping(ctx):
	ping = f'My ping is: {round(client.latency*1000)}ms!'
	embedVar = discord.Embed(title="Pong! 🏓 ",
	                         description=ping,
	                         color=0x42f2f5)
	await ctx.send(embed=embedVar)


#>get user ID command @@TODO@@
@client.command
#>get server ID command @@TODO@@

#--------

#fun commands

#>spank command
@client.command()
async def spank(ctx, member: discord.Member):
	await ctx.send(f'*SPANKS {member}*')


#>unretard
@client.command()
async def unretard(ctx, member: discord.Member):
	wait = randint(3, 30)
	subject = f' - Unretarded **{member}**  ✅'
	embedVar = discord.Embed(title="Unretard successful!",
	                         description="Unretard hosted by EagleBot",
	                         color=0x00ff00)
	embedVar.add_field(name="Checking correct subject:",
	                   value=subject,
	                   inline=False)
	embedVar.add_field(name="Checking retard removal: ",
	                   value=" - Temporary removal of retard ✅",
	                   inline=False)
	embedVar.add_field(name="Verifying retard meter: ",
	                   value=" - Retard meter (0/100%)",
	                   inline=False)
	embedVar.add_field(name="_ _", value="_ _", inline=False)
	embedVar.set_footer(
	    text=
	    f"Disclaimer /unretard is only temporary! | (Time to unretard: {wait} seconds) "
	)

	await ctx.send(
	    f'Please wait while we unretard the user. (This may take a while). Estimated time: {(wait)+1} seconds',
	    delete_after=wait)
	async with ctx.channel.typing():
		await asyncio.sleep(wait)
		await ctx.send(embed=embedVar)


#>subreddit command @@TODO@@

#> owofy command 
@client.command() 
async def owoify(ctx, *, message):
  smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)','x3']
  actions = ['*nuzzles*','*pounces*','*blushes*']

  message = message.replace('L','W').replace('l','w')
  message = message.replace('R','W').replace('r','w')

  text = (f'{message}!!! {format(random.choice(smileys))} {format(random.choice(actions))}')
  async with ctx.channel.typing():
    await ctx.send(text)

#drippify command
@client.command()
async def drippify(ctx, *, message):
  emotes = ['🔥','❌🧢','😔','😈','🚰','🧊','🥶','😴','🤐','💪🏿','🥾','💦','☔']
  affix = ['yawll hurr','shieeet','yawll already know','no cap','drippin','mhm']
  text = f'{message} {format(random.choice(affix))} {format(random.choice(affix))} {format(random.choice(emotes))} {format(random.choice(emotes))}'
  message  = message.replace('you','yawll')
  async with ctx.channel.typing():
    await ctx.send(text)

#gravestone command

@client.command()
async def rip(ctx, member : discord.Member = None):
  if not member :
    member = ctx.author

  rip = Image.open('rip.jpg') 
  asset = member.avatar_url_as(size=128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)

  pfp =pfp.resize((192,163))
  rip.paste(pfp,(130,311))
  rip.save('prip.jpg')

  await ctx.send(file = discord.File('prip.jpg'))
  

  



#--------

#moderation commands


#>purge message command
@client.command()
async def purge(ctx, amount=5):
	if (ctx.message.author.permissions_in(
	    ctx.message.channel).manage_messages):
		await ctx.channel.purge(limit=amount + 1)
		await ctx.send(f'Cleared {amount} messages', delete_after=5)


#>kick member command
@client.command()
async def kick(ctx, member: discord.Member, *, reason='no reason.'):
	if (ctx.message.author.permissions_in(ctx.message.channel).administrator):
		kickReason = f'Reason: {reason}'
		embedVar = discord.Embed(title="🥾 Kicked ",
		                         description=kickReason,
		                         color=0xff0000)
		await ctx.send(embed=embedVar)
		await member.kick(reason=reason)


#>ban member command !!WIP!!
@client.command()
async def ban(ctx, member: discord.Member, *, reason='no reason.'):
	if (ctx.message.author.permissions_in(ctx.message.channel).administrator):
		banReason = f'Reason: {reason}'
		bannedMember = f'<:serious:811315620212899880> Banned {member}'
		embedVar = discord.Embed(title=bannedMember,
		                         description=banReason,
		                         color=0xff0000)
		await ctx.send(embed=embedVar)
		await member.ban(reason=reason)


#>add role to member command @@TODO@@


#>mute member command !!WIP!!
@client.command()
async def mute(ctx,
               member: discord.Member,
               duration: int = 60,
               *,
               reason='no reason.'):
	if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
		muted_role = ctx.guild.get_role(813287042456748042)
		normal_role = ctx.guild.get_role(690193537073020965)
		await member.add_roles(muted_role)
		await member.remove_roles(normal_role)
		muteReason = f'Reason: {reason}'
		mutedMember = f'<:killthemkillthemall:799385844740915241> Muted {member} for {duration} minutes'
		embedVar = discord.Embed(title=mutedMember,
		                         description=muteReason,
		                         color=0xff0000)
		await ctx.send(embed=embedVar)
		await asyncio.sleep(duration * 60)
		await member.add_roles(normal_role)
		await member.remove_roles(muted_role)
		await ctx.send(f'Unmuted {member} [MUTE DURATION EXPIRED]')


@client.command()
async def unmute(ctx, member: discord.Member):
	if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
		muted_role = ctx.guild.get_role(813287042456748042)
		normal_role = ctx.guild.get_role(690193537073020965)
		await member.add_roles(normal_role)
		await member.remove_roles(muted_role)
		unmutedMember = f'<:troII:753707536170877109> Unmuted {member}'
		embedVar = discord.Embed(title=unmutedMember,
		                         description="Member unmuted.",
		                         color=0x00ff44)
		await ctx.send(embed=embedVar)


#--------

#token
client.run(os.getenv('TOKEN'))

#await ctx.send(f'Pong! {round(client.latency*1000)}ms')
