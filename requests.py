# -*- coding: utf-8 -*-
import re
import requests
import paramiko
from build_xls import get_Xls      #txt_to_xls.py
from selenium import write_Web
import jenkins
from time import sleep,strftime,localtime
from mail import Mail
from push_tag import push_Tag
import logging
from datetime import date
import copy

End_Commit_ID_branch_1 = ''
End_Commit_ID_branch_2 = ''
Start_Commit_ID_branch_1 = ''
Start_Commit_ID_branch_2 = ''

All_Commit_ID_branch_1 = []
All_Author_branch_1 = []
All_branch_1 = []
All_Summary_branch_1 = []

All_Commit_ID_branch_2 = []
All_Author_branch_2 = []
All_branch_2 = []
All_Summary_branch_2 = []

def get_End_Commit_ID_branch_1():
    hostname = '198.168.1.158'  
    port = 22  
    username = 'root'  
    password = '密码'  
    commit_value = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command ('cd /home/pwd \n git reset --hard HEAD\n git checkout branch_1 \n git pull --rebase \n git log --pretty="%H" -1 ')	
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.  
    filters = ['Current','Branch','origin']  
    for line in stdout:
    	if any(keyword in line for keyword in filters): continue
    	commit_value = line.strip('\n')
    	#print commit_value
    s.close()   
    return commit_value
    
def get_End_Commit_ID_branch_2():
    hostname = '198.168.1.158'  
    port = 22  
    username = 'root'  
    password = '密码'  
    commit_value = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command ('cd /home/pwd \n git reset --hard HEAD\n git checkout branch_2 \n git pull --rebase \n git log --pretty="%H" -1 ')	
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.  
    filters = ['Current','Branch','origin']  
    for line in stdout:
    	if any(keyword in line for keyword in filters): continue
    	commit_value = line.strip('\n')
    	#print commit_value
    s.close()   
    return commit_value
    
def get_400_commit():
    hostname = '198.168.1.158'  
    port = 22  
    username = 'root'  
    password = '密码'  
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command('cd /home/pwd  \n git reset --hard HEAD \n git checkout branch_1_uas_dev \ngit pull --rebase \n git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $2}\'>branch_1_author.txt\n  git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $3}\'>branch_1_P.txt\n git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $1}\'>branch_1_commit.txt\n scp branch_1_author.txt root@198.168.1.25:/home/uas/ \n scp branch_1_P.txt root@198.168.1.25:/home/uas/ \n scp branch_1_commit.txt root@198.168.1.25:/home/uas/ ')
    for line in stdout:
        print line
    for line in stderr:
        print line
    s.close()
    
def get_400_branch_2():
    hostname = '198.168.1.158'  
    port = 22  
    username = 'root'  
    password = '密码'  
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command('cd /home/pwd \n git reset --hard HEAD \n git checkout branch_2_uas_dev \ngit pull --rebase \n git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $2}\'>branch_2_author.txt\n  git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $3}\'>branch_2_P.txt\n git log --pretty=%H****%an****%s -400 | awk -F \'[*]+\' \'{print $1}\'>branch_2_commit.txt\n scp branch_2_author.txt root@198.168.1.25:/home/uas/ \n scp branch_2_P.txt root@198.168.1.25:/home/uas/ \n scp branch_2_commit.txt root@198.168.1.25:/home/uas/ ')
    for line in stdout:
        print line
    for line in stderr:
        print line
    s.close()

def get_Author_P(Start_Commit_ID,End_Commit_ID,branch_1_or_branch_2):
    All_Author_1 = []
    All_1 = []
    All_Author_2 = []
    All_2 = []
    All_Commit_ID_2 = []
    start_Flag = 0
    index = 0
    def check_P(word,ppp):
        return word in ppp

        
    x = open("d:\\uas\\%s_author.txt"%branch_1_or_branch_2)
    for line in x:
        All_Author_1.append(line.strip())

    y = open("d:\\uas\\%s_P.txt"%branch_1_or_branch_2)
    for line in y:
        All_1.append(line.strip())


    z = open("d:\\uas\\%s_commit.txt"%branch_1_or_branch_2)
    for line in z:
        if line.strip() == Start_Commit_ID:
            start_Flag = 1
            print line 
            if check_P('ABCDEFHIG',All_1[index]):
                try:
                    temp_line = re.search(r'ABCDEFHIG-[0-9]{5}',All_1[index]).group()
                    All_2.append(temp_line)
                    All_Author_2.append(All_Author_1[index])
                    All_Commit_ID_2.append(line.strip())
                except Exception:
                    print 'Exception:\t %s'%line
                    
            elif check_P('ABCD',All_1[index]):
                try:
                    temp_line = re.search(r'ABCD-[0-9]{5}',All_1[index]).group()
                    print temp_line
                    All_2.append(temp_line)
                    print All_2
                    All_Author_2.append(All_Author_1[index])
                    print All_Author_2
                    All_Commit_ID_2.append(line.strip())
                    print All_Commit_ID_2
                except Exception:
                    print 'Exception:\t %s'%line
                    
            elif check_P('P',All_1[index]):
                try:
                    temp_line = re.search(r'P-[0-9]{5}',All_1[index]).group()
                    All_2.append(temp_line)
                    All_Author_2.append(All_Author_1[index])
                    All_Commit_ID_2.append(line.strip())
                except Exception:
                    print 'Exception:\t %s'%line
            index = index + 1
        elif line.strip() == End_Commit_ID:
            start_Flag = 0
            print 'Enc Commit ID is %s'%line 
            
        elif start_Flag == 1:
            print line 
            if check_P('ABCDEFHIG',All_1[index]):
                try:
                    temp_line = re.search(r'ABCDEFHIG-[0-9]{5}',All_1[index]).group()
                    All_2.append(temp_line)
                    All_Author_2.append(All_Author_1[index])
                    All_Commit_ID_2.append(line.strip())
                except Exception:
                    print 'Exception:\t %s'%line
                    
            elif check_P('ABCD',All_1[index]):
                try:
                    temp_line = re.search(r'ABCD-[0-9]{5}',All_1[index]).group()
                    All_2.append(temp_line)
                    All_Author_2.append(All_Author_1[index])
                    All_Commit_ID_2.append(line.strip())
                except Exception:
                    print 'Exception:\t %s'%line
                    
            elif check_P('P',All_1[index]):
                try:
                    temp_line = re.search(r'P-[0-9]{5}',All_1[index]).group()
                    All_2.append(temp_line)
                    All_Author_2.append(All_Author_1[index])
                    All_Commit_ID_2.append(line.strip())
                except Exception:
                    print 'Exception:\t %s'%line
            index = index + 1
        else:
            print line
            index = index + 1
    if branch_1_or_branch_2 == "branch_1":
        for line in All_Commit_ID_2:
            All_Commit_ID_branch_1.append(line)
        for line in All_2:
            All_branch_1.append(line)
        for line in All_Author_2:
            All_Author_branch_1.append(line)
    else:
        for line in All_Commit_ID_2:
            All_Commit_ID_branch_2.append(line)
        for line in All_2:
            All_branch_2.append(line)
        for line in All_Author_2:
            All_Author_branch_2.append(line)
    print All_Commit_ID_2
    print All_Author_2
    print All_2

def get_branch_1_Tag():
    hostname = '198.168.1.107'  
    port = 22  
    username = 'root'  
    password = '密码' 
    tag = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command ('cd /root/branch_1_sync/branch_1_Firmware \n ls ./ | tail -1 \n')	
    for line in stdout:
        line = re.search(r'[0-9]{5}_00.[0-9]{10}',line).group() 
        print(u'branch_1 tag is %s!'%line)
        tag = line
    s.close() 
    return tag
    
def get_branch_2_Tag():
    hostname = '198.168.1.107'  
    port = 22  
    username = 'root'  
    password = '密码' 
    tag = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command ('cd /root/branch_2_sync/branch_2_Firmware \n ls ./ | tail -1 \n')	
    for line in stdout:
        line = re.search(r'[0-9]{5}_00.[0-9]{10}',line).group() 
        print(u'branch_2 tag is %s!'%line)
        tag = line
    s.close() 
    return tag    
    
def get_branch_3_Tag():
    hostname = '198.168.1.107'  
    port = 22  
    username = 'root'  
    password = '密码' 
    tag = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, stderr = s.exec_command ('cd /root/branch_3_sync/branch_3_Firmware \n ls ./ | tail -1 \n')	
    for line in stdout:
        line = re.search(r'[0-9]{5}_00.[0-9]{10}',line).group() 
        print(u'branch_3 tag is %s!'%line)
        tag = line
    s.close() 
    return tag      
    
    
def get_All_Summary(P,branch_1_or_branch_2):
    s = requests.session()
    s.auth = ('账号', '密码')
    r = s.get(u'https://www.*/search?jql=key=%s&fields=summary'%P)
    summary = re.findall(r'summary":"(.+?)"',r.text) #findall输出数组格式，日文显示不正常
    #print summary
    jira_summary = "".join(summary)                          #字符串格式
    if branch_1_or_branch_2 == "branch_1":
        All_Summary_branch_1.append(jira_summary)
    else:
        All_Summary_branch_2.append(jira_summary)
    #print jira_summary #有几率导致gbk打印错误
    #print r.text

   
def main():
    logging.basicConfig(filename='logger_%s.log'%date.today().strftime('%Y%m%d'), level=logging.INFO)
#--------------------------------------------------------    
    tag_branch_1 = get_branch_1_Tag()
    logging.info(u'branch_1 tag is :%s'%tag_branch_1)
    tag_branch_2 = get_branch_2_Tag()
    logging.info(u'branch_2 tag is :%s'%tag_branch_2)
    tag_branch_3 = get_branch_3_Tag()
    logging.info(u'branch_3 tag is :%s'%tag_branch_3)
#--------------------------------------------------------     
    End_Commit_ID_branch_1 = get_End_Commit_ID_branch_1()
    End_Commit_ID_branch_2 = get_End_Commit_ID_branch_2()
    print ("End_Commit_ID_branch_1 is %s"%End_Commit_ID_branch_1)
    print ("End_Commit_ID_branch_2 is %s"%End_Commit_ID_branch_2)

    
    server = jenkins.Jenkins('http://198.168.1.55/jenkins', username='yue_zhang.neu', password='yue_zhang.neu')
    last_build_number = server.get_job_info('I_branch_1_branch_2_V100-PushDev_Slave107_Master')['lastCompletedBuild']['number']
    server.build_job('H_branch_1_branch_2_V100-PushOfficial_Slave107_Master', {'param1': 'branch_1', 'param2': 'DPro-App-UI_161H', 'param3': 'DPro_161H/BR_REL_branch_1_V100', 'param4': '','praram4':'DPro_161H/branch_2'})
    while True:
        sleep(4)
        this_build_number = server.get_job_info('I_branch_1_branch_2_V100-PushDev_Slave107_Master')['lastCompletedBuild']['number']
        if this_build_number == last_build_number:
            continue
        else:
            build_info = server.get_build_info('I_branch_1_branch_2_V100-PushDev_Slave107_Master', this_build_number)
            build_result = build_info['result']
            if build_result == 'SUCCESS':
                print 'push official success!'
                break
            else:
                print 'pushDev failed!'
                break
    Start_Commit_ID_branch_1 = get_End_Commit_ID_branch_1() #没错就是end！
    Start_Commit_ID_branch_2 = get_End_Commit_ID_branch_2() #没错就是end！

    logging.info(u'End_Commit_ID_branch_1 is %s'%End_Commit_ID_branch_1)   
    logging.info(u'Start_Commit_ID_branch_1 is %s'%Start_Commit_ID_branch_1)
    
    logging.info(u'End_Commit_ID_branch_2 is %s'%End_Commit_ID_branch_2)   
    logging.info(u'Start_Commit_ID_branch_2 is %s'%Start_Commit_ID_branch_2)

    get_400_commit()
    get_400_branch_2()
    
    get_Author_P(Start_Commit_ID_branch_1,End_Commit_ID_branch_1,"branch_1")
    get_Author_P(Start_Commit_ID_branch_2,End_Commit_ID_branch_2,"branch_2")
    print ("All author is %s"%All_Author_branch_1)
    print ("All commit is %s"%All_Commit_ID_branch_1)
    print ("All P is %s"%All_branch_1)
    print ("````````````````````````````````````````````````")
    print ("All author is %s"%All_Author_branch_2)
    print ("All commit is %s"%All_Commit_ID_branch_2)
    print ("All P is %s"%All_branch_2)
    

    logging.info(u'All_Commit_ID_branch_1 is %s'%All_Commit_ID_branch_1)
    logging.info(u'All_Author_branch_1 is %s'%All_Author_branch_1)
    logging.info(u'All_branch_1 is %s'%All_branch_1)
    
    logging.info(u'All_Commit_ID_branch_2 is %s'%All_Commit_ID_branch_2)
    logging.info(u'All_Author_branch_2 is %s'%All_Author_branch_2)
    logging.info(u'All_branch_2 is %s'%All_branch_2)
    
    for P in All_branch_1:
        get_All_Summary(P,"branch_1")
    for summary in All_Summary_branch_1:
        print "".join(summary).encode('utf8')
    logging.info(u'All_Summary_branch_1 is %s'%All_Summary_branch_1)
    
    for P in All_branch_2:
        get_All_Summary(P,"branch_2")
    for summary in All_Summary_branch_2:
        print "".join(summary).encode('utf8')
    logging.info(u'All_Summary_branch_2 is %s'%All_Summary_branch_2)

    get_Xls(All_Author_branch_1,All_branch_1,All_Summary_branch_1,"branch_1")
    get_Xls(All_Author_branch_2,All_branch_2,All_Summary_branch_2,"branch_2")
    
    abcdefg = u'*****'   

    
    branch_1 = write_Web(Start_Commit_ID_branch_1,tag_branch_1,All_branch_1,All_Summary_branch_1,abcdefg,'branch_1')
    logging.info(u'branch_1 is %s'%branch_1)
    branch_2 = write_Web(Start_Commit_ID_branch_2,tag_branch_2,All_branch_2,All_Summary_branch_2,abcdefg,'branch_2')
    logging.info(u'branch_2 is %s'%branch_2)
    branch_3 = write_Web(Start_Commit_ID_branch_1,tag_branch_3,All_branch_1,All_Summary_branch_1,abcdefg,'branch_3')
    logging.info(u'branch_3 is %s'%branch_3)
    print 'branch_1 is %s'%branch_1
    print 'branch_2 is %s'%branch_2
    print 'branch_3 is %s'%branch_3

    push_Phase30_Release_Tag(branch_1,branch_2,branch_3,abcdefg,"branch_1")
    push_Phase30_Release_Tag(branch_1,branch_2,branch_3,abcdefg,"branch_2")
    logging.info(u'Push Tag is success!')
    Mail_Phase30(branch_1,branch_2,branch_3,abcdefg)
    logging.info(u'Mail is success!')
    

    
if __name__ == "__main__":  
    main() 
