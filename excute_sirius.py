# -*- coding: utf-8 -*-

'''
excute sirius
'''


import subprocess
import os

def excute_cmd(filename,output):

    input = "{}".format(filename)
    assert os.path.exists(input), "File does not existing, please read after cheaking!"

    command='sirius -i {}  -o ./{} formula -c 50 zodiac structure canopus'.format(input,output)
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout_data, stderr_data = result.stdout.read(),result.stderr.read()
    pid,returncode = result.pid, result.returncode

    return {
        'stdout':stdout_data,
        'stderr':stderr_data,
        'pid':pid,
        'returncode':returncode
    }

if __name__ == '__main__':
    from config import arg_parse
    args=arg_parse()
    print(args.input)
    excute_cmd(args.input,args.output1)
