from smtplib import SMTP_SSL

host = 'imap.gmail.com'
port = 465
username = 'will.coding.test@gmail.com'
password = 'YOUR_PASSWORD'
fromAddr = 'will.coding.test@gmail.com'
toAddrs = ['will.coding.test@gmail.com']
msg = 'Hi Test2'

server = SMTP_SSL(host, port)
server.login(username, password)
server.set_debuglevel(1)
server.sendmail(fromAddr, toAddrs, msg)
server.quit()

