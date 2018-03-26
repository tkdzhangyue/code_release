flyingV_zy
====================
Code Release
---------------------
新入职的工作负责每日代码release:通过Git发往远程服务器.并处理邮件和票号信息填写(在一个独立网址填写release信息).
#### 应用: 
+ python2.7 
+ git
+ shell
+ jenkins
+ python_selenium

#### 工作流程:
1. 通过ssh在linux服务器的git上取信息:author,commit ID,commit MSG.
2. 通过python的xlwt和xlrd将以上信息保存为xls格式.
3. 利用selenium在网页进行一系列动作.
4. paramiko控制远程linux服务器在git的主分支上打tag.
5. smtplib发送成功release邮件.

##### 1
 ```python
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
 ```

