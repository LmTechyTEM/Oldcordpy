
from .requester import Requester

class Channel:
    def __init__(self, data, bot):
        self.raw = data
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self._req = Requester()
    async def send(self, content):
        pass

class Guild:
    def __init__(self, data):
        self.channels = []
        for channel in data['channels']:
            self.channels.append(Channel(channel))

class Message:
    def __init__(self,data):
        self.content = data['content']
        self.channel_id = data['channel_id']
        self.raw = data
