# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep,strftime,localtime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys  
from datetime import date





def write_Website(commit,tag,All_P,All_Summary,x,a_b_c):
    
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
    
    driver.find_element('class name','ignore-inline-attach').send_keys(u'C:\dir_for_python_jira\%s_P****3.0\title.xls'%date.today().strftime('%Y-%m-%d'))

    
    do('name','summary',title.decode('utf8'))

    description = []
    description.append(u'string')
    description.append(u'string\n%s\nstring\n'%commit)
    i = 0
    for line in All_P:
        P = ''.join(All_P[i]).encode('utf8')
        summary = ''.join(All_Summary[i]).encode('utf8')
        P_summary = P + summary
        i += 1 
        description.append(u'%s\n'%P_summary.decode('utf8'))
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
    P = driver.find_element_by_id('key-val').get_attribute(u'data-issue-key')     
    sleep(5)
    return P

    
  
def main():
    
    
    
if __name__ == "__main__":  
    main() 
