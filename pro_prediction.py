'''
将向量转成model可接受的输入
调用模型预测
'''
import glob
import os
import pandas as pd
from data_process import load_data
import joblib


def merge_results(output2):
    '''
    合并所有指定前缀的文件夹
    :param output2:
    :return:
    '''

    path=output2
    path_list=glob.glob('{}/*.csv'.format(output2))#sirius结果转成的向量文件所在的路径
    car=[]
    spit=path.count('/')#默认搜索整个字符串 path中/的个数
    name_head=4 #定义前缀的位数

    '''获取所有的前缀'''
    for filename in path_list:
        dir_name=filename#获取这些文件的完整路径
        # 因为是根据 / 分割的,要注意文件的位置,根据name_head取前几位字母
        name=dir_name.split('/')[spit+1][:name_head]
        car.append(name)

    listType = set(car)#`set()` 建立一个无序的独特元素合集
    dictionary = dict(zip([i for i in range(len(listType))],listType))#给上述的listType加上一个index，组成一个字典

    for i in range(len(listType)):
        df=pd.DataFrame()
        for filename in path_list:
            dir_name = filename
            name = dir_name.split('/')[spit + 1][:name_head]
            if name== 'pro_':
                data_input=pd.read_csv(dir_name,index_col=0)
                df = pd.concat([df,data_input],axis=0)
                df = df.sort_values(by='siderophore', ascending=[False]).reset_index(drop=True)
                df.to_csv('{}/result.csv'.format(os.path.dirname(output2)))

def pro_predict(output2,ionsource_type):
    for root,dirs,files in os.walk(output2):#output2是包含fp向量和meta的所有文件的文件夹
        for j in range(len(dirs)):
            for root1,dirs1,files1 in os.walk('{}/{}'.format(output2,dirs[j])):
                list=[]
                for file in os.listdir('{}/{}/'.format(output2,dirs[j])):
                    if file.endswith('.csv'):
                        list.append(file)
                locals()['sum' + str(j)]=pd.concat([pd.read_csv('{}/{}/{}'.format(output2,dirs[j],x),index_col=0) for x in list],axis=1)
                locals()['sum'+str(j)]=locals()['sum' + str(j)].T
                locals()['sum'+str(j)].columns=['X'+str(l) for l in range(0,1401)]
                locals()['sum' + str(j)].index=[m for m in list]
                locals()['sum' + str(j)]['y']=1
                locals()['sum' + str(j)]['w'] =1
                locals()['sum' + str(j)]['ids'] =1
                locals()['sum'+str(j)].to_csv('{}/{}.csv'.format(output2,dirs[j]))

                dataX, dataY, dataW, dataid=load_data(output2,dirs[j])

                if ionsource_type=='positive':
                    clf = joblib.load('sid_predict+.pkl')
                else:
                    clf = joblib.load('sid_predict-.pkl')

                y_pred = clf.predict(dataX)
                y_pro = clf.predict_proba(dataX)
                s = ['not siderophore', 'siderophore']
                pro_DF = pd.DataFrame(y_pro, columns=s)
                pro_DF['prediction'] = y_pred
                list1=[]
                for file1 in os.listdir('{}/{}/'.format(output2,dirs[j])):
                    if file1.endswith('.txt'):
                        list1.append(file1)
                    for k in range(len(list1)):
                        locals()['data']=pd.read_table('{}/{}/{}'.format(output2, dirs[j],list1[k]),header=None)
                        try:
                            pro_DF['Premass'] = locals()['data'].iloc[0,0]
                            pro_DF['formula'] = list
                            pro_DF['name'] = dirs[j]
                            pro_DF['Sirisus_score']=locals()['data'].iloc[1,0]
                            pro_DF['RT'] = locals()['data'].iloc[2,0]
                        except:
                            pro_DF['RT'] = 'Unknown'
                        pro_DF.to_csv('{}/pro_{}.csv'.format(output2,dirs[j]))
    merge_results(output2)


if __name__ == '__main__':
    from config import arg_parse
    args=arg_parse()
    pro_predict(args.output2,args.ionsource)