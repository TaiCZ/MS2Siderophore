# -*- coding: utf-8 -*-

'''

'''
import argparse

def arg_parse():
    parser = argparse.ArgumentParser(usage='python sidprediction.py -i *.mgf -o1 Result/sirius_output -o2 Result/sid_pro  ',description='Predicting the probablity of siderophores')
    parser.add_argument('-i','--input',dest='input',help='mgf_file')
    parser.add_argument('-o1', '--output1', dest='output1', help='Sirius output directory')
    parser.add_argument('-o2', '--output2', dest='output2', help='Probablity output directory')
    parser.add_argument('-t','--type', dest='ionsource',help='Type of ionsource')
    parser.set_defaults(
                        input='./data/test.mgf',
                        output1='./result/output1',
                        output2='./result/output2',
                        ionsource='positive',
                        dataname='sid_train',
                        profile='qtof',
                        model="RF",
                        iters=5,
                        seed=200,)
    return parser.parse_args()
