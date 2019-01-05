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

class parseUnistd:

    def parseFile(self, unistd):
        unSplit = "define __NR_"
        sysCallList = []
        with open(unistd) as unFile:
            for line in unFile:
                gd = line.find(unSplit)
                if gd == -1:
                    continue
                splLine = line.split(unSplit)
                splSys = splLine[1].split()
                if splSys[0] == "syscalls":
                    # x86_64 has some extra after this one
                    break
                sysCallList.append(int(splSys[1]))
                sysCallList.append(splSys[0])
        return sysCallList
                
    def  __init__(self, unistd):
        self.syscallList = self.parseFile(unistd)
