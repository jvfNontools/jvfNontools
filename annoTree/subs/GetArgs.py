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


class getArgs:

    def getFiles(self):

# use argparse to get input parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--symbol", default='symbols', help="symbol file from stderr of 'perf annotate -vn >>symbols > anno.perf.data' -- default symbols")
        parser.add_argument("-m", "--machine", help="machine: data is from -- power or x86_64-- default, current machine")
        parser.add_argument("-a", "--anno", default='anno.perf.data', help="annotated data  file from\n'perf annotate -vn >>symbols > anno.perf.data'\n -- default anno.perf.data")
        parser.add_argument("-o", "--output", default='annoOrderedTree',  help="output file: default annoOrderedTree")
        args = parser.parse_args()
       
        if args.machine == None:
            machIs = subprocess.check_output(['uname', '-m'])
           # change to string 
            PY3K = sys.version_info >= (3, 0)
            machStr = []
            if not PY3K:
                machStr.append(machIs)
            else:
                machStr.append(machIs.decode('cp437'))
            try:
                xCount = machStr.index("x86_64\n")
                args.machine = "x86_64"
            except:
                args.machine = "power"
        ret = [args.symbol, args.output, args.anno, args.machine]
        return ret
    

    def  __init__(self):
        setFiles = self.getFiles()
        self.symFile = setFiles[0]
        self.outFile = setFiles[1]
        self.annoFile = setFiles[2]
        self.machine = setFiles[3]

