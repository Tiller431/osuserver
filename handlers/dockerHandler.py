import os
import requests
import subprocess
import fileinput
from handlers import nginxHandler as nginx

def getNewID():
    return 1 + len(next(os.walk('servers'))[1])

def startCompose(user_id):
    path = "servers/" + str(user_id)
    result = subprocess.run(["/usr/bin/docker-compose", "up", "-d"], cwd=os.path.realpath(".") + "/" + path)

def stopCompose(user_id):
    path = "servers/" + str(user_id)
    result = subprocess.run(["/usr/bin/docker-compose", "kill"], cwd=os.path.realpath(".") + "/" + path)

def createFiles(user_id):
    path = "servers/" + str(user_id)
    compose_path = path + "/" + "docker-compose.yml"
    if os.path.exists(path):
        return False
    else:
        os.system("cp -r server_template/ " + path)
        subprocess.call(["sed", "-i", "-e",  f's/ID_/{user_id}/g', compose_path])
        return True

def rmALL():
    for i in range(getNewID() - 1):
        i = i + 1
        rmStack(i)

def rmStack(user_id):
    stopCompose(user_id)
    path = "servers/" + str(user_id)
    subprocess.run(["/usr/bin/docker-compose", "down"], cwd=os.path.realpath(".") + "/" + path)
    os.system(f"rm -rf servers/{user_id}")
    rmNginx(user_id)

def updateNginx(user_id):
    subprocess.run(["/usr/bin/docker-compose", "down", "--rmi", "all"], cwd=os.path.realpath(".") + "/nginx-backend")
    os.system(f"cp server_TEMPLATE.conf nginx-backend/rippleginx/servers/{user_id}.conf")
    subprocess.call(["sed", "-i", "-e",  f's/SERVER_ID/{user_id}/g', f"nginx-backend/rippleginx/servers/{user_id}.conf"])
    subprocess.run(["/usr/bin/docker-compose", "up", "-d"], cwd=os.path.realpath(".") + "/nginx-backend")

def rebuildNginx():
    subprocess.run(["/usr/bin/docker-compose", "down", "--rmi", "all"], cwd=os.path.realpath(".") + "/nginx-backend")
    subprocess.run(["/usr/bin/docker-compose", "up", "-d"], cwd=os.path.realpath(".") + "/nginx-backend")

def rmNginx(user_id):
    os.system(f"rm -rf nginx-backend/rippleginx/servers/{user_id}.conf")
    rebuildNginx()


def createServer():
    user_id = getNewID()
    createFiles(user_id)
    startCompose(user_id)
    updateNginx(user_id)
    return f"https://osu.{user_id}.192.168.1.167.xip.io"
