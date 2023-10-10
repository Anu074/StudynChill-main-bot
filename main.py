import os
import discord
from discord.ext import commands
import asyncio
import random
from keep_alive import keep_alive
import json
import time
from typing import Optional
from discord.ext import tasks

from discord import app_commands #added for slash commands 17/05/23
from replit import db

import tracemalloc
tracemalloc.start()

import replit
# Global variables to store voice channel IDs -- for server stats
bot_channel_id = None
human_channel_id = None
#---------------------------------------------


intents=discord.Intents.all()


bot=commands.Bot(command_prefix='?',intents=intents)


#bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
#bot.remove_command('help')

#added on 15/05/2023 17:20
@bot.event
async def on_ready():
  
  await bot.wait_until_ready() #added later 01/07/2023
  #await bot.change_presence(activity=discord.Game(name="helping my iitm bs degree peeps"))
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my IITM BS friends"))
  print(f'{bot.user} is ready to chat!')
  
  #added later to check member is sharing screen,turn on cam-------
  target_channel_id = 1125314778513027072  # Replace with the ID of your target voice channel #added to to check if members are doing screen share or turned on thier cam or not
  channel = bot.get_channel(target_channel_id)
  if channel:
    #Start the background task
    bot.loop.create_task(check_voice_channel(channel))



  #added for slash commands #17/05 -------
  try:
      synced = await bot.tree.sync()
      print(f"synced {len(synced)} command(s)")
  except Exception as e:
      print(e)

#-----------------------------------------------------







'''
@bot.event 
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="helping my iitm bs degree peeps"))
    #await bot.command.sync() #added later, before that bot is running good (no use as of now)
    #print("Logged in as" +" " + bot.user.name + "!")
    print(f'{bot.user} is ready!')
'''


'''
#added on 15/05/2023 17:18
@bot.event
async def on_message(message):
    await bot.process_commands(message)
'''
@bot.command(name = "hello")
async def hello(ctx):
    await ctx.author.send("hello there, \nhope you are doing good, im the official bot of your lovely sever Study'nChill,\nim so happy to help you, here are some of my active commands you can use \n\n`?notes` - will give the notes website link \n`?print` - type any costum message \n`?ping` - just for fun(shows latency) \nnote - ` i will not be able to respond to any of your querry when im offline`")


@bot.command(name = "ping")
async def ping(ctx):
    await ctx.send(f'pong! ||{round(bot.latency*1000)} ms||')

@bot.command(name = 'notes')
async def notes(ctx):
    await ctx.send("here we go but remember this website doesn't belong to us,"+'https://medium.com/@prathambhalla7/iit-madras-bs-data-science-applications-all-notes-a522ab17c520')


@bot.command()
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)
  


@bot.command(name = 'motivation')
async def motivation(ctx):
  def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)
  await ctx.send(random_line('quotes.txt'))


#adding this  on 12/05/2023 everything is working fine till now
@bot.event
async def on_member_join(member):
  if not member.bot:
    await member.send("Welcome to Study'nChill, :wave: ! \n\nThis is the most friendly server on discord to study and to chill too with your other iitm bs degree peeps where you can study and have fun together \n\nlets go! \n:white_check_mark: get to know about the server<#1092539989486751844>  \n:white_check_mark: Get your roles from <#1107755405439938691> \n:white_check_mark: introduce yourself in <#1092838110452252733> \n:white_check_mark: read server rules <#1064672210024923220> \n\nhope we all will have an amazing journey together lets rock  ")



#addin to update the server stats-----
  await update_member_count() #for server stats

@bot.event
async def on_member_remove(member):
    await update_member_count()


async def update_member_count():
    guild = bot.get_guild(1046852934819909722)  # Replace with guild ID
    if guild is not None:
        category = discord.utils.get(guild.categories, name="server stats")
        if category is None:
            category = await guild.create_category("server stats")
        
        total_bots = sum(member.bot for member in guild.members)
        total_humans = len(guild.members) - total_bots

      # Find or create the voice channels for bots and humans
        global human_channel_id
        if human_channel_id is None:
            human_channel = discord.utils.get(category.voice_channels, name=f"Total Humans: {total_humans}")
            if human_channel is None:
                human_channel = await guild.create_voice_channel(f"Total Humans: {total_humans}", category=category)
            human_channel_id = human_channel.id
        else:
            human_channel = guild.get_channel(human_channel_id)
            await human_channel.edit(name=f"Total Humans: {total_humans}")


        global bot_channel_id
        if bot_channel_id is None:
            bot_channel = discord.utils.get(category.voice_channels, name=f"Total Bots: {total_bots}")
            if bot_channel is None:
                bot_channel = await guild.create_voice_channel(f"Total Bots: {total_bots}", category=category)
            bot_channel_id = bot_channel.id
        else:
            bot_channel = guild.get_channel(bot_channel_id)
            await bot_channel.edit(name=f"Total Bots: {total_bots}")





#adding embed commnad 15/05/2023 before this everything is working fine
#after adding this commnad everything is working fine too that command is also working hurreee


@bot.command()
async def embed(ctx):
    # Define the initial embed message
    embed_msg = discord.Embed()

    # Ask the user for the title
    await ctx.send("What should be the title of the embed message?")
    title = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    # Ask the user for the description
    await ctx.send("What should be the description of the embed message?")
    description = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    # Add the title and description to the embed message
    embed_msg.title = title.content
    embed_msg.description = description.content

    # Ask the user if they want to add any fields
    add_field = True
    while add_field:
        await ctx.send("Do you want to add a field to the embed message? (y/n)")
        add_field_answer = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

        if add_field_answer.content.lower() == 'y':
            # Ask the user for the field name
            await ctx.send("What should be the name of the field?")
            field_name = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

            # Ask the user for the field value
            await ctx.send("What should be the value of the field?")
            field_value = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

            # Add the field to the embed message
            embed_msg.add_field(name=field_name.content, value=field_value.content, inline=False)
        else:
            add_field = False

    # Send the embed message
    msg = await ctx.send(embed=embed_msg)

    # Allow the author to edit the embed message
    await msg.add_reaction('📝')
    await asyncio.sleep(1)  # Wait for reaction to be added

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '📝'

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)
            if reaction.message.id == msg.id:
                await msg.delete()
                await ctx.send("What should be the new description of the embed message?")
                new_description = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                embed_msg.description = new_description.content

                for field in embed_msg.fields:
                    await ctx.send(f"What should be the new value of the field `{field.name}`?")
                    new_value = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    field.value = new_value.content

                new_msg = await ctx.send(embed=embed_msg)
                msg = new_msg
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            break








#adding reaction role commnad before this everything is working fine 15/05/2023


@bot.command()
async def addreactionrole(ctx, message_id, role_name, emoji):
    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            # If role does not exist, create it
            role = await ctx.guild.create_role(name=role_name)
            await ctx.send(f"Role {role_name} created!")

        # Check if the reaction_roles file is empty
        with open("reaction_roles.json", "r") as file:
            data = file.read()
            if len(data) == 0:
                # If the file is empty, create a new dictionary
                reaction_roles = {}
            else:
                reaction_roles = json.loads(data)

        # Add the reaction role to the dictionary
        if message_id not in reaction_roles.keys():
            reaction_roles[message_id] = {}
        reaction_roles[message_id][emoji] = role.id

        # Save the updated dictionary to the file
        with open("reaction_roles.json", "w") as file:
            json.dump(reaction_roles, file)

        message = await ctx.fetch_message(int(message_id))
        await message.add_reaction(emoji)
        await ctx.send(f"Reaction role added: {role_name} - {emoji}")
    except Exception as e:
        print(f"Error adding reaction role: {e}")



#reflectiong roles on user profile

@bot.event
async def on_raw_reaction_add(payload):
    try:
        with open("reaction_roles.json", "r") as file:
            reaction_roles = json.load(file)
        if str(payload.message_id) in reaction_roles.keys() and str(payload.emoji) in reaction_roles[str(payload.message_id)].keys():
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role_id = reaction_roles[str(payload.message_id)][str(payload.emoji)]
            role = guild.get_role(role_id)
            await member.add_roles(role)
            print(f"Added role {role.name} to {member.name}")
    except Exception as e:
        print(f"Error adding role: {e}")








'''
@bot.command()
async def removereactionrole(ctx, role_name, emoji):
    # Get the role and message
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    instructions_message = await ctx.channel.history().get(author=bot.user)

    # Remove the reaction and role from the reaction roles dictionary
    await instructions_message.clear_reaction(emoji)
    reaction_roles = get_reaction_roles()
    reaction_roles.pop(emoji)
    set_reaction_roles(reaction_roles)

    # Notify the user that the reaction role was removed
    response = f'The reaction role "{role_name}" has been removed with the emoji {emoji}.'
    await ctx.send(response)
'''


#updating above command 
#removereactionrolecommand 

@bot.command()
async def removereactionrole(ctx, role_name, emoji, message_id):
    # Get the role and message
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    message = await ctx.fetch_message(int(message_id))

    # Check if the role exists
    if not role:
        await ctx.send(f"The role '{role_name}' does not exist.")
        return

    # Remove the reaction and role from the reaction roles dictionary
    with open("reaction_roles.json", "r") as file:
        reaction_roles = json.load(file)

    if message_id not in reaction_roles.keys() or emoji not in reaction_roles[message_id]:
        await ctx.send(f"The specified reaction role ({role_name} - {emoji}) does not exist.")
        return

    reaction_roles[message_id].pop(emoji)

    with open("reaction_roles.json", "w") as file:
        json.dump(reaction_roles, file)

    # Remove the reaction from the message
    try:
        await message.remove_reaction(emoji, bot.user)
    except discord.NotFound:
        pass

    # Notify the user that the reaction role was removed
    response = f"The reaction role {role_name} - {emoji} has been removed."
    await ctx.send(response)








#remove raction role when reaction remomoved
@bot.event
async def on_raw_reaction_remove(payload):
    try:
        with open("reaction_roles.json", "r") as file:
            reaction_roles = json.load(file)
        if str(payload.message_id) in reaction_roles.keys() and str(payload.emoji) in reaction_roles[str(payload.message_id)].keys():
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role_id = reaction_roles[str(payload.message_id)][str(payload.emoji)]
            role = guild.get_role(role_id)
            await member.remove_roles(role)
            print(f"Removed role {role.name} from {member.name}")
    except Exception as e:
        print(f"Error removing role: {e}")






def get_reaction_roles():
    # Load the reaction roles dictionary from a file
    if os.path.exists('reaction_roles.json'):
        with open('reaction_roles.json', 'r') as f:
            return json.load(f)
    else:
        return {}

    try:
        with open('reaction_roles.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        data = {}
    return data






#command to clear (purge messages)




#updated above command



@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int, user: Optional[discord.Member] = None, include_bots: bool = False):
    """Clears the specified number of messages in the current channel, optionally filtered by user and bots."""
    def is_valid_message(message):
        return (not message.pinned) and (not message.author.bot or include_bots) and (user is None or message.author == user)

    deleted_messages = await ctx.channel.purge(limit=amount + 1, check=is_valid_message)

    await ctx.send(f"Cleared {len(deleted_messages)} messages.", delete_after=5)



#adding slash command 17/05/2023 ---------

@bot.tree.command(name = "namaste")
async def namaste(interaction: discord.Interaction):
  await interaction.response.send_message(f"hello namskar {interaction.user.mention}! its an test slash command!")

#-----------------------------------------------------------


#adding new slash command to send cost0m messages ------------

#not working
@bot.tree.command(name="sendmessage", description="Send a custom message in a specific channel")
async def send_message(ctx: commands.Context, channel: discord.TextChannel, *, message: str):
    # Check if the author has permission to send messages in the specified channel
    if channel.permissions_for(ctx.author).send_messages:
        await channel.send(message)
        await ctx.send("Message sent successfully!")
    else:
        await ctx.send("You don't have permission to send messages in that channel.")






#------------------------------------------------------------

# The pomodoro command



# A dictionary to store the settings and participants of each Pomodoro session
pomodoro_sessions = {}

# A dictionary to store the message objects for each Pomodoro session
pomodoro_messages = {}

# A dictionary to store the study time of each user
study_time = {}

# A helper function to format the embed messages
def create_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Powered by Study'nChill")
    return embed

# A helper function to check if the user is in a voice channel
def in_voice_channel():
    async def predicate(ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            return True
        else:
          
            await ctx.send("You have to be in a voice channel to use this command.")
            raise commands.CheckFailure
    return commands.check(predicate)





# The pomodoro command
@bot.command()
@in_voice_channel() # Require the user to be in a voice channel
async def pomodoro(ctx, work_time: int = 50, break_time: int = 10, cycles: int = 4):
    # Check if there is already a Pomodoro session in the same voice channel
    voice_channel = ctx.author.voice.channel
    if voice_channel.id in pomodoro_sessions:
        await ctx.send(embed=create_embed("Error", "There is already a Pomodoro session in this voice channel.", discord.Color.red()))
        return
    
    # Create a new Pomodoro session with the given settings and participants
    pomodoro_session = {
        "work_time": work_time,
        "break_time": break_time,
        "cycles": cycles,
        "current_cycle": 1,
        "current_time": work_time * 60,
        "is_work": True,
        "is_running": True,
        "participants": [member for member in voice_channel.members if not member.bot]
    }
    pomodoro_sessions[voice_channel.id] = pomodoro_session

    # Notify the participants about the start of the Pomodoro session
    participants = ", ".join(member.mention for member in pomodoro_session["participants"])
    await ctx.send(f"{participants}")
    await ctx.send(embed=create_embed("Pomodoro Session Started", f"\nin Voice Channel: {voice_channel.mention}\n\nWork time: {work_time} minutes\nBreak time: {break_time} minutes\nCycles: {cycles}\nParticipants: {participants}", discord.Color.green()))

    

    # Get the voice channel and the text channel from the bot
    voice_channel = bot.get_channel(voice_channel.id)
    # = ctx.message
    #text_channel = ctx.member
    text_channel = bot.get_channel(1064468194540126248)
    #text_channel = ctx.channel
    #text_channel = voice_channel.guild.text_channels[0]  # You can change this to a specific text channel if you want

    # Send the initial embed message
    embed = create_embed("Work Time", f"Start cycle {pomodoro_session['current_cycle']} of {pomodoro_session['cycles']}.\nWork for {pomodoro_session['work_time']} minutes.\n{participants}", discord.Color.red())
    pomodoro_message = await text_channel.send(embed=embed)

    # Store the message object in the dictionary
    pomodoro_messages[voice_channel.id] = pomodoro_message

    # Start the countdown loop
    pomodoro_loop.start(voice_channel.id)



# keep track of the join time of each member in the voice channel (to count study time)
member_join_times = {}
# Dictionary to store the study start times for each member in each voice channel
study_start_times = {}

    
# The countdown loop that updates the Pomodoro session every second
@tasks.loop(minutes = 1)
async def pomodoro_loop(channel_id):
    # Get the Pomodoro session from the dictionary
    pomodoro_session = pomodoro_sessions[channel_id]

    # Check if the session is running or paused
    if not pomodoro_session["is_running"]:
        return

    embed = discord.Embed()  # Initialize the embed variable
    
    # Get the voice channel and the text channel from the bot
    voice_channel = bot.get_channel(channel_id)
    #text_channel = ctx.channel
    text_channel = bot.get_channel(1064468194540126248)
  
    #text_channel = voice_channel.guild.text_channels[0]  # You can change this to a specific text channel if you want

    # Decrease the current time by one second
    pomodoro_session["current_time"] -= 1*60

    # Check if the current time reaches zero
    if pomodoro_session["current_time"] <= 0:
        # Check if the session is in work time or break time
        if pomodoro_session["is_work"]:
            # Transition to break time
            pomodoro_session["is_work"] = False
            pomodoro_session["current_time"] = pomodoro_session["break_time"] * 60

            # Notify the participants about the break time
            participants = ", ".join(member.mention for member in pomodoro_session["participants"])
            embed = create_embed("Break Time", f"You have completed cycle {pomodoro_session['current_cycle']} of {pomodoro_session['cycles']}.\nTake a `{pomodoro_session['break_time']}` minutes break.\n{participants}", discord.Color.blue())
            if participants:  # Check if participants list is not empty
             tag = await text_channel.send(f"{participants}")
            message = await text_channel.send(embed=embed)
            await asyncio.sleep(10)  # Wait for 10 seconds
            await message.delete()  # Delete the message
            #await asyncio.sleep("break_time")  # Wait for the specified time
            #await asyncio.sleep(10)  # Wait for 10 seconds
            await tag.delete()

            #await embed.delete()  # Delete the message


        else:
            # Check if the session has completed all cycles
            if pomodoro_session["current_cycle"] == pomodoro_session["cycles"]:
                # Stop the countdown loop and delete the Pomodoro session from the dictionary
                pomodoro_loop.stop()
                del pomodoro_sessions[channel_id]

                # Notify the participants about the completion of the Pomodoro session
                participants = ", ".join(member.mention for member in voice_channel.members if not member.bot)
            
                embed = create_embed("Pomodoro Session Completed", f"Congratulations! You have completed all the {pomodoro_session['cycles']} cycles of work.\n{participants}", discord.Color.green())
                
                await text_channel.send(f"{participants}")
                await text_channel.send(embed=embed)
            else:
                # Transition to work time and increase the cycle count by one
                pomodoro_session["is_work"] = True
                pomodoro_session["current_cycle"] += 1
                pomodoro_session["current_time"] = pomodoro_session["work_time"] * 60

                # Notify the participants about the work time
                participants = ", ".join(member.mention for member in voice_channel.members if not member.bot)
                embed = create_embed("Work Time", f"Start cycle {pomodoro_session['current_cycle']} of {pomodoro_session['cycles']}.\nWork for `{pomodoro_session['work_time']}` minutes.\n{participants}", discord.Color.red())
                if participants:  # Check if participants list is not empty
                 tag = await text_channel.send(f"{participants}")
                message = await text_channel.send(embed=embed)
                await asyncio.sleep(10)  # Wait for 10 seconds
                await message.delete()  # Delete the message
                await tag.delete()
                #await asyncio.sleep("work_time")  # Wait for the specified time

                #await embed.delete()  # Delete the message
    
    # Update the remaining work time or break time in the embed message
    minutes = pomodoro_session["current_time"] //60
    #seconds = pomodoro_session["current_time"] %60
    participants = ", ".join(member.mention for member in pomodoro_session["participants"])
    if pomodoro_session["is_work"]:
        embed.title = "Work Time"
        #embed.description = f"Remaining time: `{minutes}` : `{seconds}` \n\npadhai likhai karne wale chhatra \n{participants}"
        embed.description = f"Remaining time: `{minutes}`minutes \n\npadhai likhai karne wale chhatra \n{participants}"
        embed.set_footer(text="Study'nChill")
        embed.color = discord.Color.red()
        #reaction = "✅"  #add emoji reaction

        #await embed.add_reaction(reaction)
    else:
        embed.title = "Break Time"
        #embed.description = f"Remaining time: `{minutes}` : `{seconds}` \n\nkuch doubt ho to discuss kar lo \n{participants}"
        embed.description = f"Remaining time: `{minutes}` minutes \n\nkuch doubt ho to discuss kar lo \n{participants}"
        embed.set_footer(text="Study'nChill")
        embed.color = discord.Color.blue()
        #reaction = "✅"  #  reaction emoji

        #await embed.add_reaction(reaction)
        #reaction = "✅"  # reaction emoji
        #message = await pomodoro_messages[channel_id].edit(embed=embed)
        #await message.add_reaction(reaction)
    # Edit the embed message
    
    reaction = "✅"
    message = await pomodoro_messages[channel_id].edit(embed=embed)
    await message.add_reaction(reaction)




# Dictionary to keep track of voice channels and associated text channels
custom_channels = {}
# The event listener that updates the participants list when a member joins or leaves a voice channel

study_voice_channel_ids = [1046852934819909726, 1125314778513027072]  # Replace with the desired study voice channel IDs 1066055196762984669- ent and fun, 1095230623314092093-welcome, 1076195437792464986- confe, 
hidden_category_ids = [1066055196762984669, 1076195437792464986, 1095230623314092093]  # Replace with the ID of the category to be hidden
hidden_channel_ids = [1064468405173895230, 1064493373613940766, ]  # Replace with the IDs of the specific text channels to be hidden

#uddating the code to count study time more accuratly---------------------
# Define the list of voice channel IDs to track study time
voice_channel_ids = [1046852934819909726, 1125314778513027072]

# Function to record the start time when a user joins a voice channel
def start_study(member, voice_channel_id):
    db[f"study_start_time:{member.id}:{voice_channel_id}"] = time.time()

# Function to calculate and update study time when a user leaves a voice channel
def stop_study(member, voice_channel_id):
    start_time_key = f"study_start_time:{member.id}:{voice_channel_id}"
    start_time = db.get(start_time_key)
    
    if start_time is not None:
        current_time = time.time()
        elapsed_time = current_time - start_time

        study_time_key = f"study_time:{member.id}:{voice_channel_id}"
        total_study_time = db.get(study_time_key, default=0)
        total_study_time += elapsed_time
        db[study_time_key] = total_study_time

        del db[start_time_key]  # Remove the start time from the database

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    
    if before.channel != after.channel:
        # Check if the member is participating in a Pomodoro session
        for session in pomodoro_sessions.values():
            if member in session["participants"]:
                # Update the participants list based on the new voice state
                voice_channel = before.channel or after.channel
                session["participants"] = [member for member in voice_channel.members if not member.bot]

                # Notify the participants about the change
                participants = ", ".join(member.mention for member in session["participants"])
                embed = create_embed("Participants Updated", f"Participants: {participants}", discord.Color.green())
                text_channel = bot.get_channel(1064468194540126248) # You can change this to a specific text channel if you want
                if participants:
                 tag = await text_channel.send(f"{participants}")
                message = await text_channel.send(embed=embed)
                await asyncio.sleep(10)  # Wait for 10 seconds
                await message.delete()  # Delete the message
                await tag.delete()  # Delete the message
                

              
              # Check if all participants have left the voice channel
                if not session["participants"]:
                    # Pause the Pomodoro session
                    session["is_running"] = False

                    # Notify the participants about the pause
                    text_channel = bot.get_channel(1064468194540126248)  # change this to a specific text channel
                    embed = create_embed("Pomodoro Session Paused", "All participants have left the voice channel. The session has been paused.", discord.Color.orange())
                    await text_channel.send(embed=embed)
                else:
                    # Check if the Pomodoro session is paused and participants have joined
                    if not session["is_running"]:
                        # Resume the Pomodoro session
                        session["is_running"] = True

                        # Notify the participants about the resume
                        participants = ", ".join(member.mention for member in session["participants"])
                        text_channel = bot.get_channel(1064468194540126248)  #  change this to a specific text channel
                        embed = create_embed("Pomodoro Session Resumed", "All participants have joined the voice channel. The session has been resumed.", discord.Color.green())
                        await text_channel.send(embed=embed)
                break
              
#syncing the create costum voice channle in this on voice state update ---

  
    # Check if the member joined the specific voice channel
    if after.channel and after.channel.id == 1111673115118936144:  # Replace SPECIFIC_VOICE_CHANNEL_ID with the desired voice channel ID
        guild = member.guild
        category = guild.get_channel(1113776348842967132)  # Replace CATEGORY_ID with the desired category ID

        # Create the custom voice channel
        voice_channel = await category.create_voice_channel(f"{member.name}'s Voice Channel")

        # Create the associated text channel
        text_channel = await category.create_text_channel(f"{member.name}'s Text Channel")


        # Move the member to the created voice channel
        await member.move_to(voice_channel)

        # Grant necessary permissions
        await voice_channel.set_permissions(member, connect=True, manage_channels=True)
        await text_channel.set_permissions(member, manage_channels=True)

        # Store the custom channels in the dictionary
        custom_channels[voice_channel.id] = text_channel.id
      
        # Send a direct message to the member
        #await member.send("Your custom voice channel and text channel have been created!")



     # Check if the member left a voice channel
    if before.channel and before.channel.id in custom_channels:
        # Get the associated text channel
        text_channel_id = custom_channels[before.channel.id]
        text_channel = bot.get_channel(text_channel_id)

        # Check if all members have left the voice channel
        if len(before.channel.members) == 0:
            # Delete the voice channel and text channel
            await before.channel.delete()
            await text_channel.delete()

            # Remove the custom channels from the dictionary
            del custom_channels[before.channel.id]

  
    #voice_channel_id =   1046852934819909726 #to count study time
    voice_channel_ids = [1046852934819909726, 1125314778513027072]

    #to count stuy time in replit db 05/09/23-----------------------------------

    # Check if the member is joining or leaving a voice channel
    if before.channel != after.channel:
      if after.channel and after.channel.id in voice_channel_ids:
        start_study(member, after.channel.id)
    elif before.channel and before.channel.id in voice_channel_ids:
        stop_study(member, before.channel.id)




    #to hide unnecessory channels and categories-----
    if after.channel and after.channel.id in study_voice_channel_ids:
        # Hide the specified categories for the member
        for category_id in hidden_category_ids:
            category = discord.utils.get(member.guild.categories, id=category_id)
            if category:
                await category.set_permissions(member, read_messages=False)
        
        # Hide specific text channels within the categories for the member
        for channel_id in hidden_channel_ids:
            channel = discord.utils.get(member.guild.channels, id=channel_id)
            if channel:
                await channel.set_permissions(member, read_messages=False)
    
    elif before.channel and before.channel.id in study_voice_channel_ids:
        # Restore permissions for the hidden categories
        for category_id in hidden_category_ids:
            category = discord.utils.get(member.guild.categories, id=category_id)
            if category:
                await category.set_permissions(member, read_messages=None)
        
        # Restore permissions for the hidden text channels
        for channel_id in hidden_channel_ids:
            channel = discord.utils.get(member.guild.channels, id=channel_id)
            if channel:
                await channel.set_permissions(member, read_messages=None)



# # Function to count study time for each member in a voice channel
# def count_study_time(voice_channel_id, member, study_time):
# #def count_study_time(voice_channel_id, study_time):
#     voice_channel = bot.get_channel(voice_channel_id)
#     for member in voice_channel.members:
#         # Ignore bots
#         if member.bot:
#             continue

#         member_id = str(member.id)
#         if f"study_time:{member_id}" in db:
#             db[f"study_time:{member_id}"] += study_time
#         else:
#             db[f"study_time:{member_id}"] = study_time

# Function to get the total study time for a user in a specific voice channel
def get_total_study_time(member, voice_channel_id):
    study_time_key = f"study_time:{member.id}:{voice_channel_id}"
    total_study_time = db.get(study_time_key, default=0)
    return total_study_time




# Command to display the leaderboard in sorted form
@bot.command()
async def rank(ctx):
  # Fetch all study time data from Replit DB
  #study_times = [(member_id, db[f"study_time:{member_id}"]) for member_id in db.keys() if member_id.startswith("study_time:")]
  #study_times = [(member_id, db[f"study_time:{member_id.split(':')[1]}"]) for member_id in db.keys() if member_id.startswith("study_time:")]
  study_times = [(member_id, db[member_id]) for member_id in db.keys() if member_id.startswith("study_time:")]



  # Sort the study times in descending order
  study_times = sorted(study_times, key=lambda x: x[1], reverse=True)

  # Create the leaderboard embed
  leaderboard_embed = discord.Embed(title="Study Time Leaderboard", color=discord.Color.gold())
  # Set the footer
  leaderboard_embed.set_footer(text="Powered by Study'nChill")
 
  #leaderboard_embed.set_thumbnail(url="study'nchill leaderboard.png")


  #adding later-----------

  # Create separate lists for users and study times
  user_data = []
  study_times_formatted = []
  
  # Prepare a string to store the formatted leaderboard data, added later
  leaderboard_data = ""
  role_id = ""

  # Add user and formatted study time data to the respective lists
  for index, (member_id, study_time) in enumerate(study_times):
      # Convert the member ID to an integer
      member_id = int(member_id.split(":")[1])

      # Fetch the member object from the member ID
      member = ctx.guild.get_member(member_id)

      # Calculate study time in hours and minutes
      study_hours = study_time // 3600
      study_minutes = (study_time % 3600) // 60
      # Assign roles based on study time
      if study_time >= 3600*250:  # If study time is 250 hour or more
          role_id = 1073849614685458484
      elif study_time >= 3600*200:  # If study time is 200 hour or more
          role_id = 1073849596519923713  # Replace with the role ID of Role 1
      elif study_time >= 3600*160:  # If study time is 30 minutes or more
          role_id =  1073849581143588994 # Replace with the role ID of Role 2
      elif study_time >= 3600*120: # If study time is 30 minutes or more
          role_id =  1073849565658218586  # Replace with the role ID of Role 2
      elif study_time >= 3600*80: # If study time is 30 minutes or more
          role_id =  1073849540400132148  # Replace with the role ID of Role 2
      elif study_time >= 3600*40: # If study time is 30 minutes or more
          role_id =  1073849527045468270  # Replace with the role ID of Role 2
      elif study_time >= 3600*20: # If study time is 30 minutes or more
          role_id =  1073849506124288000  # Replace with the role ID of Role 2
      elif study_time >= 3600*10: # If study time is 30 minutes or more
          role_id =  1073849487350583328 # Replace with the role ID of Role 2
      elif study_time >= 3600*6: # If study time is 30 minutes or more
          role_id =  1073849471185723423  # Replace with the role ID of Role 2
      elif study_time >= 3600*3: # If study time is 30 minutes or more
          role_id =  1073849451652861982  # Replace with the role ID of Role 2
      
      
      else:
          role_id = 1073848877108711445

      # Get the role object from the role ID
      #role = ctx.guild.get_role(role_id)
      role = discord.utils.get(ctx.guild.roles, id=role_id)
      if role and role not in member.roles:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} Congratulations! You have earned the role <@&{role_id}>!")


    
     # Format the user and study time data in a tabular format. added later----
      leaderboard_data += f"{index+1}. {member.mention:<20} {study_hours:>2} hours {study_minutes:>2} minutes | <@&{role_id}>\n"


    
      # Format the user data with numbering
      user_data.append(f"{index+1}. {member.mention}")


      # Add user and formatted study time to the respective lists
      #users.append(member.mention)
      study_times_formatted.append(f"{study_hours} hours {study_minutes} minutes")

#removing study role from here and moved it upside there




  # Add the leaderboard data as a field in the embed #added later
  leaderboard_embed.add_field(name="Rank   User                 Study Time   Study Role", value=leaderboard_data)

 
  # Send the leaderboard embed to the channel
  await ctx.send( embed=leaderboard_embed)





#self rank command -----------------
@bot.command()
async def srank(ctx):
    # Fetch the study time for the user invoking the command
    study_time_key = f"study_time:{ctx.author.id}"
    if study_time_key not in db:
        await ctx.send("You haven't recorded any study time yet.")
        return
      
    # Fetch the study time for the user invoking the command
    study_time = db[f"study_time:{ctx.author.id}"]
  
    # Calculate study time in hours and minutes
    study_hours = study_time // 3600
    study_minutes = (study_time % 3600) // 60

    # Determine the next study badge and the remaining time needed to achieve it
    next_badge = ""
    remaining_time = 0

    if study_time >= 3600*250:
        next_badge = "No more study badges"
    elif study_time >= 3600*200:
        next_badge = "psychopath (250+)"
        remaining_time = (3600*250) - study_time
    elif study_time >= 3600*160:
        next_badge = "productivity master(200-250)"
        remaining_time = (3600*200) - study_time
    elif study_time >= 3600*120:
        next_badge = "grandmaster(160-200)"
        remaining_time = (3600*160) - study_time
    elif study_time >= 3600*80:
        next_badge = "master(120-160)"
        remaining_time = (3600*120) - study_time
    elif study_time >= 3600*40:
        next_badge = "proffesor(80-120)"
        remaining_time = (3600*80) - study_time
    elif study_time >= 3600*20:
        next_badge = "expert(40-80)"
        remaining_time = (40) - study_time
    elif study_time >= 3600*10:
        next_badge = "proffesional(20-40)"
        remaining_time = (3600*20) - study_time
    elif study_time >= 3600*6:
        next_badge = "advanced(10-20)"
        remaining_time = (3600*10) - study_time
    elif study_time >= 3600*3:
        next_badge = "intermediate(6-10)"
        remaining_time = (3600*6) - study_time
    else:
        next_badge = "beginar"
        remaining_time = (3600*3) - study_time

    # Calculate remaining time in hours and minutes
    remaining_hours = remaining_time // 3600
    remaining_minutes = (remaining_time % 3600) // 60

     # Get the user's current study badge role
    current_badge = None
    for role in ctx.author.roles:
        if role.id in [1073849614685458484, 1073849596519923713, 1073849581143588994, 1073849565658218586, 1073849540400132148, 1073849527045468270, 1073849506124288000, 1073849487350583328, 1073849471185723423, 1073849451652861982, 1073848877108711445]:
          current_badge = role.mention
          
      # Create the self-rank embed
    selfrank_embed = discord.Embed(title="Your Study Time Details", color=discord.Color.blue())
    selfrank_embed.add_field(name="User", value=ctx.author.mention, inline=True)
    selfrank_embed.add_field(name="Study Time", value=f"{study_hours} hours {study_minutes} minutes", inline=True)
    selfrank_embed.add_field(name="Current Study Badge", value=current_badge, inline=False)
    selfrank_embed.add_field(name="Next Study Badge", value=next_badge, inline=False)
    selfrank_embed.add_field(name="Remaining Time", value=f"{remaining_hours} hours {remaining_minutes}minutes", inline=False)
    #selfrank_embed.set_thumbnail(url=ctx.author.avatar_url)


    # Send the self-rank embed to the user
    await ctx.send(embed=selfrank_embed)





  






#command to delete the pomodoro

@bot.command()
async def delete_pomodoro(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel.id in pomodoro_sessions:
        del pomodoro_sessions[voice_channel.id]  # Remove the Pomodoro session from the dictionary
        await ctx.send("Pomodoro session deleted.")
    else:
        await ctx.send("There is no active Pomodoro session in this voice channel.")



#adding command to lock and unlock costum voice channles 


@bot.command()
async def lock(ctx):
    voice_channel = ctx.author.voice.channel

    # Check if the voice channel is a custom channel
    if voice_channel.id not in custom_channels:
        await ctx.send("You can only lock custom voice channels.")
        return

    text_channel_id = custom_channels[voice_channel.id]
    text_channel = bot.get_channel(text_channel_id)

    # Hide the text channel by adjusting permissions
    await text_channel.set_permissions(ctx.guild.default_role, read_messages=False)

    # Lock the voice channel
    await voice_channel.set_permissions(ctx.guild.default_role, connect=False)

    # Allow access to the text channel for voice channel members
    for member in voice_channel.members:
        await text_channel.set_permissions(member, read_messages=True)

    await ctx.send("The voice channel has been locked and the associated text channel has been made visible to voice channel members.")

@bot.command()
async def unlock(ctx):
    voice_channel = ctx.author.voice.channel

    # Check if the voice channel is a custom channel
    if voice_channel.id not in custom_channels:
        await ctx.send("You can only unlock custom voice channels.")
        return

    # Unlock the voice channel
    await voice_channel.set_permissions(ctx.guild.default_role, connect=True)

    await ctx.send("The voice channel has been unlocked.")


# Ghost command to hide the text channel and the associated voice channel
@bot.command()
async def ghost(ctx):
    voice_channel = ctx.author.voice.channel

    # Check if the voice channel is a custom channel
    if voice_channel.id not in custom_channels:
        await ctx.send("You can only ghost custom voice channels.")
        return

    text_channel_id = custom_channels[voice_channel.id]
    text_channel = bot.get_channel(text_channel_id)

    # Hide the text channel by adjusting permissions
    await text_channel.set_permissions(ctx.guild.default_role, read_messages=False)

    # Hide the voice channel and deny view_channel permission for everyone else
    for role in ctx.guild.roles:
        if role != ctx.guild.default_role:
            await voice_channel.set_permissions(role, view_channel=False)

    # Allow access to the text channel for voice channel members
    for member in voice_channel.members:
        await text_channel.set_permissions(member, read_messages=True)

    await ctx.send("The voice channel has been ghosted, and the associated text channel has been made visible to voice channel members.")


# Public command to make the voice and text channels visible to everyone
@bot.command()
async def public(ctx):
    voice_channel = ctx.author.voice.channel

    # Check if the voice channel is a custom channel
    if voice_channel.id not in custom_channels:
        await ctx.send("You can only make custom voice channels public.")
        return

    text_channel_id = custom_channels[voice_channel.id]
    text_channel = bot.get_channel(text_channel_id)

    # Allow viewing the text channel for everyone
    await text_channel.set_permissions(ctx.guild.default_role, read_messages=True)

    # Allow viewing the voice channel for everyone
    for role in ctx.guild.roles:
        await voice_channel.set_permissions(role, view_channel=True)

    await ctx.send("The voice channel and associated text channel are now visible to everyone.")

# Error handling for the ghost command
@ghost.error
async def ghost_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please join a custom voice channel to use the ghost command.")
    else:
        await ctx.send("An error occurred while processing the command.")

# Error handling for the public command
@public.error
async def public_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please join a custom voice channel to use the public command.")
    else:
        await ctx.send("An error occurred while processing the command.")




#function to check if they have turn on theri cam or doing screen share or not
async def check_voice_channel(channel):
    while True:
        for member in channel.members:
            if member.bot:
              continue  # Skip if the member is a bot
              
            if not member.voice.self_video and not member.voice.self_stream:
                await member.send("```You have not started sharing your screen or turned on your camera.\n Please do so within 2 minutes or you will be kicked.```")
                await asyncio.sleep(120)  # 2 minutes delay

                # Check if the member has still not started screen sharing or turned on the camera
                if not member.voice.self_video and not member.voice.self_stream:
                    await member.move_to(None)  # Replace None with the desired voice channel ID to move the user
                    #await member.send("You have been kicked from the voice channel for not starting screen sharing or turning on your camera.")
                    # Optionally, you can send a message to a specific channel to log the action
                    log_channel_id = 1064468194540126248  # Replace with the ID of your log channel
                    log_channel = bot.get_channel(log_channel_id)
                    if log_channel:
                        await log_channel.send(f"{member.mention} was kicked from the voice channel for not starting screen sharing or turning on the camera.")

        await asyncio.sleep(60)  # Check every minute


'''
async def check_voice_channel(channel):
    while True:
        for member in channel.members:
            if not member.voice.self_video and not member.voice.self_stream:
                # Warn the member if 2 minutes have passed
                if member.id not in warned_members and member.id not in kicked_members:
                    warned_members.add(member.id)
                    await member.send("You have not started sharing your screen or turned on your camera. Please do so within 3 minutes or you will be kicked.")
                    await asyncio.sleep(180)  # 3 minutes delay

                # Kick the member if 5 minutes have passed since the warning
                if member.id in warned_members and member.id not in kicked_members:
                    kicked_members.add(member.id)
                    await member.move_to(None)  # Replace None with the desired voice channel ID to move the user
                    await member.send("You have been kicked from the voice channel for not starting screen sharing or turning on your camera.")
                    # Optionally, you can send a message to a specific channel to log the action
                    log_channel_id = 1064468194540126248  # Replace with the ID of your log channel
                    log_channel = bot.get_channel(log_channel_id)
                    if log_channel:
                        await log_channel.send(f"{member.mention} was kicked from the voice channel for not starting screen sharing or turning on the camera.")

        await asyncio.sleep(60)  # Check every minute
warned_members = set()
kicked_members = set()
'''

      
#addig command to clear replit db--------
@bot.command()
@commands.has_permissions(administrator=True)
async def cleardb(ctx):
    # Clear the Replit DB
    replit.db.clear()
    await ctx.send("Replit DB has been cleared.")


#adding insult command ---------
@bot.command(name='insult')
async def insult(ctx, user: discord.Member):
    def random_line(fname):
        lines = open(fname).read().splitlines()
        return random.choice(lines)

    if user == bot.user:
        # Send a different message if the bot is mentioned
        await ctx.send("I'm sorry babu, aapko ban karna padega server se ..!")
    else:
        insult_line = random_line('insult.txt')
        insult_message = f"{user.mention}, {insult_line}"
        await ctx.send(insult_message)

    # Delete the user's message invoking the command
    await ctx.message.delete()






keep_alive()
my_secret = os.environ['token']

try:
  bot.run(os.getenv('token'))
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("python restarter.py")
