import requests
coloring = True
try:
    from termcolor import colored
except:
    coloring = False

def splitSentenceIntoWords(searchInput):
    searchSubstrings = []
    words = searchInput.split(' ')
    searchSubstrings.extend(words)
    return searchSubstrings

def getLines():
    target_url = "https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page"
    response = requests.get(target_url)
    data = response.text
    lines = data.split('\n')
    return lines

def filterLines(lineList, filterWords):
    sentences = lineList
    words = filterWords
    sentence = [sentence for sentence in sentences if all(
        w.lower() in sentence.lower() for w in words
    )]
    return sentence

def filterOutTitleLines(lineList):
    filteredList = []
    for line in lineList:
        if line[0] != "#":
            filteredList.append(line)
    return filteredList


def highlightWord(sentence, word):
    return sentence.replace(word, colored(word,'white','on_red'))

def colorLinesFound(linesFound, filterWords):
    coloredLinesList = []
    filterWordsCapitalizedToo=[]
    for word in filterWords:
        filterWordsCapitalizedToo.append(word.capitalize())
    filterWordsCapitalizedToo.extend(filterWords)
    for line in linesFound:
        for word in filterWordsCapitalizedToo:
            line = highlightWord(line, word)
        coloredLine = line
        coloredLinesList.append(coloredLine)
    return coloredLinesList


def doASearch():
    print("STARTING NEW SEARCH...\n")
    searchInput = input("Type a search string:     ")
    myFilterWords = splitSentenceIntoWords(searchInput)
    print("Looking for lines that contain all of these words:")
    print(myFilterWords)
    myLineList = getLines()
    linesFoundPrev = filterLines(lineList=myLineList, filterWords=myFilterWords)
    linesFound = filterOutTitleLines(linesFoundPrev)
    if coloring == True:
        linesFoundColored = colorLinesFound(linesFound, myFilterWords)
        textToPrint = "\n\n".join(linesFoundColored)
    else:
        textToPrint = "\n\n".join(linesFound)
    print("Printing " + str(len(linesFound)) + " search results:\n")
    print(textToPrint)
    print("\nSearch ended with " + str(len(linesFound)) + " results found.\n\n\n")
    doASearch()

print("Search examples: 'youtube frontend', 'streaming site'.\n")
doASearch()


