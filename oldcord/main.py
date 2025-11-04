import requests
import websockets
import json
import asyncio

from .requester import Requester

from .classes import *
from .commands import cmds


# ill just throw the token into cmds like you use the commmands class and if the client sees it itll put the bot client in there so piss off
class Commands:
    def __init__(self, prefix=""):
        self.prefix = prefix
    def process(self):
        for i in self:
            print(i)


class Client:
    def __init__(self, url, debug=False, commands=None):
        self.user_agent = "Oldcord Bot"
        self.url = url
        self.debug = debug
        self.req = requests.session()
        self.requests = Requester(self.user_agent, self.url)
        self.token = None
        self.guilds = []
        self._cmds = []
        self.user:User = None
        self.dm_channels = []
        self.commands: Commands | None = commands       
    async def start(self, token=None):
        if self.url is None:
            print("Please specify an oldcord instance url.")
            return
        if token is None:
            print("Please specify a token.")
            return
        self.token = token
        try:
            data = self.req.get(f"{self.url}/instance")
        except Exception as e:
            print(f"Could not connect to instance: {e}")
            print("Trying again in 5 seconds...")
            await asyncio.sleep(5)
            await self.start(token)
        gateway = f"{data.json()['gateway']}?encoding=json&v=6"
        self.requests._addToken(token)
        try:
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
                    if self.debug == True:
                        if event == "PRESENCE_UPDATE":
                            pass
                        else:
                            print(event)
                    d = data['d']
                    
                    if event == "MESSAGE_CREATE":
                        if not isinstance(d, int):
                            message = Message(d, self)
                            if self.commands:
                                commands = cmds(self.commands.prefix, self)
                                await commands.process()

                            await self.on_message(Message(d, self)) 
                    if event == "GUILD_CREATE":
                        self.guilds.append(Guild(d, self))
                    if event == "CHANNEL_CREATE":
                        if d['guild_id']:
                            for guild in self.guilds:
                                if guild.id == d['guild_id']:
                                    guild.channels.append(GuildChannel(d, self))
                        else:
                            self.dm_channels.append(DMChannel(d, self))
                    if event == "READY":
                        self.user = User(d['user'],self)
                        await self.on_ready(User(d['user'], self))
                        for guild in d['guilds']:
                            self.guilds.append(Guild(guild, self))
                        for channel in d['private_channels']:
                            self.dm_channels.append(DMChannel(channel, self))
                        if self.debug == True:
                            print(d['user'])

                                
                    if event == "PRESENCE_UPDATE":
                        pass
                        #return
                        #for guild in self.guilds:
                        #    if guild.id == d['guild_id']:
                        #        for presence in guild.presences:
                        #            if presence.user.id == d['user']['id']:
                        #                self.guilds[self.guilds.index(guild)].presences[guild.presences.index(presence)] = Presence(d, self)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed, reconnecting...")
            await self.start(token)
                                