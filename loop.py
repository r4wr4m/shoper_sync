import os,time
logpath='logs/'

interval=5 #minutes
iteration=0

while True:
    t = time.localtime()
    minute = int(time.strftime('%M',t))
    if minute%interval == 0:
        iteration+=1
        print('Iteration',iteration,'started ',end='')
        if not os.path.isdir(logpath):
            os.mkdir(logpath)
        filename = logpath + time.strftime('%Y%m%d_%H%M_'+str(iteration).zfill(5)+'.txt',t)
        os.system('python3 sync_stock.py change allegro 2>&1 >'+filename)
        print(filename)
        #os.system('date>'+filename)
    time.sleep(60)
