import os,time
from functions import *
logpath='logs/'

interval=20 #minutes
iteration=0
file_number=len(os.listdir(logpath))

while True:
    t = time.localtime()
    minute = int(time.strftime('%M',t))
    if minute%interval == 0:
        iteration+=1
        print('Iteration',iteration,'started')
        if not os.path.isdir(logpath):
            os.mkdir(logpath)
        
        new_file_number=len(os.listdir(logpath))
        if new_file_number - file_number == 0:
            send_mail(mail_creds,to,"SKRYPT SIĘ ZACIĄŁ PANIE!")
            break
        file_number = new_file_number
    time.sleep(60)
