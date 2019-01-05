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

class DoFormat:
    def doPrint(self, verboseFlag, outFile, parseData, sysCallList):
        if outFile != "sys.stdout":
            prtOutFile = open(outFile, 'w')
        else:
            prtOutFile = sys.stdout
        c1 = "SVC"
        c0 = "SvcName"
        c2 = "TmStrt"
        c3 = "TmEnd"
        c4 = "Elapsed"
        c5 = "CPUtime"
        c6 = "SwitOut"
        c7 = "Thread"
        c8 = "InitCPU"
        c9 = "ExitCode"
        outR = '{:8} {:20} {:14} {:14} {:8} {:8} {:8} {:8} {:5} {:8}'.format(c1,c0,c2,c3,c4,c5,c6,c7,c8,c9)
        if verboseFlag >= 1:
            prtOutFile.write(outR + '\n')
        svcList = []
        svcSummary = []
        # Summary: svc Number, count, elapsed, cpu time, switched out
        for ii in parseData:
            tmpF = ii
            svcNow = int(tmpF[0])
            timeSt = tmpF[1]
            timeEnd = tmpF[2]
            timeElap = tmpF[3] + tmpF[6]
            timeCPU = tmpF[3]
            timeSwO = tmpF[6]
            Thrd = tmpF[-2]
            InitCpu = tmpF[7]
            ExitCode = tmpF[-1]
            try:
                indxSvcName = sysCallList.index(svcNow)
            except:
                print("oops")
                print("svc", svcNow)
                for ii in sysCallList:
                    print(ii)
            svcName = sysCallList[indxSvcName+1]
            outR = '{:8} {:20} {:14} {:14} {:8d} {:8d} {:8d} {:8} {:5} {:8d}'.format(svcNow,svcName,timeSt,timeEnd,timeElap,timeCPU,timeSwO,Thrd,InitCpu,ExitCode)
            if verboseFlag >= 1:
                prtOutFile.write(outR + '\n')
            try:
                svcIndex = svcList.index(svcNow)
            except:
                svcList.append(svcNow)
                svcIndex = svcList.index(svcNow)
                svcSummary.append([svcNow, svcName, 0,  0, 0, 0])
            adder = svcSummary[svcIndex]
            adder[2] += 1
            adder[3] += int(timeElap)
            adder[4] += int(timeCPU)
            adder[5] += int(timeSwO)
            svcSummary[svcIndex] = adder

        svcSummary.sort()
#       if we ever want to get clever and write the header at the "top" of the
#       page ---
#import sys
#import os
#
#try:
#    columns, rows = os.get_terminal_size(0)
#except OSError:
#    columns, rows = os.get_terminal_size(1)
#
#sys.stdout.write('cols:{}\nrows:{}\n'.format(columns, rows))
        outR = '{:5} {:22} {:10} {:10} {:9} {:10}'.format("  svc", "svc Name", "count", "AvgTime", "AvgCpu", "AvgOut")
        prtOutFile.write(outR + '\n')
        for ii in svcSummary:
            svcNow = ii[0]
            svcName = ii[1]
            svcCount = ii[2]
            totalTimeA = float(ii[3]) / float(ii[2])
            cpuTimeA = float(ii[4]) / float(ii[2])
            outTimeA = float(ii[5]) / float(ii[2])
            outR = '{:5} {:20} {:10} {:9.2f} {:9.2f} {:9.2f}'.format(svcNow,svcName, svcCount, totalTimeA, cpuTimeA, outTimeA)

            prtOutFile.write(outR + '\n')
            

    def  __init__(self, verboseFlag, outFile, parseData, syscallList):
        self.doPrint(verboseFlag, outFile, parseData, syscallList)
