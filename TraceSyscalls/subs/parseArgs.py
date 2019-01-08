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
import GetArgs


class getArgsCom(GetArgs.getArgs):

    def __init__(self):

# use argparse to get input parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--trace", default='trace1.out', help="formatted ftrace file")
        parser.add_argument("-u", "--unistd",  help="full path to location of unistd.h (which holds syscall number to syscall name #defines)\n default [source directory]/unistd/power_unistd.h or [source directory]/unistd/x86_unistd.h based on machine")
        parser.add_argument("-o", "--output", default='syscalls.out',  help="output file: default syscalls.out")

        setFiles = GetArgs.getArgs.getFiles(self, parser)
# set by default
        self.verbose = setFiles.verbose
        self.outFile = setFiles.output
        self.traceFile = setFiles.trace
        self.kallsyms = setFiles.kallsyms
# others need check for default
# done in common 
        self.machine = setFiles.machine
# set default if not entered
        if setFiles.unistd == None:
            if setFiles.machine == "x86_64":
                self.unistd = sys.path[0] + "/unistd/x86_64_unistd.h"
            else:
                self.unistd = sys.path[0] +  "/unistd/power_unistd.h"

