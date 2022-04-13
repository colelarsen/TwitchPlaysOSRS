def writeQueueToFile(filePath, queue):
    file1 = open(filePath,"w")

    for line in queue:
        file1.write(line + "\n")
    
    file1.close()