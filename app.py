  
import discord
import os


client = discord.Client()

TOKEN = os.environ.get('TOKEN')


@client.event
async def on_message(message):
    content = message.content
    user = message.author
    channel = message.channel

    if user == client.user:
        return

    if content.startswith("-"):
        print(f"----------\nProcessing command: {content}\nFrom: {user}\n----------")

    # Create a server
    if content.startswith("-osucreate"):
        await channel.send("WIP")
    
    # Remove server
    if content.startswith("-osurm"):
        await channel.send("WIP")

    # Stop server
    if content.startswith("-osustop"):
        await channel.send("WIP")
    
    # Get status of a users server
    if content.startswith("-osustatus"):
        await channel.send("WIP")





client.run(TOKEN)