from functions import *
start = time.time()

past_data_filename='past_data'
from_file=False
active_only=False
change=False

if 'offline' in sys.argv:
    from_file=True
if 'active' in sys.argv:
    active_only=True
if 'change' in sys.argv:
    change=True
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
products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)
past_name_dict = create_name_dict(past_products,'PAST DATA') #creating dictionary without duplicates, name oriented

print(Fore.BLUE+'###################\nCOMPARING DATA\n###################')
#COMPARING DATA WITHOUT STOCKS
products1_past = compare_products(products[0],past_products,name_dict1,past_name_dict,pages[0][0],'PAST DATA',availabilities[0],past_availabilities,deliveries[0],past_deliveries,['active','price','availability_name','delivery_name'],False,False)
products2_past = compare_products(past_products,products[1],past_name_dict,name_dict2,'PAST DATA',pages[1][0],past_availabilities,availabilities[1],past_deliveries,deliveries[1],['active','price','availability_name','delivery_name'],False,False)
products1_product2 = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','price','availability_name','delivery_name'],False,False)

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

data_updated = False
for name in past_name_dict:
    stock1=name_dict1[name]['stock']
    stock2=name_dict2[name]['stock']
    stockp=past_name_dict[name]['stock']
    if (stock1 < stockp) and (stock2 < stockp): #ORDERS IN BOTH SHOPS
        stock = stockp - (stockp-stock1) - (stockp-stock2)
        print('[i] Orders in both shops (stock in the past: {})'.format(stockp))
        if stock >=0:
            print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[0][0],'stock',stock1,stock),end='')
            if change:
                if update_value(pages[0][0],pages[0][3],name_dict1[name]['id'],'stock',stock):
                    print(Fore.GREEN + ' DONE')
                    for product in past_products: #update past_products
                        if product['name']==name:
                            product['stock']=stock
                    data_updated=True
                else:
                    print(Fore.RED + ' ERROR')
            else:
                print('') 
            print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[1][0],'stock',stock2,stock),end='')
            if change:
                if update_value(pages[1][0],pages[1][3],name_dict2[name]['id'],'stock',stock):
                    print(Fore.GREEN + ' DONE')
                    for product in past_products: #update past_products
                        if product['name']==name:
                            product['stock']=stock
                    data_updated=True
                else:
                    print(Fore.RED + ' ERROR')
            else:
                print('')   
        else:
            print(Fore.RED + '[!] ERROR: Sold more than in stock!!!')
            print('[i] Clearing stocks')
            #CLEARING STOCKS
            print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[1][0],'stock',stock2,0),end='')
            if change:
                if update_value(pages[1][0],pages[1][3],name_dict2[name]['id'],'stock',0):
                    print(Fore.GREEN + ' DONE')
                    for product in past_products: #update past_products
                        if product['name']==name:
                            product['stock']=0
                    data_updated=True
                else:
                    print(Fore.RED + ' ERROR')
            else:
                print('')
            print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[0][0],'stock',stock1,0),end='')
            if change:
                if update_value(pages[0][0],pages[0][3],name_dict1[name]['id'],'stock',0):
                    print(Fore.GREEN + ' DONE')
                    for product in past_products: #update past_products
                        if product['name']==name:
                            product['stock']=0
                    data_updated=True
                else:
                    print(Fore.RED + ' ERROR')
            else:
                print('')            
    elif (stock1 < stockp) and (stock2 == stockp):  #ORDERS IN SHOP1
        print('[i] Orders only in ' + pages[0][0])
        print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[1][0],'stock',stock2,stock1),end='')
        if change:
            if update_value(pages[1][0],pages[1][3],name_dict2[name]['id'],'stock',stock1):
                print(Fore.GREEN + ' DONE')
                for product in past_products: #update past_products
                    if product['name']==name:
                        product['stock']=stock1
                data_updated=True
            else:
                print(Fore.RED + ' ERROR')
        else:
            print('')
    elif (stock2 < stockp) and (stock1 == stockp): #ORDERS IN SHOP2
        print('[i] Orders only in ' + pages[1][0])
        print('[i] Changing product {} in {} {} attribute: {}->{}'.format(name,pages[0][0],'stock',stock1,stock2),end='')
        if change:
            if update_value(pages[0][0],pages[0][3],name_dict1[name]['id'],'stock',stock2):
                print(Fore.GREEN + ' DONE')
                for product in past_products: #update past_products
                    if product['name']==name:
                        product['stock']=stock2
                data_updated=True
            else:
                print(Fore.RED + ' ERROR')
        else:
            print('')
    else: #ERROR
        if stock1 == stockp and stock2 == stockp and stock1 == stock2:
            pass #stock synced
        else:
            print(Fore.RED+'[-] UNKNOWN STOCK ERROR: {} {}: {} {} :{} PAST DATA: {}'.format(name,pages[0][0],stock1,pages[1][0],stock2,stockp))

if data_updated:
    save_products((past_products,past_availabilities,past_deliveries),past_data_filename)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
