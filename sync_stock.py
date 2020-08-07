from functions import *
start = time.time()

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


print(Fore.BLUE+'###################\nLOADING DATA\n###################')
past_data_path='data/past_data'
if not os.path.isfile(past_data_path): # IF PAST DATA DOESN'T EXIST
    print(Fore.RED+'[-] File {} doesn\'t exit'.format(past_data_path))
    products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)
    equal = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','stock','price','availability_name','delivery_name'],True,False)
    if equal: #CREATE PAST DATA
        save_products((products[0],availabilities[0],deliveries[0]),past_data_path)
        print(Fore.GREEN+'[+] Products information is synchronized, file {} created'.format(past_data_path))
    else: #EXIT
        print(Fore.RED+'[-] Products information is not synchronized, cannot create file {}'.format(past_data_path))
    print('[i] Exiting')
    sys.exit(1)

past_products,past_availabilities,past_deliveries = load_products(past_data_path)
products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)
past_name_dict = create_name_dict(products[0],pages[0][0]) #creating dictionary without duplicates, name oriented
#COMPARE PRODUCTS

#COMPARING DATA
products1_past = compare_products(products[0],past_products,name_dict1,past_name_dict,pages[0][0],'PAST DATA',availabilities[0],past_availabilities,deliveries[0],past_deliveries,['active','stock','price','availability_name','delivery_name'],True,False)
products2_past = compare_products(past_products,products[1],past_name_dict,name_dict2,'PAST DATA',pages[1][0],past_availabilities,availabilities[1],past_deliveries,deliveries[1],['active','stock','price','availability_name','delivery_name'],True,False)
products1_product2 = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','stock','price','availability_name','delivery_name'],True,False)



if products1_past and products2_past and products1_product2: #ALL THE SAME
    pass # OK, exit
if products1_products2 and products1_past and not products2_past: #PAST AND P1 SAME, P2 DIFFERENT
    pass
if products1_products2 and products2_past and not products1_past: #PAST AND P2 SAME, P2 DIFFERENT
    pass
if not products1_products2 and not products2_past and not products1_past: #PAST, P1, P2 DIFFERENT
    pass

    



print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))