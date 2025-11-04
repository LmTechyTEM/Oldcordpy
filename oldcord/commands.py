class cmds:
    def __init__(self, prefix, bot):
        self.bot = bot
        self.prefix = prefix
    async def process(self):
        for i in dir(self):
            print(i)