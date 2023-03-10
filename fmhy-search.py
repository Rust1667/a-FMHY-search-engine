import requests

#enable text coloring only if the requirements are met
coloring = True
try:
    from termcolor import colored
    import colorama
    colorama.init()
except:
    coloring = False


#----------------Alt Indexing------------
doAltIndexing = True

def addPretext(lines, preText):
    for i in range(len(lines)):
        lines[i] = preText + lines[i]
    return lines

def dlWikiChunk(fileName, icon, subURL):
    #first, try to get the chunk locally
    try:
        #First, try to get it from the local file
        print("Loading " + fileName + " from local file...")
        with open(fileName, 'r') as f:
            data = f.read()
        print("Loaded.\n")
        lines = data.split('\n')
    #if not available locally, download the chunk from github
    except:
        print("Local file not found. Downloading " + fileName + "from Github...")
        lines = requests.get("https://raw.githubusercontent.com/nbats/FMHYedit/main/" + fileName).text.split('\n')
        print("Downloaded")

    #add a pretext
    if not fileName=="NSFWPiracy.md":
        preText = "[" + icon + "](" + "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/" + subURL + ") "
    else:
        preText = "[" + icon + "](" + subURL + ") "
    preText = icon + " "
    lines = addPretext(lines, preText)
    
    return lines

def cleanLineForSearchMatchChecks(line):
    return line.replace('https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/', '/')

def alternativeWikiIndexing():
    wikiChunks = [
        dlWikiChunk("VideoPiracyGuide.md", "📺", "video"),
        dlWikiChunk("Android-iOSGuide.md", "📱", "android"),
        dlWikiChunk("AudioPiracyGuide.md", "🎵", "audio"),
        dlWikiChunk("DownloadPiracyGuide.md", "💾", "download"),
        dlWikiChunk("EDUPiracyGuide.md", "🧠", "edu"),
        dlWikiChunk("GamingPiracyGuide.md", "🎮", "games"),
        dlWikiChunk("Game-Tools.md", "🎮🔧", "game-tools"),
        dlWikiChunk("AdblockVPNGuide.md", "📛", "adblock-vpn-privacy"),
        dlWikiChunk("TOOLSGuide.md", "🔧", "tools-misc"),
        dlWikiChunk("MISCGuide.md", "📂", "misc"),
        dlWikiChunk("ReadingPiracyGuide.md", "📗", "reading"),
        dlWikiChunk("TorrentPiracyGuide.md", "🌀", "torrent"),
        dlWikiChunk("img-tools.md", "🖼️🔧", "img-tools"),
        dlWikiChunk("LinuxGuide.md", "🐧🍏", "linux"),
        dlWikiChunk("DEVTools.md", "🖥️", "dev-tools"),
        dlWikiChunk("Non-English.md", "🌏", "non-eng"),
        dlWikiChunk("STORAGE.md", "🗄️", "storage"),
        dlWikiChunk("NSFWPiracy.md", "🌶", "https://saidit.net/s/freemediafuckyeah/wiki/index")
    ]
    return [item for sublist in wikiChunks for item in sublist]
#--------------------------------


def standardWikiIndexing():
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

def getAllLines():
    if doAltIndexing:
        try:
            lines = alternativeWikiIndexing()
        except:
            lines = standardWikiIndexing()
    else:
        lines = standardWikiIndexing()
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

def getLinesThatContainAllWords(lineList, words):
    bumped = []
    for line in lineList:
        if doAltIndexing:
            lineModdedForChecking = cleanLineForSearchMatchChecks(line).lower()
        else:
            lineModdedForChecking = line.lower()
        for word in words:
            if word not in lineModdedForChecking:
                break
        else:
            bumped.append(line)
    return bumped

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
    filterWordsCapitalized=[]
    for word in filterWords:
        filterWordsCapitalized.append(word.capitalize())
    
    filterWordsAllCaps=[]
    for word in filterWords:
        filterWordsAllCaps.append(word.upper())

    filterWordsIncludingCaps = filterWords + filterWordsCapitalized + filterWordsAllCaps
    coloredLinesList = []
    for line in linesFound:
        for word in filterWordsIncludingCaps:
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

    if len(linesFoundPrev) > 300:
        print("Too many results (" + str(len(linesFoundPrev)) + "). Showing only full-word matches.")
        linesFoundPrev = getOnlyFullWordMatches(linesFoundPrev, searchInput)

    #rank results
    #linesFoundPrev = moveExactMatchesToFront(linesFoundPrev, searchInput)
    linesFoundPrev = moveBetterMatchesToFront(linesFoundPrev, searchInput)

    #separate title lines
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
