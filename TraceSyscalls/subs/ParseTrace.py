#!usr/bin/python3

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
import argparse
import subprocess


class parseTrace:

#    def eprint(*args, **kwargs, verbose):
    def eprint(self, *args, **kwargs):
        if self.verbose > 1:
            print(*args, file=sys.stderr, **kwargs)

    def timSub(self, tBig, tSmall):
        partsBig = tBig.split('.')
        partB1 = int(partsBig[0])
        partB2 = int(partsBig[1][0:-1])
        partsSmall = tSmall.split('.')
        partS1 = int(partsSmall[0])
        partS2 = int(partsSmall[1][0:-1])
        if partB2 < partS2:
            partB2 += 1000000
            partB1 -= 1
        p2 = partB2 - partS2
        p1 = partB1 - partS1
        ret = p2 + (1000000*p1)
        return ret

    def findEntry(self, threadId, lastEntry):
        # start from the last entry and go backwards
        # not found is -1 -- otherwise, return entry in self.active_syscall
        curEntry = lastEntry
        while (curEntry >= 0):
            tmpf = self.active_syscall[curEntry]
            try:
                if tmpf[9]  == threadId:
                    return curEntry
            except:
                print("Error")
                
                print(tmpf, curEntry)
                for ii in self.active_syscall:
                    print(ii)
            curEntry -= 1
        return -1
    def doTraceParse(self, traceFile):
        comment = "#"
        sys_enter = " sys_enter"
        sys_exit = " sys_exit"
        sched_switch = " sched_switch"
        sched_wakeup = " sched_wakeup"
        Minus = "-"
        with open(traceFile) as trFile:    
            working = -1
            # active_syscall 
            # 0: syscall number
            # 1: time Start
            # 2: time End
            # 3: processor time (start - end - switched out time)
            # 4: time switched out
            # 5: time switched in
            # 6: total time switched out
            # 7: processor id start
            # 8: processor id end
            # 9: thread id
            # 10: syscall return value
            self.active_syscall = []
           
            for line in trFile:
                if line.find(sys_enter) == -1 and line.find(sched_switch) == -1 and line.find(sys_exit) == -1:
                    continue
                    
                lineSpl = line.split()
                if lineSpl[0] == comment:
                    continue
                lineSpl = line.split(":")
                lineSpl_0 = lineSpl[0].split()
                lineSpl_1 = lineSpl[1].split()
                lineSpl_2 = lineSpl[2].split()
                if lineSpl[1] == sys_enter:
                    syscallNum = lineSpl_2[1]
                    sysTimeSt = lineSpl_0[-1]
                    sysCpu = lineSpl_0[-3]
                    tmSpl = lineSpl_0[-4].split(Minus)
                    sysThread = tmSpl[-1]
                    appender = [syscallNum, sysTimeSt, 0, 0, 0, 0, 0, sysCpu, 0, sysThread, 0]
                    self.active_syscall.append(appender)
                    working += 1
                # for the moment, we're going to assume
                # a thread has only one active syscall at a time (should be true)
                elif lineSpl[1] == sched_switch:
                    tmSpl = line.split("prev_pid=")
                    tm2Spl = tmSpl[1].split()
                    prevThr = tm2Spl[0]
                    tmSpl = line.split("next_pid=")
                    tm2Spl = tmSpl[1].split()
                    nextThr = tm2Spl[0]
                    whichEntry = self.findEntry(prevThr, working)
                    if whichEntry == -1:
                        if prevThr != "0":
                            self.eprint(line)
                            self.eprint(f'Not found prev {prevThr:8}')
                    else:
                        tmpf = self.active_syscall[whichEntry]
                        tmpf[4] =  lineSpl_0[3]
                        self.active_syscall[whichEntry] = tmpf
                    whichEntry = self.findEntry(nextThr, working)
                    if whichEntry == -1:
                        if nextThr != "0":
                            self.eprint(line)
                            self.eprint(f'Not found next {nextThr:8}')
                        continue
                    tmpf = self.active_syscall[whichEntry]
                    tmpf[5] = lineSpl_0[-1]
                    if tmpf[5] == 0:
                        adder = 0
                    else:
                        adder = self.timSub(str(tmpf[5]), str(tmpf[4]))
                    tmpf[6] += adder
                    self.active_syscall[whichEntry] = tmpf
                elif lineSpl[1] == sched_wakeup:
                    # pass for now -- this only alerts scheduler to run thread
                    pass
                elif lineSpl[1] == sys_exit:
                    syscallNum = lineSpl_2[1]
                    sysTimeEn = lineSpl_0[-1]
                    sysCpu = lineSpl_0[-3]
                    tmSpl = lineSpl_0[0].split(Minus)
                    sysThread = tmSpl[-1]
                    whichEntry = self.findEntry(sysThread, working)
                    if whichEntry == -1:
                        prtS = 'Not found enter with exit {:8}'.format(sysThread)
                        self.eprint(prtS)
                        continue
                    remover = self.active_syscall[whichEntry]
                    remover[2] = sysTimeEn
                    remover[8] = sysCpu
                    adder = self.timSub(remover[2], remover[1])
                    remover[3] = adder - remover[6]
                    remover[10] = int(lineSpl_2[-1])
                    self.active_syscall[whichEntry] = remover
#                    print("Exit", remover)
#                    for ii in self.active_syscall:
#                        print(ii)
                else:
                    continue
        return self.active_syscall

    def  __init__(self, traceFile, verbose):
        self.verbose = verbose
        self.traceData_tmp = self.doTraceParse(traceFile)
        if 0 == 1:
            return
        #eliminate records with no syscall exit
        self.traceData = []
        for ii in self.traceData_tmp:
            tmpf = ii
            if int(tmpf[3]) == 0:
                continue
            self.traceData.append(tmpf)
