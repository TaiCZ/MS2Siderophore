'''
定位到Sirius的fingerprints(目标文件)
合并 fp 与 pro,输出对应的文件夹
'''

import os
import pandas as pd

def search(rootdir,keyword):
    '''
    :param rootdir:搜索目录
    :param keyword: 包含关键词
    :return: 返回文件名
    '''
    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:  # 输出文件信息
            # print "filename is:" + filename
            if keyword in filename:
               return filename # 输出文件路径信息

def prt_stratswith(file,starts_txt):
    '''

    :param file: 读取文件
    :param starts_txt: 起始关键词
    :return: 返回关键词后所有内容
    '''

    with open (file,'r')as f:
        lines1=f.read().splitlines()
        for line in lines1:
            if line.startswith(starts_txt):
                return line[len(starts_txt):]


def input_generate(path,result):#path是sirius输出的结果，result是预测输出
    '''

    :param path: siris的输出结果总文件,比如 output1
    :param result: 合并 fp 与 pro,输出对应的文件夹，比如output2
    :return: None
    '''

    #创建结果文件，output2
    if os.path.exists(result)==False:
        os.mkdir(result)

    for root,dirs,files in os.walk(path):
        #print(root) #string/root根目录
        #print(dirs) #list/root下所有子目录文件夹
        #print(files)#list/root下非目录子文件
            for j in range(0,len(dirs)):
                for root1,dirs1,files1 in os.walk('{}/{}'.format(path,dirs[j])):
                    try:
                        locals()['formula']=pd.read_csv('{}/{}/formula_candidates.tsv'.format(path,dirs[j]),sep='\t').iloc[0,1]
                        locals()['fpt_file']=search('{}/{}/fingerprints'.format(path,dirs[j]),locals()['formula'])
                        if os.path.exists('{}/{}/fingerprints'.format(path,dirs[j]))==True:
                            a = pd.read_table('{}/{}/fingerprints/{}'.format(path, dirs[j], locals()['fpt_file']),
                                              names=['pro'])
                            if os.path.exists('{}/{}'.format(result,dirs[j])) == False:
                                os.mkdir('{}/{}'.format(result,dirs[j]))
                            a.iloc[0:1401,:].to_csv('{}/{}/{}.csv'.format(result,dirs[j],locals()['fpt_file']))

                            '''获取ionMass,rt和sirius score，生成compound info的信息'''
                            b=prt_stratswith('{}/{}/compound.info'.format(path,dirs[j]),'ionMass	')
                            c=prt_stratswith('{}/{}/compound.info'.format(path,dirs[j]), 'rt	')
                            d=prt_stratswith('{}/{}/compound.info'.format(path,dirs[j]).format(locals()['fpt_file'].split('.')[0]),'sirius.scores.SiriusScore	')
                            with open ('{}/{}/{}.txt'.format(result,dirs[j],locals()['fpt_file']),'w')as f1:
                                try:
                                    f1.write(b+'\n')
                                    f1.write(d+'\n')
                                    f1.write(c+'\n')
                                except:
                                    pass
                        else:
                            pass
                    except:
                        pass

if __name__ == '__main__':
    from config import arg_parse
    args=arg_parse()
    print('SIRIUS的输出文件'+args.output1)  # SIRIUS的输出文件
    print('vector的输出文件'+args.output2)  # vector的输出文件
    input_generate(args.output1,args.output2)