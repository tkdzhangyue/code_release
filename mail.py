# -*- coding: utf-8 -*-
from datetime import *  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

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
    
   
def main():
    
    
    
if __name__ == "__main__":  
    main() 
