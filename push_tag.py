# -*- coding: utf-8 -*-
from datetime import *  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import re
import requests
import paramiko
import jenkins,time


def push_Tag(a,b,c,d,a_or_b):
    hostname = '192.168.1.158'  
    port = 22  
    username = 'root'  
    password = '密码' 
    tag = ''
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    riqi = date.today().strftime('%Y%m%d')
    if a_or_b == "a":
        stdin, stdout, stderr = s.exec_command ('cd /home/pwd\n git reset --hard HEAD \n git checkout branch_1\n git pull --rebase\ngit tag -a "RELEASE_%s_28" -m "\nTYPE=*\nBRANCH=branch_1\nMODEL=***\nRELEASE_TARGET=%s\nBUILD_TARGET=***\nTICKET=%s\n"\n git tag -a "RELEASE_%s_30" -m "\nTYPE=*\nBRANCH=branch_2\nMODEL=***\nRELEASE_TARGET=%s\nBUILD_TARGET=***\nTICKET=%s\n"\ngit push origin RELEASE_%s_28\ngit push origin RELEASE_%s_30\n'%(riqi,d,a,riqi,d,c,riqi,riqi))	
    else:
        stdin, stdout, stderr = s.exec_command ('cd /home/pwd\n git reset --hard HEAD \n git checkout branch_3\n git pull --rebase\ngit tag -a "RELEASE_%s_29" -m "\nTYPE=*\nBRANCH=branch_3\nMODEL=***\nRELEASE_TARGET=%s\nBUILD_TARGET=***\nTICKET=%s\n"\n git push origin RELEASE_%s_29\n'%(riqi,d,b,riqi))	
    
    for line in stdout:
        print line
    for line in stderr:
        print line
    s.close() 
    return tag





def main():
    
    
if __name__ == "__main__":  
    main() 
