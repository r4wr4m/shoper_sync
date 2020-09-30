from functions import *
start = time.time()

past_data_filename='past_data'
from_file=False
active_only=False
change=False
allegro=False

pythoncmd=''
for cmd in ['python3','python']:
    try:
        p = subprocess.Popen([cmd, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        outerr=(out+err).decode("utf-8") 
        if outerr[:6]=='Python':
            if outerr[7]=='3':
                pythoncmd = cmd
    except:
        pass
if pythoncmd=='':
    print('Python 3 not found!')
    sys.exit(1)

if 'offline' in sys.argv:
    from_file=True
if 'active' in sys.argv:
    active_only=True
if 'change' in sys.argv:
    change=True
if 'allegro' in sys.argv:
    allegro=True
print_only=not change
if 'delete' in sys.argv:
    delete_past_data(past_data_filename)


print(Fore.BLUE+'###################\nLOADING PAST DATA\n###################')
#############################################
######### PAST DATA DOESN'T EXIST ###########
#############################################
if not os.path.isfile('data/'+past_data_filename): # IF PAST DATA DOESN'T EXIST
    print(Fore.RED+'[-] File data/{} doesn\'t exit'.format(past_data_filename))
    create_past_data(past_data_filename,from_file,active_only)
    
#############################################
############ PAST DATA EXISTS ###############
#############################################
past_products,past_availabilities,past_deliveries = load_products(past_data_filename)
products,availabilities,deliveries,name_dict1,name_dict2,auctions = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)
past_name_dict = create_name_dict(past_products,'PAST DATA') #creating dictionary without duplicates, name oriented

print(Fore.BLUE+'###################\nCOMPARING DATA\n###################')
#COMPARING DATA WITHOUT STOCKS
products1_past = compare_products(products[0],past_products,name_dict1,past_name_dict,pages[0][0],'PAST DATA',availabilities[0],past_availabilities,deliveries[0],past_deliveries,['active','availability_name','delivery_name'],False,False)
products2_past = compare_products(past_products,products[1],past_name_dict,name_dict2,'PAST DATA',pages[1][0],past_availabilities,availabilities[1],past_deliveries,deliveries[1],['active','availability_name','delivery_name'],False,False)
products1_product2 = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','availability_name','delivery_name'],False,False)

if products1_past and products2_past and products1_product2: #PRODUCT INFORMATION SYNCED
    print(Fore.GREEN+'[+] Product information is synchronized')
else:
    print(Fore.RED+'[+] Products information is not synchronized (synchronize information first)')
    sys.exit(1)

#COMPARING STOCKS
stock1_stockp = compare_products(products[0],past_products,name_dict1,past_name_dict,pages[0][0],'PAST DATA',availabilities[0],past_availabilities,deliveries[0],past_deliveries,['stock'],False,False)
stock2_stockp = compare_products(past_products,products[1],past_name_dict,name_dict2,'PAST DATA',pages[1][0],past_availabilities,availabilities[1],past_deliveries,deliveries[1],['stock'],False,False)
stock1_stock2 = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['stock'],False,False)
if stock1_stockp and stock2_stockp and stock1_stock2: #STOCKS INFORMATION SYNCED
    print(Fore.GREEN+'[+] Stock information is synchronized')
    sys.exit(1)
else:
    print(Fore.RED+'[-] Stock information is not synchronized')

#SYNCHRONIZING STOCKS INFORMATION
changes_file = changes_filename()
write2file(changes_file,'CHANGING VALUES: '+str(change))
email_text=""
data_updated = True
for name in past_name_dict:
    stock1=name_dict1[name]['stock']
    stock2=name_dict2[name]['stock']
    stockp=past_name_dict[name]['stock']
    if (stock1 < stockp) and (stock2 < stockp): #ORDERS IN BOTH SHOPS
        stock = stockp - (stockp-stock1) - (stockp-stock2)
        print(Fore.YELLOW + '[i] Orders in both shops - product: {} (stock in the past: {})'.format(name,stockp))
        if stock >=0:
            d = change_stock(past_products,name_dict1,name,pages[0],stock1,stock,change,changes_file)
            data_updated = data_updated and d
            dd = change_stock(past_products,name_dict2,name,pages[1],stock2,stock,change,changes_file)
            data_updated = data_updated and d and dd
        else:
            text = '[!] ERROR: Sold more than in stock ({})!!! (product: {})'.format(stock,name)
            print(Fore.RED + text)
            email_text+=text+'\n'
            print('[i] Clearing stocks')
            #CLEARING STOCKS
            d = change_stock(past_products,name_dict1,name,pages[0],stock1,0,change,changes_file)
            data_updated = data_updated and d
            dd = change_stock(past_products,name_dict2,name,pages[1],stock2,0,change,changes_file)
            data_updated = data_updated and d and dd
    elif (stock1 < stockp) and (stock2 == stockp):  #ORDERS IN SHOP1
        print(Fore.YELLOW + '[i] Orders only in {} - product: {}'.format(pages[0][0],name))
        d = change_stock(past_products,name_dict2,name,pages[1],stock2,stock1,change,changes_file)
        data_updated = data_updated and d
    elif (stock2 < stockp) and (stock1 == stockp): #ORDERS IN SHOP2
        print(Fore.YELLOW + '[i] Orders only in {} - product: {}'.format(pages[1][0],name))
        d = change_stock(past_products,name_dict1,name,pages[0],stock1,stock2,change,changes_file)
        data_updated = data_updated and d
    elif (stock1 > stockp) and (stock2 == stockp):  #STOCK INCREASED IN SHOP1
        print(Fore.YELLOW + '[i] Stocked increased in {} - product: {}'.format(pages[0][0],name))
        d = change_stock(past_products,name_dict2,name,pages[1],stock2,stock1,change,changes_file)
        data_updated = data_updated and d
    elif (stock2 > stockp) and (stock1 == stockp): #STOCK INCREASED IN SHOP2
        print(Fore.YELLOW + '[i] Stocked increased in {} - product: {}'.format(pages[1][0],name))
        d = change_stock(past_products,name_dict1,name,pages[0],stock1,stock2,change,changes_file)
        data_updated = data_updated and d
    elif (stock1 > stockp) and (stock2 < stockp):  #STOCK INCREASED IN SHOP1 AND DECREASED IN SHOP2
        stock = stock1 - (stockp-stock2)
        text = '[i] Stocked increased in {} ({}->{}) AND decreased in {} ({}->{})- product: {}. New stock: {}'.format(pages[0][0],stockp,stock1,pages[1][0],stockp,stock2,name,stock)
        print(Fore.YELLOW + text)
        email_text+=text+'\n'
        d = change_stock(past_products,name_dict2,name,pages[0],stock1,stock,change,changes_file)
        dd = change_stock(past_products,name_dict2,name,pages[1],stock2,stock,change,changes_file)
        data_updated = data_updated and d
    elif (stock2 > stockp) and (stock1 < stockp): #STOCK INCREASED IN SHOP2 AND DECREASED IN SHOP1
        stock = stock2 - (stockp-stock1)
        text = '[i] Stocked increased in {} ({}->{}) AND decreased in {} ({}->{})- product: {}. New stock: {}'.format(pages[1][0],stockp,stock2,pages[0][0],stockp,stock1,name,stock)
        print(Fore.YELLOW + text)
        email_text+=text+'\n'
        d = change_stock(past_products,name_dict1,name,pages[0],stock1,stock,change,changes_file)
        dd = change_stock(past_products,name_dict1,name,pages[1],stock2,stock,change,changes_file)
        data_updated = data_updated and d
    else: #ERROR
        if stock1 == stockp and stock2 == stockp and stock1 == stock2:
            pass #stock synced
        else:
            text = '[-] UNKNOWN STOCK ERROR: {} {}: {} {} :{} PAST DATA: {}'.format(name,pages[0][0],stock1,pages[1][0],stock2,stockp)
            print(Fore.RED+text)
            email_text+=text+'\n'
if data_updated:
    save_products((past_products,past_availabilities,past_deliveries),past_data_filename)
if email_text != '' and mail_creds[0] != '' and mail_creds[1] != '':
    send_mail(mail_creds,to,email_text)

if allegro:
    args = ''
    if from_file:
        args += ' offline'
    if change:
        args += ' change'
    cmd1 = pythoncmd + ' copy_auction_stocks.py ' + pages[0][0] + args
    cmd2 = pythoncmd + ' copy_auction_stocks.py ' + pages[1][0] + args
    print(cmd1)
    print(cmd2)
    os.system(cmd1)
    os.system(cmd2)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
