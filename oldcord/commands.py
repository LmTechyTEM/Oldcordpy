class Commands:
    def __init__(self, prefix=""):
        self._prefix = prefix
        self._current_cmd = None
    async def process(self, message):
        if message.content.startswith(self._prefix):
            for i in dir(self):
                if i.startswith("__"):
                    pass
                else:
                    if message.content.startswith(self._prefix):
                        command = message.content.split(" ")[0][len(self._prefix):]
                        if command != "_current_cmd" or command != "_prefix":
                            if hasattr(self, command):
                                self._current_cmd = getattr(self,command)
                                if callable(self._current_cmd):
                                    await self._current_cmd(message)
                                    break
                            

                    
