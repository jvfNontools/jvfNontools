#!/usr/bin/python3
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

import sys
# import cxxfilt
# from demangler import demangle
# seems that neither demangler nor cxxfilt work on phython 3
# x86_64 has only mangled names -- will need to demangle after formatting

class doFormatOut:

    def __init__(self, annoParse, outFile, TotalTicks, machine):
        self.annoData = self.formatOutput(annoParse, outFile, TotalTicks, machine)

    def formatOutput(self, annoParse, outFile, TotalTicks, machine):
        curr = " "
        datEntry = []
        if outFile != "sys.stdout":
            prtOutFile = open(outFile, 'w')
        else:
            prtOutFile = sys.stdout
        toPrt = '{}  {:-8} '.format("Total Events ", TotalTicks)
        prtOutFile.write(toPrt+'\n')
        dat = annoParse[0]
        curr = dat[1]
        for dat in annoParse:
            len0 = len(dat)
            if len0 == 0:
                continue
            if curr == dat[1]:
                # sub count, sub name, call count, caller
                datEntry.append(dat)
            else:
                callers = datEntry
                callers.sort(reverse=True)
                lenCall = len(callers)
                prtCall = callers[lenCall-1]
                perCent = prtCall[0] / TotalTicks
                toPrt = '{:2.2%}  {:-8} {}'.format(perCent, prtCall[0], prtCall[1])
                prtOutFile.write(toPrt+'\n')
                for prtCall in callers:
                    if prtCall[2] == -1:
                        continue
#                    if prtCall[2] > 100: 
#                        revCount = int(prtCall[2]/100)
#                    else:
#                        revCount =1
                    toPrt = '{:6} {:-8} {}'.format(" ", prtCall[2], prtCall[3])
                    prtOutFile.write(toPrt+'\n')
                curr = dat[1]
                datEntry = []
                datEntry.append(dat)
        prtOutFile.close()


