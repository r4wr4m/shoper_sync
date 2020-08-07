from functions import *
start = time.time()


products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file=True) #load_data(active_only=False,from_file=False)



#LOADING PAST_DATA
past_data_path='data/past_data'
if os.path.isfile(past_data_path):
    past_products,past_availabilities,past_deliveries = load_products(stocks)
else:
    print(Fore.RED+'[-] File {} doesn\'t exit'.format(past_data_path))
    equal = compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','stock','price','availability_name','delivery_name'],True,False)
    if equal:
        save_products((products[0],availabilities[0],deliveries[0]),past_data_path)
        print(Fore.GREEN+'[+] Products information is synchronized, file {} created'.format(past_data_path))
    else:
        print(Fore.RED+'[+] Products information is not synchronized, cannot create file {}'.format(past_data_path))
    print('[i] Exiting')
    sys.exit(1)

api_get_products(pages[0][0],pages[0][3],availabilities[0],deliveries[0],active_only),



    






print(Fore.BLUE+'###################\nCOMPARING PRODUCTS\n###################')

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))