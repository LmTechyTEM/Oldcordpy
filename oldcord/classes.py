
from .requester import Requester

class Channel:
    def __init__(self, data, bot):
        self.raw = data
        self.bot = bot
        self.id = data['id']
        self._type = data['type']
        self.guild_id = data['guild_id']
        self.last_message_id = data['last_message_id']
    async def send(self, content):
        t = self.bot.requests.POST(f'channels/{self.id}/messages',data={'content':content})
        
        if self.bot.debug == True:
            print(t.text)
        return Message(t.json(), self.bot)
    async def fetch_messages(self, limit=50):
        t = self.bot.requests.GET(f'channels/{self.id}/messages?limit={limit}')
        print(t)
        messages = []
        for message in t.json():
            messages.append(Message(message, self.bot))
        return messages

class GuildChannel(Channel):
    def __init__(self, data, bot):
        super().__init__(data, bot)
        self.name = data['name']
        self.position = data['position']

class DMChannel(Channel):
    def __init__(self, data, bot):
        super().__init__(data, bot)
        self.recipients = []
        for user in data['recipients']:
            self.recipients.append(User(user, bot))

class Guild:
    def __init__(self, data, bot):
        self.id = data['id']
        self.name = data['name']
        self.channels:Channel = []
        self.roles:Role = []
        for channel in data['channels']:
            self.channels.append(GuildChannel(channel, bot))
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
        self.author:User = User(data['author'], bot)
        self.guild_id = data.get('guild_id')
        if data.get('guild_id') != None:
            self.guild_id = data['guild_id']
            for guild in self._self.guilds:
                if guild.id == self.guild_id:
                    self.guild:Guild = guild
                    for channel in guild.channels:
                        if channel.id == self.channel_id:
                            self.channel:Channel = channel
        else:
            self.guild_id = None
            self.guild = None
        for channel in self._self.dm_channels:
            if channel.id == self.channel_id:
                self.channel:DMChannel = channel
    async def edit(self, content):
        
        t = self._self.requests.PATCH(f'channels/{self.channel_id}/messages/{self.raw["id"]}',data={'content':content})
    async def delete(self):
        t = self._self.requests.DELETE(f'channels/{self.channel_id}/messages/{self.raw["id"]}')
        

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
    def __init__(self, data, bot):
        self.id = data['id']
        self.username = data['username']
        self.discriminator = data['discriminator']
        self.bot = data['bot']
        self._avatar = data.get('avatar')
