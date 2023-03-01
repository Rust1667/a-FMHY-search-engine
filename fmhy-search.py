import requests

#enable text coloring only if the requirements are met
coloring = True
try:
    from termcolor import colored
    import colorama
    colorama.init()
except:
    coloring = False



def getAllLines():
    try:
        #First, try to get it from the local single-page file
        print("Loading FMHY from local single-page...")
        with open('single-page', 'r') as f:
            data = f.read()
        print("Loaded.\n")
    except:
        print("Local single-page file not found.")
        #If that fails, try to get it from Github
        print("Loading FMHY single-page file from Github...")
        response1 = requests.get("https://raw.githubusercontent.com/nbats/FMHYedit/main/single-page")
        print("Loaded.\n")
        data = response1.text

    lines = data.split('\n')
    return lines


def checkMultiWordQueryContainedExactlyInLine(line, searchQuery):
    if len(searchQuery.split(' ')) <= 1: 
        return False
    return (searchQuery.lower() in line.lower())

def moveExactMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for i in range(len(myList)):
        if checkMultiWordQueryContainedExactlyInLine(myList[i], searchQuery):
            bumped.append(myList[i])
        else:
            notBumped.append(myList[i])
    return (bumped + notBumped)

def checkList1isInList2(list1, list2):
    for element in list1:
        if element not in list2:
            return False
    return True

def checkWordForWordMatch(line, searchQuery):
    lineWords = line.lower().replace('[', ' ').replace(']', ' ').split(' ')
    searchQueryWords = searchQuery.lower().split(' ')
    return checkList1isInList2(searchQueryWords, lineWords)

def moveBetterMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for i in range(len(myList)):
        if checkWordForWordMatch(myList[i], searchQuery):
            bumped.append(myList[i])
        else:
            notBumped.append(myList[i])
    return (bumped + notBumped)

def getOnlyFullWordMatches(myList, searchQuery):
    bumped = []
    for i in range(len(myList)):
        if checkWordForWordMatch(myList[i], searchQuery):
            bumped.append(myList[i])
    return bumped

def getLinesThatContainAllWords(lineList, filterWords):
    lineListFiltered = [line for line in lineList if all(
        word.lower() in line.lower() for word in filterWords
    )]
    return lineListFiltered

def filterLines(lineList, searchQuery):
    filterWords = searchQuery.lower().split(' ')
    lineListFiltered = getLinesThatContainAllWords(lineList, filterWords)
    return lineListFiltered

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

    #make sure the input is right before continuing
    if searchInput == "exit" or searchInput == "":
        print("The script is closing...")
        return

    #intro to the search results
    myFilterWords = searchInput.lower().split(' ')
    print("Looking for lines that contain all of these words:")
    print(myFilterWords)

    #main results
    myLineList = lineList
    linesFoundPrev = filterLines(myLineList, searchInput)

    if len(linesFoundPrev)>50:
        print("Too many results (" + str(len(linesFoundPrev)) + "). Showing only full-word matches.")
        linesFoundPrev = getOnlyFullWordMatches(linesFoundPrev, searchInput)

    linesFoundPrev = moveExactMatchesToFront(linesFoundPrev, searchInput)
    linesFoundPrev = moveBetterMatchesToFront(linesFoundPrev, searchInput)
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
print("Search examples: 'youtube frontend', 'streaming site', 'rare movies', 'userscripts'... You can also type 'exit' or nothing to close the script.\n")
doASearch()
