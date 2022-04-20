import queue

class messageHandler:
    def __init__(self, chatfp):
        self.chatQueue = queue.Queue(30)
        self.commands = []
        self.chatHistoryFile = open(chatfp, "w")
        self.chatHistoryFile.close()


    class message:
        def __init__(self, source, author, msg):    
            self.source = source
            self.author = author

            self.chat = author + "(" + source + ") " + msg

            self.command = msg.lower()
            self.command = self.command.strip()
            
    # Take in message object params, add to chatQueue and commands list
    def put_message(self, source, user, line, print = True):
        msg = self.message(source, user, line)
        if print:
            if self.chatQueue.full():
                self.chatQueue.get(0)
            self.chatQueue.put(msg)
        self.commands.append(msg)

    # Clear commands list
    def clear_commands(self):
        self.commands.clear()

    # Closes chat file (called when login screen is checked ~ every 10s)
    def close_chat_file(self):
        self.chatHistoryFile.close()

    # Writes chat to output for OBS
    def writeChatToFile(self):
        if self.chatHistoryFile.closed: # Check if file is already open, if not open it
            self.chatHistoryFile = open(self.chatHistoryFile.name,self.chatHistoryFile.mode)

        textToWrite = ""
        for message in self.chatQueue.queue: # Get message history in string
            textToWrite = textToWrite + message.chat + "\n"

        self.chatHistoryFile.write(textToWrite)
        self.chatHistoryFile.flush()
