#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import zipfile
os.chdir('F:/test/')
file_chdir=os.getcwd()
file_tem = []
file_comp = []
questionData=[]
allData=[]
cases=[]
currentQue=''
code=''
id=0
type=''
score=0
queName=''
count=-1
testcases='.mooctest/testCases.json'
answer='.mooctest/answer.py'
codename='main.py'
for root,dirs,files in os.walk(file_chdir):
    for file in files:
        file_tem.append(file)
        data = os.path.splitext(file)[0].split(',')
        file_tem.append(int(data[0]))
        file_tem.append(data[1])
        file_tem.append(float(data[2]))
        file_tem.append(data[3])
        file_comp.append(file_tem)
        file_tem = []
file_comp.sort(key=lambda x: (x[1], x[2],x[4],x[3]))


for file in file_comp:
    if file[1]!=id:
        id=int(file[1])
    if file[2]!=type:
        type=file[2]
    if str(file[4]).split('_')[0]!=queName:
        queName=str(file[4]).split('_')[0]
        count=-1
        score=0
    if file[3]!=score:
        score=file[3]
    if str(file[4]).split('_')[0] == queName:
        count+=1
    questionData.append(id)
    questionData.append(type)
    questionData.append(queName)
    questionData.append(score)
    questionData.append(count)
    questionData.append(file[0])
    allData.append(questionData)
    questionData=[]

for data in allData:
    read_hey = zipfile.ZipFile(data[5])
    if data[4]==0:#如果count=0，代表题目包，从题目包中获取测试用例
        if testcases in read_hey.namelist():
            '''with open(testcases, 'r', encoding='utf8')as fp:
                json_data = json.load(fp)
                print(json_data)'''
            fp=read_hey.open(testcases)
            cases = json.load(fp)
            currentQue=data[2]#更新当前题目
    else:
        zipname=read_hey.namelist()[0]
        if '.zip' in zipname:
            fp=read_hey.open(zipname)
            read_code=zipfile.ZipFile(fp)
            code=read_code.open(codename).read()#获取当前提交代码
            if data[2]!=currentQue:#检验题目与测试用例当前题目是否一致
                f=read_code.open(testcases)
                cases=json.load(f)
