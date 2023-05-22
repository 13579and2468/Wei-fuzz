#!/usr/bin/python3
import sys
import os
def main():
    
    if len(sys.argv) < 2:
        print("Usage: ./fuzz_graph.py [out_dir_of_arg_fuzzer] [fuzzing_target_build_with_asan]")
    else:
        crash_arg_dir = sys.argv[1] + '/queue_info/crashes/'
        crash_dir = sys.argv[1] + '/crashes/'
        with os.scandir(crash_arg_dir) as it:
            direntries = list(it)  # reads all of the directory entries
            direntries.sort(key=lambda x: x.name)
        
        for entry in direntries:
            f = open(entry, 'r')
            tokens = f.readline().split()
            crash_file = crash_dir + entry.name

            for i in range(len(tokens)):
                if '.cur_input' in tokens[i]:
                    tokens[i] = crash_file

            tokens[0] = 'ASAN_OPTIONS=halt_on_error=0 ' + sys.argv[2]
            cmdline = ' '.join(tokens)
            print(entry.name[:10])
            os.system(cmdline + ' 1>/dev/null')
            f.close()
            input((os.path.getctime(crash_dir+entry.name)-os.path.getctime(sys.argv[1]+'/queue_info'))/3600)

            
if __name__ == "__main__":
    main()
