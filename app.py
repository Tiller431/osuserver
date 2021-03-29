  
import discord
import os
from handlers import dockerHandler as docker
import time
import threading

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
        print(f"----------\nProcessing command: {content}\nFrom: @{user}\n----------")

    # Create a server
    if content.startswith("-create"):
        start_time = round(time.time(), 2)
        process = threading.Thread(target=docker.createServer)
        process.start()
        await channel.send(f"The url to your server is: {docker.getURL()}\nPlease allow about 30 seconds for the server to start. ")
    
    if content.startswith("-masscreate"):
        message = "The urls to your servers are: \n"
        try:
            num_servers = int(content.split(" ")[1])
        except:
            await channel.send("please specify how many servers you would like")
            return

        if num_servers > 25:
            await channel.send("damn bruh i dont have that much server power to give away")
            return
        for i in range(num_servers):
            i = i + 1
            process = threading.Thread(target=docker.createServer, args=(False, ))
            process.start()
            time.sleep(0.3)
            message += f"https://osu.{i}.192.168.1.167.xip.io\n"
        await channel.send(message)

    if content.startswith("-getallservers"):
        message = "These are all of the servers running: \n"
        for i in range(docker.getNewID() - 1):
            i = i + 1
            message += f"https://osu.{i}.192.168.1.167.xip.io\n"
        await channel.send(message)

    # Remove server
    if content.startswith("-rmall"):
        start_time = time.time()
        docker.rmALL()
        await channel.send("Done!")

    # Stop server
    if content.startswith("-stop"):
        await channel.send("WIP")
    
    # Get status of a users server
    if content.startswith("-status"):
        await channel.send("WIP")

    # Restart main nginx server
    if content.startswith("-restartnginx"):
        start_time = time.time()
        docker.rebuildNginx()
        await channel.send(f"Done! Took {time.time() - start_time} seconds!")
    
    # Restart all osu! servers
    if content.startswith("-restartall"):
        start_time = time.time()
        docker.restartAll()
        await channel.send(f"Done! Took {time.time() - start_time} seconds!")





client.run(TOKEN)