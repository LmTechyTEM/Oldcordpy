import requests
import websockets
import json
import asyncio

from .requester import Requester

from .classes import *

class Client:
    def __init__(self, url, secure=False):
        self.user_agent = "Oldcord Bot"
        self.url = url
        self.req = requests.session()
        self.requests = Requester(self.user_agent, self.url)
        self.token = None
    async def start(self, token=None):
        if self.url is None:
            print("Please specify an oldcord instance url.")
            return
        if token is None:
            print("Please specify a token.")
            return
        self.token = token
        data = self.req.get(f"{self.url}/instance")
        gateway = f"{data.json()['gateway']}?encoding=json&v=6"
        self.requests._addToken(token)
        async with websockets.connect(gateway) as ws:
            identify_payload = {
                "op": 2,
                "d": {
                    "token": f"Bot {token}",
                    "properties": {
                        "os": "Linux",
                        "browser": "Firefox",
                        "device": "Terminal",
                        "referrer": f"{self.url}/selector",
                        "referring_domain": f"{self.url}"
                    }
                }
            }
            await ws.send(json.dumps(identify_payload))

            resp = await ws.recv()
            print("Received:", resp)

            data = json.loads(resp)
            interval = data["d"]["heartbeat_interval"] / 1000
            seq = 0

            async def heartbeat():
                nonlocal seq
                while True:
                    await asyncio.sleep(interval)
                    seq += 1
                    await ws.send(json.dumps({"op": 1, "d": seq}))

            asyncio.create_task(heartbeat())

            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                try:
                    event = data['t']
                except Exception as e:
                    pass
                print(event)
                d = data['d']
                if event == "MESSAGE_CREATE":
                    if not isinstance(d, int):
                        await self.on_message(Message(d)) 
                if event == "READY":
                    await self.on_ready()
                    for guild in d['guilds']:
                        Guild(guild, self)
                    
