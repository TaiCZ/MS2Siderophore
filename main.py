# -*- coding: utf-8 -*-
'''
main()：
    1. excute_sirius
    2. input_generate
    3. pro_predict
'''

from excute_sirius import excute_cmd
from input_gen import input_generate
from config import arg_parse
from pro_prediction import pro_predict

def main(args):
    excute_cmd(args.input,args.output1)
    input_generate(args.output1,args.output2)
    pro_predict(args.output2,args.ionsource)
    print('Program completed！')



if __name__=='__main__':
    args=arg_parse()
    main(args)