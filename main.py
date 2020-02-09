import urllib.request
import urllib.error
import timeit
import requests
import csv
import http
CLASS_MW_LEN = 11
HEADER_WORD_LEN = 14

'''
currently it wont be able to search merriam webster for shames, for example. It'll go to the shame page. I can have it
return the root page + 1 or just the root page, but there's no logic. Shame = 1, Shames = 1, Pace = 1, Paces = 2. 
Current plan is to just get all the words which themselves are on webster, i can always read through all the words
in my 450k list to see if any have roots in my output csv file at a later date applying some sort of logic to them
'''

def openPage(word):
    try:
        fp = urllib.request.urlopen("https://www.merriam-webster.com/dictionary/" + word.lower())
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return mystr
    except urllib.error.HTTPError:
        return -1

def openPageRequests(word):
    if(requests.head("https://www.merriam-webster.com/dictionary/" + word.lower()).status_code == 200):

        fp = urllib.request.urlopen("https://www.merriam-webster.com/dictionary/" + word.lower())
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return mystr

    return -1

def extractValueFromHtml(string):
    value = ""
    for c in string:
        if c == '<':
            break
        value += c
    return value


def doesHeadWordEqualSearch(html,word):
    headerpos = html.find("class=\"hword\"")
    desiredString = html[headerpos + HEADER_WORD_LEN: headerpos + 60]

    if extractValueFromHtml(desiredString) == word:
        return True
    return False



def numSyllables(word):
    html = openPageRequests(word)

    if html == -1:
        return -1
    if not doesHeadWordEqualSearch(html, word):

        return -1

    syllablepos = html.find("class=\"mw\"")
    if syllablepos == -1:

        return -1

    reducedHtml = html[syllablepos + CLASS_MW_LEN: syllablepos + 200]
    reducedHtml = extractValueFromHtml(reducedHtml)
    syllablecount = 0
    lastCharWasSyllable = False
    hasReachedWord = False
    randomStartChars = ['(', ')']
    syllabicIdentifiers = ['-', '.', 'ˌ', 'ˈ', '¦']
    for c in reducedHtml:
        if not hasReachedWord:
            if c not in randomStartChars  and c not in syllabicIdentifiers:
                hasReachedWord = True
            continue
        #this will consume the first consonant of each syllable but even if the syllable
        #is 1 consonant long it's fine
        if lastCharWasSyllable:
            if c not in syllabicIdentifiers:
                lastCharWasSyllable = False
            continue

        if c == ',' or c == '\\' or c == '<':
            break
        if c in syllabicIdentifiers:
            syllablecount += 1
            lastCharWasSyllable = True

    return syllablecount + 1


def writeToFile(fileName, data):
    with open(fileName, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


print(numSyllables("ablution"))
#TODO ALSO COUNT SYLLABLES IN THE HYPHENATED VERSION ON MERRIAM, its probably a lot easier
#flip me, also save the syllabified version as a 3rd column
saveSize = 50
outList = []
outName = "wordsyllables.csv"
with open("words.txt", "r") as ins:
    i = 0
    for line in ins:
        line = line.lower()
        line = line.strip()
        syllables = numSyllables(line)
        print(line, syllables)
        if syllables != -1:
            outList.append([line, syllables])
        if len(outList) % saveSize == 0 and len(outList) != 0:
            writeToFile(outName, outList)
        i += 1






