
from .requester import Requester

class Channel:
    def __init__(self, data, bot):
        self.raw = data
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.bot = bot
    async def send(self, content):
        t = self.bot.requests.POST(f'channels/{self.id}/messages',data={'content':content})
        print(t.text)

class Guild:
    def __init__(self, data, bot):
        self.id = data['id']
        self.name = data['name']
        self.channels:Channel = []
        self.roles:Role = []
        for channel in data['channels']:
            self.channels.append(Channel(channel, bot))
        for role in data['roles']:
            self.roles.append(Role(role))
class Message:
    def __init__(self,data, bot):
        self.content = data['content']
        self.channel_id = data['channel_id']
        self._self = bot
        self.raw = data
        self.guild = None
        self.channel = None
        self.guild_id = data.get('guild_id')
        if data.get('guild_id') != None:
            self.guild_id = data['guild_id']
            for guild in self._self.guilds:
                if guild.id == self.guild_id:
                    self.guild:Guild = guild
            for channel in guild.channels:
                if channel.id == self.channel_id:
                    self.channel:Channel = channel

class Role:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.position = data['position']
        self.color = data['color']
        self.hoist = data['hoist']
        self.mentionable = data['mentionable']
        self.raw_permissions = data['permissions']

class User:
    def __init__(self, data):
        pass