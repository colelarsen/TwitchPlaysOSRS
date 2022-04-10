import re
def getFirstNumber(line):
    number = re.search(r"[\d]+", line)
    if number:
        number = int(line[number.start():number.end()])
    return number