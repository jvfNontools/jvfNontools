# jvfNontools
Performance analysis related tools
Generally work off data produced by standard tools (trace, perf, etc) to
reformat and/or summarize standard data to make it easier to use -- suggestions for improvements and/or new tools welcome.

I.  annoTree/GetProfile.py -- (python3) -- uses output from perf annotate -- best is, 

"perf annotate -vn 2>symbols >anno.perf.data" --

to create a list of functions/methods, sorted by frequency. Where available,
callers of the functions are listed by frequency.

See "annoTree/GetProfile.py --help" for details.

2.  TraceSyscalls/GetSyscalls.py -- (python3) -- uses output from system trace

to create a (sorted by syscall number) list of syscalls with 
name, frequency, average cpu time, average elapsed time and average total time

See "TraceSyscalls/GetSyscalls.py --help" for details.
