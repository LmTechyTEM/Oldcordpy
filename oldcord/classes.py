
from .requester import Requester

class Channel:
    def __init__(self, data, bot):
        self.raw = data
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.bot = bot
    async def send(self, content):
        self.bot.requester.POST(f'channels/{self.id}',data={'content':content})

class Guild:
    def __init__(self, data, bot):
        self.channels = []
        for channel in data['channels']:
            self.channels.append(Channel(channel, bot))

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


