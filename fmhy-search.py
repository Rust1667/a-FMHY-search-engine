import requests

#enable text coloring only if the requirements are met
coloring = True
try:
    from termcolor import colored
    import platform
    if platform.system() == 'Windows':
        import colorama
        colorama.init()
except:
    coloring = False


def splitSentenceIntoWords(searchInput):
    searchInput = searchInput.lower()
    searchWords = searchInput.split(' ')
    return searchWords

def getAllLines():
    print("Loading FMHY single-page file from Github...")
    response1 = requests.get("https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page")
    print("Loaded.\n")

    data = response1.text
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
    sectionTitleList = []
    for line in lineList:
        if line[0] != "#":
            filteredList.append(line)
        else:
            sectionTitleList.append(line)
    return [filteredList, sectionTitleList]


def highlightWord(sentence, word):
    return sentence.replace(word, colored(word,'red'))

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
    #intro
    print("STARTING NEW SEARCH...\n")
    searchInput = input("Type a search string:     ")
    myFilterWords = splitSentenceIntoWords(searchInput)
    print("Looking for lines that contain all of these words:")
    print(myFilterWords)

    #main results
    myLineList = lineList
    linesFoundPrev = filterLines(lineList=myLineList, filterWords=myFilterWords)
    linesFoundAll = filterOutTitleLines(linesFoundPrev)
    linesFound = linesFoundAll[0]
    sectionTitleList = linesFoundAll[1]
    if coloring == True:
        linesFoundColored = colorLinesFound(linesFound, myFilterWords)
        textToPrint = "\n\n".join(linesFoundColored)
    else:
        textToPrint = "\n\n".join(linesFound)
    print("Printing " + str(len(linesFound)) + " search results:\n")
    print(textToPrint)
    print("\nSearch ended with " + str(len(linesFound)) + " results found.\n")

    #title section results
    if len(sectionTitleList)>0:
        print("Also there are these section titles: ")
        print("\n".join(sectionTitleList))
    
    #repeat the search
    print("\n\n\n")   
    doASearch()

lineList = getAllLines()
print("Search examples: 'youtube frontend', 'streaming site', 'rare movies', 'userscripts'...\n")
doASearch()
