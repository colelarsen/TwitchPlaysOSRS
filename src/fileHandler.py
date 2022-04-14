import queue



def writeQueueToFile(filePath, queue):
    file1 = open(filePath,"w")
    textToWrite = ""

    for line in queue.queue:
        textToWrite = textToWrite + line + "\n"
        
    file1.write(textToWrite)
    file1.close()

def addLineToQueue(line, queue, source, author):
    if len(queue.queue) == 25:
        queue.get(0)
    
    queue.put(author + "(" + source + "): " + line)



