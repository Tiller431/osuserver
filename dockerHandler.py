import os
import requests
import subprocess


def startCompose(id)
result = subprocess.run(
    ["/usr/bin/docker-compose", "up", "-d"], capture_output=True, text=True
)