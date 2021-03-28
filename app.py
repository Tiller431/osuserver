  
import discord
import os
from handlers import dockerHandler as docker
import time

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
        await channel.send(docker.createServer())
    
    # Remove server
    if content.startswith("-osurmall"):
        start_time = time.time()
        docker.rmALL()
        await channel.send(f"Done! Took {start_time - time.time()} seconds!")

    # Stop server
    if content.startswith("-osustop"):
        await channel.send("WIP")
    
    # Get status of a users server
    if content.startswith("-osustatus"):
        await channel.send("WIP")

    # Restart main nginx server
    if content.startswith("-restartnginx"):
        start_time = time.time()
        docker.rebuildNginx()
        await channel.send(f"Done! Took {start_time - time.time()} seconds!")





client.run(TOKEN)