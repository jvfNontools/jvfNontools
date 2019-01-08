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
        parser.add_argument("-s", "--symbol", default='symbols', help="symbol file from stderr of 'perf annotate -vn >>symbols > anno.perf.data' -- default symbols")
        parser.add_argument("-a", "--anno", default='anno.perf.data', help="annotated data  file from\n'perf annotate -vn >>symbols > anno.perf.data'\n -- default anno.perf.data")
        parser.add_argument("-o", "--output", default='annoOrderedTree',  help="output file: default annoOrderedTree")
        setFiles = GetArgs.getArgs.getFiles(self, parser)
        # set by default
        self.verbose = setFiles.verbose
        self.outFile = setFiles.output
        self.symFile = setFiles.symbol
        self.annoFile = setFiles.anno
# done in common
        self.machine = setFiles.machine

       
