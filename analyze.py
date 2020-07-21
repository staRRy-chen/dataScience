#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import zipfile
import xlwt
import pandas as pd
import openpyxl
def export_excel(export):
   #将字典列表转换为DataFrame
   pf = pd.DataFrame(list(export))
   #指定字段顺序
   order = ['id','type','queName','count','allCases','faceCases','originScore','realScore']
   pf = pf[order]
   columns_map = {
        'id':'用户id',
        'type':'类型',
        'queName':'题目',
        'count':'当前提交次数',
        'allCases':'总用例个数',
        'faceCases':'面向用例个数',
        'originScore':'原分数',
        'realScore':'实际分数'
   }
   pf.rename(columns = columns_map,inplace = True)
   #指定生成的Excel表格名称
   file_path = pd.ExcelWriter('C:/Users/Admin/Desktop/name.xlsx')
   #替换空单元格
   pf.fillna(' ',inplace = True)
   #输出
   pf.to_excel(file_path,encoding = 'utf-8',index = False)
   #保存表格
   file_path.save()
os.chdir('F:/test/')
file_chdir=os.getcwd()
file_tem = []
dic_list=[]
dic={}
file_comp = []
questionData=[]
allData=[]
cases=[]
inputs=[]
tempInput=''
outputs=[]
tempOutput=''
codeNumbers=[]
currentQue=''
code=''
id=0
type=''
score=0
queName=''
count=-1
faceCaseCount=0
testcases='.mooctest/testCases.json'
answer='.mooctest/answer.py'
codename='main.py'

def getTargetNumbers(s,t):
    numbers = []
    s=str(s)
    i = 0
    l = len(s)
    while i < l:
        num = ''
        symbol = s[i]
        while '0'<=symbol<='9':  # symbol.isdigit()
            num += symbol
            i += 1
            if i < l:
                symbol = s[i]
            else:
                break
        i += 1
        if num != '':
            numbers.append(int(num))
    if t=='i':
        inputs.append(numbers)
    elif t=='o':
        outputs.append(numbers)
    else:
        return numbers
    return

def judgeFaceCases(code,case):
    len1=len(code)
    len2=len(case)
    if len2==1 and case[0]<=3:
        return 0
    if len1<len2:return 0
    for i in range(0,len1-len2+1):
        if code[i:i+len2] == case:
            return 1
    return 0

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
        for i in range(0,len(cases)):
            tempInput = ''.join(cases[i]['input'])
            tempOutput = ''.join(cases[i]['output'])
            getTargetNumbers(tempInput,'i')
            getTargetNumbers(tempOutput,'o')
        print("测试用例输入：",end='')
        print(inputs)
        print("测试用例输出：",end='')
        print(outputs)
        codeNumbers=getTargetNumbers(code,'c')
        print("code中出现的所有数字：",end='')
        print(codeNumbers)
        for k in range(0,len(inputs)):
            faceCaseCount+=max(judgeFaceCases(codeNumbers,outputs[k]),judgeFaceCases(codeNumbers,inputs[k]))
        inputs=[]
        outputs=[]
    print(data[0],end=' ')
    print(data[1], end=' ')
    print(data[2], end=' ')
    print(data[3], end=' ')
    if data[4]==0:
        print("题目包",end='')
    else:
        print("第%d次提交" %(data[4]),end=' ')
        print("本题共%d个测试用例" %(len(cases)),end=' ')
        print("本次提交中面向用例个数为：%d" %(faceCaseCount),end=' ')
        realScore=data[3]-faceCaseCount/len(cases)*100
        if realScore<0:
            realScore=0
        print(cases)
        print(code)
        dic={'id':data[0],'type':data[1],'queName':data[2],'count':data[4],'allCases':len(cases),'faceCases':faceCaseCount,'originScore':data[3],'realScore':realScore}
        dic_list.append(dic)
        dic={}
        faceCaseCount=0
if __name__ == '__main__':
    export_excel(dic_list)
