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

def addPretext(lines, icon, baseURL, subURL):
    modified_lines = []
    currMdSubheading = ""
    currSubCat = ""
    currSubSubCat = ""

    for line in lines:
        if line.startswith("#"): #Title Lines
            if not subURL=="storage":
                if line.startswith("# ►"):
                    currMdSubheading = "#" + line.replace("# ►", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("# ►", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("## ▷"):
                    if not subURL=="non-english": #Because non-eng section has multiple subsubcats with same names
                        currMdSubheading = "#" + line.replace("## ▷", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("## ▷", "").strip() + " "
            elif subURL=="storage":
                if line.startswith("## "):
                    currMdSubheading = "#" + line.replace("## ", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("## ", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("### "):
                    currMdSubheading = "#" + line.replace("### ", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("### ", "").strip() + " "

            # Remove links from subcategory titles (because the screw the format)
            if 'http' in currSubCat: currSubCat = ''
            if 'http' in currSubSubCat: currSubSubCat = ''

        elif any(char.isalpha() for char in line): #If line has content
            preText = f"[{icon}{currSubCat}{currSubSubCat}]({baseURL}{subURL}{currMdSubheading}) ► "
            if line.startswith("* "): line = line[2:]
            modified_lines.append(preText + line)

    return modified_lines

def dlWikiChunk(fileName, icon, redditSubURL):
    pagesDevSiteSubURL = fileName.replace(".md", "").lower()
    subURL = pagesDevSiteSubURL
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
    redditBaseURL = "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/"
    pagesDevSiteBaseURL = "https://fmhy.pages.dev/"
    baseURL = pagesDevSiteBaseURL
    lines = addPretext(lines, icon, baseURL, subURL)

    return lines

def cleanLineForSearchMatchChecks(line):
    return line.replace('https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/', '/').replace('https://fmhy.pages.dev/', '/')

def alternativeWikiIndexing():
    wikiChunks = [
        dlWikiChunk("VideoPiracyGuide.md", "📺", "video"),
        dlWikiChunk("AI.md", "🤖", "ai"),
        dlWikiChunk("Android-iOSGuide.md", "📱", "android"),
        dlWikiChunk("AudioPiracyGuide.md", "🎵", "audio"),
        dlWikiChunk("DownloadPiracyGuide.md", "💾", "download"),
        dlWikiChunk("EDUPiracyGuide.md", "🧠", "edu"),
        dlWikiChunk("GamingPiracyGuide.md", "🎮", "games"),
        dlWikiChunk("AdblockVPNGuide.md", "📛", "adblock-vpn-privacy"),
        dlWikiChunk("TOOLSGuide.md", "🔧", "tools-misc"),
        dlWikiChunk("MISCGuide.md", "📂", "misc"),
        dlWikiChunk("ReadingPiracyGuide.md", "📗", "reading"),
        dlWikiChunk("TorrentPiracyGuide.md", "🌀", "torrent"),
        dlWikiChunk("img-tools.md", "📷", "img-tools"),
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

def removeEmptyStringsFromList(stringList):
    return [string for string in stringList if string != '']

def checkMultiWordQueryContainedExactlyInLine(line, searchQuery):
    if len(searchQuery.split(' ')) <= 1:
        return False
    return (searchQuery.lower() in line.lower())

def moveExactMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for element in myList:
        if checkMultiWordQueryContainedExactlyInLine(element, searchQuery):
            bumped.append(element)
        else:
            notBumped.append(element)
    return (bumped + notBumped)

def checkList1isInList2(list1, list2):
    for element in list1:
        if element not in list2:
            return False
    return True

def checkWordForWordMatch(line, searchQuery):
    lineWords = removeEmptyStringsFromList( line.lower().replace('[', ' ').replace(']', ' ').split(' ') )
    lineWords = [element.strip() for element in lineWords] #doesnt work on streamlit without this line even though it works locally
    searchQueryWords = removeEmptyStringsFromList( searchQuery.lower().split(' ') )
    return checkList1isInList2(searchQueryWords, lineWords)

def checkWordForWordMatchCaseSensitive(line, searchQuery):
    lineWords = removeEmptyStringsFromList( line.replace('[', ' ').replace(']', ' ').split(' ') )
    lineWords = [element.strip() for element in lineWords] #doesnt work on streamlit without this line even though it works locally
    searchQueryWords = removeEmptyStringsFromList( searchQuery.split(' ') )
    return checkList1isInList2(searchQueryWords, lineWords)

def moveBetterMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for element in myList:
        if checkWordForWordMatch(element, searchQuery):
            bumped.append(element)
        else:
            notBumped.append(element)
    return (bumped + notBumped)

def getOnlyFullWordMatches(myList, searchQuery):
    bumped = []
    for element in myList:
        if checkWordForWordMatch(element, searchQuery):
            bumped.append(element)
    return bumped

def getOnlyFullWordMatchesCaseSensitive(myList, searchQuery):
    bumped = []
    for element in myList:
        if checkWordForWordMatchCaseSensitive(element, searchQuery):
            bumped.append(element)
    return bumped

def getLinesThatContainAllWords(lineList, searchQuery):
    words = removeEmptyStringsFromList( searchQuery.lower().split(' ') )
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
    if len(searchQuery)<=2 or (searchQuery==searchQuery.upper() and len(searchQuery)<=5):
        return getOnlyFullWordMatches(lineList, searchQuery)
    else:
        return getLinesThatContainAllWords(lineList, searchQuery)

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

def addNumberingToStringList(string_list):
    for i in range(len(string_list)):
        string_list[i] = f"{i + 1}- {string_list[i]}"
    return string_list

def doASearch(searchInput):

    #intro to the search results
    myFilterWords = removeEmptyStringsFromList( searchInput.lower().split(' ') )
    print("Looking for lines that contain all of these words:")
    print(myFilterWords)

    #main results
    myLineList = lineList
    linesFoundPrev = filterLines(myLineList, searchInput)

    #limit result list
    if len(linesFoundPrev) > 300:
        print("Too many results (" + str(len(linesFoundPrev)) + "). Showing only full-word matches.")
        linesFoundPrev = getOnlyFullWordMatches(linesFoundPrev, searchInput)

    #rank results
    #linesFoundPrev = moveExactMatchesToFront(linesFoundPrev, searchInput)
    linesFoundPrev = moveBetterMatchesToFront(linesFoundPrev, searchInput)

    #separate title lines
    linesFoundAll = filterOutTitleLines(linesFoundPrev)
    linesFound = linesFoundAll[0]
    linesFound = addNumberingToStringList(linesFound)
    sectionTitleList = linesFoundAll[1]

    #reverse list for terminal
    linesFound.reverse()

    #check for coloring
    if coloring == True:
        linesFoundColored = colorLinesFound(linesFound, myFilterWords)
        textToPrint = "\n\n".join(linesFoundColored)
    else:
        textToPrint = "\n\n".join(linesFound)

    # print main results
    print("Printing " + str(len(linesFound)) + " search results:\n")
    print(textToPrint)
    print("\nSearch ended with " + str(len(linesFound)) + " results found.\n")

    #title section results
    if len(sectionTitleList)>0:
        print("Also there are these section titles: ")
        print("\n".join(sectionTitleList))



def searchLoop():
    print("STARTING NEW SEARCH...\n")

    searchInput = input("Type a search string:     ")
    if searchInput == "exit" or searchInput == "q" or searchInput == "":
        print("The script is closing...")
        return

    doASearch(searchInput.strip())
    print("\n\n\n")
    searchLoop()



lineList = getAllLines()
print("Search examples: 'youtube frontend', 'streaming site', 'rare movies', 'userscripts'... You can also type 'exit' or nothing to close the script.\n")
searchLoop()
