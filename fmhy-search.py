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


#----------------base64 page processing------------
import base64
import re

doBase64Decoding = True

def fix_base64_string(encoded_string):
    missing_padding = len(encoded_string) % 4
    if missing_padding != 0:
        encoded_string += '=' * (4 - missing_padding)
    return encoded_string

def decode_base64_in_backticks(input_string):
    def base64_decode(match):
        encoded_data = match.group(0)[1:-1]  # Extract content within backticks
        decoded_bytes = base64.b64decode( fix_base64_string(encoded_data) )
        try:
            return decoded_bytes.decode()
        except:
            print(f"Failed to decode base64 string: {encoded_data}")
            return encoded_data

    pattern = r"`[^`]+`"  # Regex pattern to find substrings within backticks
    decoded_string = re.sub(pattern, base64_decode, input_string)
    return decoded_string

def remove_empty_lines(text):
    lines = text.split('\n')  # Split the text into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Filter out empty lines
    return '\n'.join(non_empty_lines)  # Join non-empty lines back together

def extract_base64_sections(base64_page):
    sections = base64_page.split("***")  # Split the input string by "***" to get sections
    formatted_sections = []
    for section in sections:
        formatted_section = remove_empty_lines( section.strip().replace("#### ", "").replace("\n\n", " - ").replace("\n", ", ") )
        if doBase64Decoding: formatted_section = decode_base64_in_backticks(formatted_section)
        formatted_section = '[🔑Base64](https://rentry.co/FMHYBase64) ► ' + formatted_section
        formatted_sections.append(formatted_section)
    lines = formatted_sections
    return lines
#----------------</end>base64 page processing------------



def dlWikiChunk(fileName, icon, redditSubURL):

    #first, try to get the chunk locally
    try:
        #First, try to get it from the local file
        print("Loading " + fileName + " from local file...")
        with open(fileName.lower(), 'r') as f:
            page = f.read()
        print("Loaded.\n")
    #if not available locally, download the chunk
    except:
        if not fileName=='base64.md':
            print("Local file not found. Downloading " + fileName + " from Github...")
            page = requests.get("https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/" + fileName.lower()).text
        elif fileName=='base64.md':
            print("Local file not found. Downloading rentry.co/FMHYBase64...")
            page = requests.get("https://rentry.co/FMHYBase64/raw").text.replace("\r", "")
        print("Downloaded")

    #add a pretext
    redditBaseURL = "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/"
    siteBaseURL = "https://fmhy.net/"
    if not fileName=='base64.md':
        pagesDevSiteSubURL = fileName.replace(".md", "").lower()
        subURL = pagesDevSiteSubURL
        lines = page.split('\n')
        lines = addPretext(lines, icon, siteBaseURL, subURL)
    elif fileName=='base64.md':
        lines = extract_base64_sections(page)

    return lines

def cleanLineForSearchMatchChecks(line):
    siteBaseURL = "https://fmhy.net/"
    redditBaseURL = "https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/"
    return line.replace(redditBaseURL, '/').replace(siteBaseURL, '/')

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
        dlWikiChunk("System-Tools.md", "💻", "system-tools"),
        dlWikiChunk("File-Tools.md", "🗃️", "file-tools"),
        dlWikiChunk("Internet-Tools.md", "🔗", "internet-tools"),
        dlWikiChunk("Social-Media-Tools.md", "💬", "social-media"),
        dlWikiChunk("Text-Tools.md", "📝", "text-tools"),
        dlWikiChunk("Video-Tools.md", "📼", "video-tools"),
        dlWikiChunk("MISCGuide.md", "📂", "misc"),
        dlWikiChunk("ReadingPiracyGuide.md", "📗", "reading"),
        dlWikiChunk("TorrentPiracyGuide.md", "🌀", "torrent"),
        dlWikiChunk("img-tools.md", "📷", "img-tools"),
        dlWikiChunk("gaming-tools.md", "👾", "gaming-tools"),
        dlWikiChunk("LinuxGuide.md", "🐧🍏", "linux"),
        dlWikiChunk("DEVTools.md", "🖥️", "dev-tools"),
        dlWikiChunk("Non-English.md", "🌏", "non-eng"),
        dlWikiChunk("STORAGE.md", "🗄️", "storage"),
        dlWikiChunk("base64.md", "🔑", "base64"),
        dlWikiChunk("NSFWPiracy.md", "🌶", "https://saidit.net/s/freemediafuckyeah/wiki/index")
    ]
    return [item for sublist in wikiChunks for item in sublist] #Flatten a <list of lists of strings> into a <list of strings>
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
        response1 = requests.get("https://api.fmhy.net/single-page")
        print("Loaded.\n")
        data = response1.text
    lines = data.split('\n')
    return lines

def getAllLines():
    return alternativeWikiIndexing()

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
