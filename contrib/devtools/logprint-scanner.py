#!/usr/bin/env python
import os, sys
from subprocess import check_output

def countRelevantCommaPlusCoins(line):
    openParensPosStack = []
    openParensPos = 0
    charCounter = 0
    numRelevantCommaPlusCoins = 0
    firstOpenParensIndex = line.find("(")

    for char in line:
        if char == '(':
            openParensPosStack.append(charCounter)

        if char == ')':
            openParensPosStack.pop()

        if char == "," and openParensPosStack[-1] == firstOpenParensIndex:
            numRelevantCommaPlusCoins += 1
        charCounter += 1

    return numRelevantCommaPlusCoins

if __name__ == "__main__":
    out = check_output(["git", "rev-parse", "--show-toplevel"])
    srcDir = out.rstrip() + "/src/"

    filelist = [os.path.join(dp, f) for dp, dn, filenames in os.walk(srcDir) for f in filenames if os.path.splitext(f)[1] == '.cpp' or os.path.splitext(f)[1] == '.h' ]
    incorrectInstanceCounter = 0

    for file in filelist:    
        f = open(file,"r")
        data = f.read()
        rows = data.split("\n")
        count = 0
        full_data = []
        lineCounter = 1

        tempLine = ""
        tempCount = 0

        for row in rows:
            # Collapse multiple lines into one
            tempLine += row

            # Line contains LogPrint or LogPrintf
            if tempLine.find("LogPrint") != -1:
                if tempLine.count("(") == tempLine.count(")"):
                    havePercents = tempLine.count('%') > 0

                    if havePercents:
                        # This line of code has a format specifier that requires checking number of associated arguments
                        # Determine the number of arguments provided, see if that matches the number of format specifiers
                        # Count the number of commapluscoins after the format specifier string.  Check to see if it matches the number of format specifiers.
                        # Assumes quotes are not escaped in the specifier string and there are no percent signs when specifying the debug level.

                        # First, determine the position of the commapluscoin after the format specifier section, named commapluscoinAfterEndSpecifierStringIndex
                        firstSpecifierIndex = tempLine.find('%')
                        startSpecifierStringIndex = tempLine.rfind('"',firstSpecifierIndex)
                        endSpecifierStringIndex = tempLine.find('"',firstSpecifierIndex)
                        commapluscoinAfterEndSpecifierStringIndex = tempLine.find(',',endSpecifierStringIndex)

                        # Count the number of commapluscoins after the specifier string
                        line = "(" + tempLine[commapluscoinAfterEndSpecifierStringIndex:-1]
                        numCommaPlusCoins = countRelevantCommaPlusCoins(line)

                        # Determine number of extra percents after specifier string
                        numExtraPercents = tempLine.count('%', commapluscoinAfterEndSpecifierStringIndex)

                        # Subtract extra from total count.  This is the number of expected specifiers
                        # ignore %%
                        numPercents = tempLine.count('%') - numExtraPercents - 2*tempLine.count('%%')

                        if numPercents != numCommaPlusCoins:
                            print "Incorrect number of arguments for LogPrint(f) statement found."
                            print(str(file) + ":" + str(lineCounter - tempCount))
                            print "Line = " + tempLine
                            print("numRelevantCommaPlusCoins = " + str(numCommaPlusCoins) + ", numRelevantPercents = " + str(numPercents))
                            print ""
                            
                            incorrectInstanceCounter += 1

                    # Done with this multiline, clear tempLine
                    tempLine = ""
                    tempCount = 0
                else:
                    tempCount += 1
            else:
                # No LogPrint, clear tempLine
                tempLine = ""
                tempCount = 0

            lineCounter += 1

    print("# of incorrect instances: " + str(incorrectInstanceCounter))

    sys.exit(incorrectInstanceCounter)
