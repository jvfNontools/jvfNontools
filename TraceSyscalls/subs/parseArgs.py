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
import argparse
import subprocess


class getArgs:

    def getFiles(self):

# use argparse to get input parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--trace", default='trace1.out', help="formatted ftrace file")
        parser.add_argument("-m", "--machine", help="machine: data is from -- power or x86_64-- default, current machine")
        parser.add_argument("-k", "--kallsyms", default='kallsyms.out', help='kernel symbols, \ndefault kallsyms.out')
        parser.add_argument("-o", "--output", default='syscalls.out',  help='output file: default syscalls.out')
        parser.add_argument("-v", "--verbose",  help="verbose: =0 prints summary only; =1 prints all syscall data and summary; =2 prints =1 plus warnings on stderr; default =0")
        parser.add_argument("-u", "--unistd",  help="full path to location of unistd.h (which holds syscall number to syscall name #defines)\n default [source directory]/unistd/power_unistd.h or [source directory]/unistd/x86_unistd.h based on machine")
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
        if args.verbose == None:
            args.verbose = 0
        if args.unistd == None:
            if args.machine == "x86_64":
                args.unistd = sys.path[0] + "/unistd/x86_64_unistd.h"
            else:
                args.unistd = sys.path[0] +  "/unistd/power_unistd.h"
        ret = [args.verbose, args.output, args.trace, args.machine, args.kallsyms, args.unistd]
        return ret
    

    def  __init__(self):
        setFiles = self.getFiles()
        self.verbose = setFiles[0]
        self.outFile = setFiles[1]
        self.traceFile = setFiles[2]
        self.machine = setFiles[3]
        self.kallsyms = setFiles[4]
        self.unistd = setFiles[5]

