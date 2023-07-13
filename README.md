# Wei-fuzz
Fuzzer runs with argv information and can use MAB model to select seed and task.
Either Wei-fuzz or Wei-fuzz with MAB improve the time allocation of Yuan-fuzz. 

```
  Written and maintained by 13579and2468 <13579and24680@gmail.com>
  Based on American Fuzzy Lop by Michal Zalewski
```

## Why I do this?
During my research on SQ-Fuzz and Yuan-fuzz, I found that the existing multi-parameter fuzz testing has a serious time allocation problem. In most cases, the parameter mutation(arg_gen) can generate new edge coverage very efficiently in the early stage, but its decay speed is also very fast. After a period of execution, the performance of AFL's original mutation mechanism (havoc and splice) will surpass the parameter mutation. At the same time, in my understanding of AFL, the non-parametric file mutation is the key to finding deep problems in the program, and the usage of parameters is used as a guide. Based on this observation and idea, I tried to optimize the multi-parameter fuzz test by fine-tuning first, and finally tried to introduce the MAB (Multi-armed bandit) problem to allocate the mutation time more reasonably. Many papers also show that MAB is very suitable in the field of fuzz testing.

This fuzzer first fixes a serious memory leak problem in Yuan-fuzz. In the 47-hour experiment on objdump, it increased the edge coverage of 3.777% and more than doubled the number of executions. Based on the improved version and the above concepts, Wei-fuzz and Wei-fuzz(MAB) were implemented. In the 301-hour experiment on objdump, Wei-fuzz increased the edge coverage of 11.33% compared with Yuan-fuzz(fix)(Yuan-fuzz with memory leak fixed). Compared with Yuan-fuzz(fix), Wei-fuzz(MAB) increased the edge coverage of 18.64%. During the research period, 31 program errors were found, 23 of which have been fixed by the author, and 22 bugs were assigned CVE ids.


## TODO
- Compare with other fuzzer scheduling methods like Ecofuzz.
- Auto tunning the MAB coefficient(999/1000 now) 

## Usage
Install [libxml2](http://xmlsoft.org/downloads.html) first.

Build it.
```
$ make
```

I update some [XML examples](https://github.com/13579and2468/Wei-fuzz/tree/main/xml) here.

Instrumentation method is the same as AFL.

The command line usage of Wei-fuzz is similar to Yuan-fuzz and AFL, but can enable arg_gen_det with '-A' and MAB with '-a'.
The defualt mode of Wei-fuzz uses 'quick and dirty' mode like AFL++. You can disable with '-D'.
```
$ Wei-fuzz -i [testcase_dir] -o [output_dir] -s [~/XML_PATH/parameters.xml] [-A] [-a] -- [Target program]
```

## Example
Use [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) to be example.
```
$ git clone git@github.com:libjpeg-turbo/libjpeg-turbo.git
```
Build with instrumentation, you can use other compiler.
```
$ export CC=~/Wei-fuzz/afl-gcc                                       
$ export CXX=~/Wei-fuzz/afl-g++
$ cd libjpeg-turbo
$ mkdir build && cd build
$ cmake -G"Unix Makefiles" ..
$ make
```

Run fuzzer
``` 
$ Wei-fuzz -i ./testcases/images/jpeg -o fuzz_output -m none -s ./xml/libjpeg-turbo/djpeg/parameters.xml -A -a -- ~/TARGET_PATH/libjpeg-turbo/build/djpeg
```

If yout parameter list is too long, change the defined value of size in parse.h.

## Interpreting output
You can get the argv of seeds of queue and crashes in the queue_info directory.

- queue_info/queue
- queue_info/crashes
- queue_info/hangs

## Bug reported
### nasm
https://bugzilla.nasm.us/show_bug.cgi?id=3392820 (CVE-2022-44368)\\
https://bugzilla.nasm.us/show_bug.cgi?id=3392819 (CVE-2022-44369)\\
https://bugzilla.nasm.us/show_bug.cgi?id=3392815 (CVE-2022-44370)\\
https://bugzilla.nasm.us/show_bug.cgi?id=3392814 (CVE-2022-46456)\\
https://bugzilla.nasm.us/show_bug.cgi?id=3392809 (CVE-2022-46457)\\
### binutils
https://sourceware.org/bugzilla/show_bug.cgi?id=29870 (CVE-2023-22603)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29872 (CVE-2023-22604)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29893 (CVE-2023-22605)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29908 (CVE-2023-22606)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29914 (CVE-2023-22607)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29936 (CVE-2023-22608)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29948 (CVE-2023-22609)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=29988 (CVE-2023-1579)\\
https://sourceware.org/bugzilla/show_bug.cgi?id=30284\\
https://sourceware.org/bugzilla/show_bug.cgi?id=30285 (CVE-2023-1972)\\
### libtiff
https://gitlab.com/libtiff/libtiff/-/issues/488 (CVE-2022-48281)\\
https://gitlab.com/libtiff/libtiff/-/issues/520 (CVE-2023-25433)\\
https://gitlab.com/libtiff/libtiff/-/issues/519 (CVE-2023-25434)\\
https://gitlab.com/libtiff/libtiff/-/issues/518 (CVE-2023-25435)\\
https://gitlab.com/libtiff/libtiff/-/issues/527 (CVE-2023-26965)\\
https://gitlab.com/libtiff/libtiff/-/issues/530 (CVE-2023-26966)\\
https://gitlab.com/libtiff/libtiff/-/issues/541\\
https://gitlab.com/libtiff/libtiff/-/issues/549\\
https://gitlab.com/libtiff/libtiff/-/issues/553\\
https://gitlab.com/libtiff/libtiff/-/issues/554\\
https://gitlab.com/libtiff/libtiff/-/issues/555\\
https://gitlab.com/libtiff/libtiff/-/issues/556\\
https://gitlab.com/libtiff/libtiff/-/issues/571\\
### Aomedia
https://bugs.chromium.org/p/aomedia/issues/detail?id=3424 (CVE-2023-31539)\\
https://bugs.chromium.org/p/aomedia/issues/detail?id=3425 (CVE-2023-31540)\\
### libxml2
https://gitlab.gnome.org/GNOME/libxml2/-/issues/550\\

## Thanks
Use [Yuan-fuzz](https://github.com/zodf0055980/Yuan-fuzz) to modify.
