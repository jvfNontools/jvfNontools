#Copyright 2018 Jim Van Fleet

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

class SearchAnnoFile:

            
    def getLinkData(self, annoParse, annoLink, symData, machine):
        annoParseNames = []
        for ii in annoParse:
            annoParseNames.append(ii[1])
            annoParseNames.append(ii[3])
        linkAnnoParse = []
        for lnk in annoLink:
            lnkName = self.findName(lnk[3], symData, machine)
            try:
                linkAnno = annoParseNames.index(lnkName)
            except:
                try:
                    linkAnno = annoParseNames.index(lnk[3])
                except:
#                   Ignore Notfound Name
#                   generally from branch table
#                    print(lnkName, lnk[3])
#                    print("What to do?")
                    continue
            linkAnno = int(linkAnno/2)
            pdata = annoParse[linkAnno]
            annoParse.append([pdata[0], pdata[1], lnk[2], lnk[1]])
        annoParse.append(linkAnnoParse)
        return annoParse

    def findName(self, addrAsm0, symData, machine):
        addrAsm = addrAsm0.lstrip("0")
        try:
            whx = symData.index(addrAsm)
        except:
            if machine == "x86_64":
#                print(addrAsm)
                # if it aint there it aint there
                return "NotFound_" + addrAsm
            if addrAsm[-1] == "0":
                tryAddr = addrAsm[:-1] + "8"
            elif addrAsm[-1] == "4":
                intrm = int(addrAsm, 16)
                intrm -= 8
                tryAddr = '{:x}'.format(intrm)
            elif addrAsm[-1] == "c":
                tryAddr = addrAsm[:-2] + "4"
            else:
                tryAddr = addrAsm[:-1] + "0"
            try:
                whx = symData.index(tryAddr)
            except:
                 return "NotFound_" + addrAsm0
#        print("whx", addrAsm, symData[whx-1], symData[whx])
        return symData[whx-1]

    def doParse(self, openFile, symData, machine):
        annoParse = []
        annoLink = []
        self.TotalTicks = 0
        sampb = "h->nr_samples:"
        disAssb = "Disassembly of section"
        parab = "("
        manglHead = "_ZN"
        # for x86_64 vs power (option with uname default)
        if machine == "power":
            linkb = " bl "
        else:
            linkb = " callq "
        threshHold = "0.01"
        wdCountThresh = 2
        with open(openFile) as annoFile:
            wdCount = 0
            for line in annoFile:
                splWords = line.split()
                if (line.find(sampb) != -1):
                    sampCount = splWords[-1]
                    self.TotalTicks += int(sampCount)
                    wdCount = 1
                elif line.find(disAssb) != -1:
                    if wdCount == 0:
                        continue
                    line = annoFile.readline()  # blank line
                    line = annoFile.readline()  
                    lineSpl = line.split()
                    wdCount = 2
                    namEntry = self.findName(lineSpl[1], symData, machine)
                    addrAsm = lineSpl[1].lstrip("0")
                    line = annoFile.readline()
                    if line.find(manglHead) != -1:
                        lineSpl = line.split()
                        namMangl = lineSpl[1][:-3]
                    else:
                        namMangl = namEntry
                elif line.find(linkb) != -1:
                    lineSpl = line.split()
                    if lineSpl[0] <= threshHold:
                        continue 
                    if lineSpl[4].find("0x") != -1:
                        callAdr = lineSpl[4][2:]
                    else:
                        callAdr = lineSpl[4]
                    try:
                        tx = lineSpl[0].index(".")
                        callCount = int((float(lineSpl[0]) * float(sampCount))/100.0)
                        if callCount <= 0:
                            callCount = 1
                    except:
                        callCount = int(lineSpl[0])
                    annoLink.append([int(sampCount), namEntry, int(callCount),  callAdr])

                else:
                    continue
                if wdCountThresh != wdCount:
                    continue
                wdCount = 0
                annoParse.append([int(sampCount), namEntry, -1, addrAsm])

        annoParse = self.getLinkData(annoParse, annoLink, symData, machine)
        annoParse.sort(reverse=True)
#        for ii in annoParse:
#            print(ii)
        return annoParse

    def __init__(self, openFile, symData, machine):
        self.annoData = self.doParse(openFile, symData, machine)
