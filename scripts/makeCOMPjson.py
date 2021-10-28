from math import log


def interest_to_COMP_capital(interest):
    ''' Apply early user distribution formula to
        determine COMP for the given earned interest:
        COMP = minCOMP + (interest-minInterest)/scaleFactor'''
    minQualifyingInterest = 1.0
    minCOMP = 10.0
    scaleFactor = 100.0
    if interest < minQualifyingInterest:
        return 0
    return minCOMP + (interest-minQualifyingInterest)/scaleFactor

def interest_to_COMP_logcapital(interest):
    ''' Apply early user distribution formula to
        determine COMP for the given earned interest:
        COMP = minCOMP + log_base(interest/scaleFactor)'''

    minQualifyingInterest = 1.0
    minCOMP = 5.0
    base    = 1.05
    scaleFactor = 1.0
    if interest < minQualifyingInterest:
        return 0
    return minCOMP + log(interest/scaleFactor,base)

jsonFilename = 'EarlyUserCOMP.json'
with open(jsonFilename,'w') as jsonFile:
    jsonFile.write('{\n')
    csvFilename = 'TotalUSDInterestByAddress-JuneCutoff.csv'
    firstCOMP = True # True until first line awarding COMP is written
    cumulativeCOMP = 0
    with open(csvFilename,'r') as csvFile:
        lineCounter = 0
        for line in csvFile:
            if lineCounter == 0:
                lineCounter += 1
                continue
            address  = str(line.split(',')[0])
            interest = float(line.split(',')[1])
            COMP = interest_to_COMP_capital(interest)
            cumulativeCOMP += COMP
            if COMP > 0:
                if firstCOMP:
                    firstCOMP = False
                    jsonFile.write('  "' + address + '": ' + str(COMP))
                else:
                    jsonFile.write(",\n" + '  "' + address + '": ' + str(COMP))
            lineCounter += 1
    csvFile.close()
    jsonFile.write('\n}')
jsonFile.close()
print("Cumulative COMP = " + str(cumulativeCOMP))
