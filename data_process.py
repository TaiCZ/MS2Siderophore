# -*- coding: utf-8 -*-

'''

'''
import os
import csv
from config import arg_parse

path = "./data"
filename = "sid_train"

def load_data(path, filename):

    dir = "{}/{}.csv".format(path, filename)
    assert os.path.exists(dir), "File does not existing, please read after cheaking!"
    # content = pd.read_csv(dir)
    # print(content)
    with open(dir, 'r') as f:
        file = csv.reader(f)
        contents = list(file)
        label = " ".join(contents[0])
        #X,y,w的个数
        Num_X = label.count('X')
        Num_Y = label.count('y')
        Num_W = label.count('w')

        # print(content)
        data_X = []
        data_Y = []
        data_W = []
        data_id = []
        for content in contents[1:]:
            data_X.append([float(i) for i in content[1:Num_X+1]])
            data_Y.append(float(content[Num_X+1]))
            data_W.append(float(content[Num_X+Num_Y+1]))
            data_id.append(content[Num_X+Num_Y+Num_W+1])
    return data_X, data_Y, data_W, data_id

if __name__ =='__main__':
    args=arg_parse()
    dataX, dataY, dataW, dataid = load_data(args.datadir, args.dataname)
    print(dataY[0])
