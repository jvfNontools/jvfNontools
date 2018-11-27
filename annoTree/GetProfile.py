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

import subs.GetArgs
import subs.parsSyms
import subs.parsAnno
import subs.doFormat
import subprocess
import os

import sys

argClass = subs.GetArgs.getArgs()
symClass = subs.parsSyms.SearchFileForSyms(argClass.symFile, "symbol__disassemble")
annoClass = subs.parsAnno.SearchAnnoFile(argClass.annoFile, symClass.symData, argClass.machine)
subs.doFormat.doFormatOut(annoClass.annoData, argClass.outFile, annoClass.TotalTicks, argClass.machine)
# x86_64 symbols are mangled -- run cxxflit on outfile -- note this requires a temp file
if argClass.machine != "power":
    if argClass.outFile == "sys.stdout":
        sys.stderr.write("Can not use c++filt on stdout. Use std file or pipe output to c++filt\n")
    else:
        filtOutName = argClass.outFile + str(os.getpid()) # hopefully unique
        filtOut = open(filtOutName, 'w')
        filtIn = open(argClass.outFile)
        subprocess.run(['c++filt'], stdin=filtIn, stdout=filtOut)
        filtOut.close()
        filtIn.close()
        subprocess.run(['cp', filtOutName, argClass.outFile])
        subprocess.run(['rm', '-f', filtOutName])
