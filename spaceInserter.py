import time

resultList = []
subcandidatesList = []


def displayProgressBar(target, current):
    progress = round((current / target) * 50)
    bar = '\r'
    bar += "["
    for i in range(50):
        if i < progress:
            bar += '#'
        else:
            bar += '.'
    bar += ']'
    print(bar, current, "out of", target, "characters sorted", end='')


def removeNestings(l):
    output = ""
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            output += i
    return output


def findWord(str, recursionCount, candidatesList):
    # Finds all available words from str, saves it into availables
    strCharNum = 0
    # Select a letter from the raw string
    availables = []
    # Select a word from dictionary
    for dictWordNum in range(len(dictFile)):
        # Select a letter from the word
        for dictWordNumCharNum in range(len(dictFile[dictWordNum])):
            # Does the letters match?
            try:
                if str[strCharNum + dictWordNumCharNum] == dictFile[dictWordNum][dictWordNumCharNum]:
                    # Does all the letters match?
                    if dictWordNumCharNum + strCharNum + 1 == len(dictFile[dictWordNum]):
                        availables.append(dictFile[dictWordNum])
                        # Move on to the next word to check
                        break
                else:
                    break
            except:
                pass

    # Sort the list of availables, priortize longer words
    availables = sorted(availables, key=len, reverse=True)

    # Start recursion
    # if there are no availables, terminate this branch
    if len(availables) == 0:
        print("Error: no matches, check input. Does it contain non-letter characters?")

    for i in availables:
        subcandidatesList.append(i)

        # if recursion has finished the entire raw input, return true to end recursion
        if len(str) == len(i):
            resultList.extend(subcandidatesList)
            displayProgressBar(len(rawStr), len(rawStr))
            return True

        # Trigger the next recursion, if it returns true, return true to continue ending
        try:
            recursionCount += 1
            if recursionCount == 3:
                recursionCount -= 1
                candidatesList.append(list(subcandidatesList))
                return False

            if findWord(str[-len(str) + len(i):], recursionCount, candidatesList):
                return True

            recursionCount -= 1
            subcandidatesList.pop()
        except:
            pass

        try:
            subcandidatesList.pop()
        except:
            pass

    # If 3-length-tree is completed, compare & continue
    if recursionCount == 0:
        candidatesListCharCount = []
        # print(sorted(candidatesList, reverse=True))
        for i in candidatesList:
            candidatesListCharCount.append(len(removeNestings(i)))

        displayProgressBar(len(rawStr), len(rawStr) - len(str))
        resultList.append(
            candidatesList[candidatesListCharCount.index(max(candidatesListCharCount))][0])
        findWord(str[-len(str) + len(candidatesList[candidatesListCharCount.index(max(candidatesListCharCount))][0]):],
                 0, [])

    return False


dictionaryDir = "dictionary.txt"

rawStr = input("Enter your string here\n\n")
print('\n')

# Remove all spaces and convert to upper case for dictionary processing
rawStr = rawStr.upper().replace(" ", "")

file = open(dictionaryDir, "r")
dictFile = file.read().upper()
file.close()
dictFile = dictFile.splitlines(False)

while True:
    resultList = []
    subcandidatesList = []
    timer = time.time()

    findWord(rawStr, 0, [])

    timer = time.time() - timer

    print('\n')
    print(" ".join(resultList))
    print("\nThat took", round(timer, 2), "seconds")

    file = open(dictionaryDir, "r")
    dictFile = file.read().upper()
    file.close()
    dictFile = dictFile.splitlines(False)

    if input("Continue? (Y/n)") is "n":
        break

    while (True):
        word = input("Add a word to dictionary?\n").upper().replace(" ", "")
        if word is "":
            break
        else:
            dictFile.append(word)

    while (True):
        word = input("Remove a word from dictionary?\n").upper().replace(" ", "")
        if word is "":
            break
        else:
            dictFile.remove(word)

    file = open(dictionaryDir, "w")
    file.write('\n'.join(dictFile))
    file.close()
