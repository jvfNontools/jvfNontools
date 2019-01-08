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
# add common to path
commonPath = sys.path[0] + '/../common'
sys.path.append(commonPath)

import subs.ParseTrace
import subs.parseArgs
import subs.DoOutput
import subs.ParseUnis
import os


trArgs = subs.parseArgs.getArgsCom()
traceParse = subs.ParseTrace.parseTrace(trArgs.traceFile, int(trArgs.verbose))
unistdData = subs.ParseUnis.parseUnistd(trArgs.unistd)
trOutput = subs.DoOutput.DoFormat(int(trArgs.verbose), trArgs.outFile, traceParse.traceData, unistdData.syscallList)
