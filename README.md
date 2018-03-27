flyingV_zy
====================
Code Release
---------------------
新入职的工作负责每日代码release:通过Git发往远程服务器.并处理邮件和票号信息.简直就是在感召我用pyhton做这个项目.
###### 已经根据公司信息安全守则进行了修改.
#### 应用: 
+ python2.7 
	* selenium
	* smtplib
	* xlwt
	* xlrd
	* paramiko
	* python-jenkins
+ git
+ shell
+ jenkins

#### 工作流程:
1. 在linux操作系统,通过ssh取得git服务器上信息.
2. 通过python的xlwt和xlrd将以上信息格式化为xls.
3. 利用selenium在进行一系列动作.
4. paramiko控制远程linux服务器在git的主分支上打标签.
5. smtplib群发邮件.

##### STEP.1
结合python-paramiko和git命令, 取得前一日发布的EndCommitId和今日的StartCommitId. 两次调用```get_End_Commit_ID_branch_1()```之间, 使用jenkins的任务, 将开发分支提交merge到主分支上,得到本日发布的所有提交CommitId. 在这里由Jenkins做这个动作, 是因为项目组之前全部任务都跑在Jenkins上, 是半自动运行, Python的加入让工作彻底的编程全自动.
```python
 import paramiko
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
#### STEP.2
创建当天日期的文件夹,拷贝一份example.xls, 将STEP.1取得的信息按照既定格式填写. 在使用Python之前, 这一步是最繁琐的, 需要人工一条一条从git服务器拷贝.
```python
def get_Xls(author,p,summary,a_or_b):
    if a_or_b == "ARH":
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
```
#### STEP.3
Python-selenium本是应用于网络爬虫和自动化测试中. Selenium按照既定流程进行按钮点击和文本输入, 解决了之前大量的人工工作量.
核心是函数```do()```:
1. 在click或者input动作之前加入判断元素是否存在.
2. try_except_else解决:元素被遮挡而不可点击状态
```python
def write_ARH_Jira(commit,tag,All_P,All_Summary,x,a_b_c):
    #DUE-DATE
    Due_date = strftime("%d/%b/%y",localtime())   
    driver = webdriver.Chrome()
    driver.get(u'https://www.*') 
    driver.find_element_by_name('UserID').send_keys(u"账号")
    driver.find_element_by_name('Password').send_keys(u"密码") 
    driver.find_element_by_name(u"btnSubmit").click() 
    action_list = []
    name_list = []
    id_list = []
    def do(id,name,action):
        failed_number = 0
        while True:
            try:
                if driver.find_element('%s'%id,'%s'%name):
                    if action == 'click':
                        driver.find_element('%s'%id,'%s'%name).click()
                    else:
                        driver.find_element('%s'%id,'%s'%name).send_keys(Keys.CONTROL,'a')
                        driver.find_element('%s'%id,'%s'%name).send_keys(Keys.CONTROL,'x')
                        driver.find_element('%s'%id,'%s'%name).send_keys('%s'%action)
            except Exception,e:
                print 'str(Exception):\t', str(Exception)
                print 'repr(e):\t', repr(e)
                print u'点击%s异常,failed_number = %s!'%(name,failed_number)
                failed_number = failed_number + 1
                if failed_number ==100:
                    if action_list.pop() == 'click':
                        driver.find_element('%s'%id_list.pop(),'%s'%name_list.pop()).click()
                    else:
                        driver.find_element('%s'%id_list.pop(),'%s'%name_list.pop()).send_keys(Keys.CONTROL,'a')
                        driver.find_element('%s'%id_list.pop(),'%s'%name_list.pop()).send_keys(Keys.CONTROL,'x')
                        driver.find_element('%s'%id_list.pop(),'%s'%name_list.pop()).send_keys('%s'%action_list.pop())
                sleep(1)
            else:
                failed_number = 0
                action_list.append('%s'%action)
                name_list.append('%s'%name)
                id_list.append('%s'%id)
                print action_list
                print name_list
                print id_list
                break
            
#---clone--------------------------------------------------------------------------------------------------------       
    do('id','opsbar-operations_more','click')
    do('id','clone-issue','click')
    title = '[%s][title]%s'%(a_b_c,Due_date)
    do('name','Create','click')
#---edit--------------------------------------------------------------------------------------------------------
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    do('id','edit-issue','click')
    driver.find_element('class name','ignore-inline-attach').send_keys(u'C:\dir_for_python\%s_P****3.0\title.xls'%date.today().strftime('%Y-%m-%d'))
    do('name','summary',title.decode('utf8'))
    description = []
    description.append(u'string')
    description.append(u'string\n%s\nstring\n'%commit)
    i = 0
    for line in All_p:
        p = ''.join(All_p[i]).encode('utf8')
        summary = ''.join(All_Summary[i]).encode('utf8')
        p_summary = p + summary
        i += 1 
        description.append(u'%s\n'%p_summary.decode('utf8'))
    description.append(u'\n string s string'%tag)
    description_1 = ''.join(description)
    do('name','description',description_1)
    do('id','duedate',Due_date)
    sleep(3) 
    do('id','edit-issue-submit','click')
    driver.switch_to.window(windows[-1])
    do('id','action_id_4','click')
    do('id','action_id_5','click')
    do('id','issue-workflow-transition-submit','click')
#----------------------------add comment-----------------    
    do('id','footer-comment-button','click')
    riqi = date.today().strftime('%Y%m%d')    
    do('id','comment',u'string%s%s%s%s'%(riqi,x,riqi,x,riqi,x))
    do('id','issue-comment-add-submit','click')
#--------------------------------------------------------  
    p = driver.find_element_by_id('key-val').get_attribute(u'data-issue-key')     
    sleep(5)
    return p
```
#### STEP.4
略
#### STEP.5
```python
def Mail(a,b,c,d):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    from_addr = 'yue_zhang.***@company.com'
    password = '1qaz!QAZ'
    to_addr = ['yue_zhang.***@company.com']
    #to_addr = ['yue_zhang.***@company.com']
    smtp_server = 'smtp.company.com'
    riqi = date.today().strftime('%Y%m%d')
    msg = MIMEText(u'内容', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'<%s>' % from_addr)
    msg['To'] = u'yue_zhang.***@company.com'
    msg['Subject'] = Header(u'[%s][发布成功]'%date.today().strftime('%Y-%m-%d'), 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 587)
    server.starttls() #20171012
    server.set_debuglevel(1)
    server.login('yue_zhang.***', password)
    server.sendmail(from_addr, to_addr, msg.as_string())# to_addr是list
    server.quit()
```
