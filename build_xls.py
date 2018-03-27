#coding:utf-8

from datetime import *  
import time,os,os.path,shutil
import xlwt;  
import xlrd;  
#import xlutils;  
from xlutils.copy import copy;  
from xlrd import open_workbook






def get_Xls(author,p,summary,a_or_b):
    if a_or_b == "a":
        sheet_nu = 0
    else:
        sheet_nu = 1
    example_Xls_Path = u'C:\dir_for_python_jira\example_P****3.0\动作确认.xls'
    today_Xls_Dir_Path = u'C:\dir_for_python_jira\%s_P****3.0'%date.today().strftime('%Y-%m-%d')
    isExists=os.path.exists(today_Xls_Dir_Path)
    if not isExists:
        os.makedirs(today_Xls_Dir_Path)
        shutil.copy(example_Xls_Path,today_Xls_Dir_Path)
    else:
        print today_Xls_Dir_Path+' is exist!'  
    
    target_File = u'C:\dir_for_python_jira\%s_P****3.0\动作确认.xls'%date.today().strftime('%Y-%m-%d')
    rb = xlrd.open_workbook(target_File,formatting_info=True)        #formatting_info=True 仅支持xls，xlsx需要格式转换
    rs = rb.sheet_by_index(sheet_nu)             #通过sheet_by_index()获取的sheet没有write()方法
    wb = copy(rb)                         
    ws = wb.get_sheet(sheet_nu)                  
    i = 0
    for line in p:
        p_1 = ''.join(p[i]).encode('utf8')
        summary_1 = ''.join(summary[i]).encode('utf8')
        p_summary = p_1 + summary_1
        ws.write(i+33,1,p_summary.decode('utf8'))
        #print t[4].replace("\n",'')            #责任者
        ws.write(i+33,7,''.join(author[i]).decode('utf8'))
        ws.write(i+33,4,u"手動")
        ws.write(i+33,5,u"待确认")
        i += 1 
    wb.save(target_File)
    
    
    
def main():
    


if __name__ == "__main__":  
    main() 
