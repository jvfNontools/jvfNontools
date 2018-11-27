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


class SearchFileForSyms:

    def doSearch(self, openFile, searchItem):
        symb = "sym="
        startb = "start-address=0x"
        commb = ","
        spacb = " "
        parab = "("
        brackb = "["
        allSyms = []
        symIndex = 0
        with open(openFile) as symFile:
            for line in symFile:
                if (line.find(searchItem) == -1):
                    continue
                # want exception if search items not found
                si = line.index(symb)
                ei = line.index(commb, (si+1))
                li = line.rfind(parab, (si+1), ei)
                if (li == -1):
                    li = line.rfind(brackb, (si+1), ei)
                    if li == -1:
                        sy0 = line[(si+4): (ei)]
                    else:
                        sy0 = line[(si+4): li]
                else:
                    sy0 = line[(si+4): li]
                line = symFile.readline()
                line = symFile.readline()
                si = line.index(startb)
                ei = line.index(spacb, si)
                star10 = line[(si+16): ei]
                star1 = star10.lstrip("0")
                allSyms.append(sy0)
                allSyms.append(star1)

        return allSyms

    def __init__(self, openFile, searchItem):
        self.symData = self.doSearch(openFile, searchItem)
