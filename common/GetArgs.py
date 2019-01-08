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

    def getFiles(self, parser):

# use argparse to get input parameters
        parser.add_argument("-m", "--machine", help="machine: data is from -- power or x86_64-- default, current machine")
        parser.add_argument("-v", "--verbose",  help="verbose: =0 standard output; =1 detailed output including standard; =2 adds warnings on stderr; default =0", default=0)
        parser.add_argument("-k", "--kallsyms", default='kallsyms.out', help='kernel symbols, \ndefault kallsyms.out')
        args = parser.parse_args()

        if args.verbose == None:
            args.verbose = 0
       
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
#        ret = [args.symbol, args.output, args.anno, args.machine, args.kallsyms]
        return args
    
