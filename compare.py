from functions import *
start = time.time()
products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file=True) #load_data(active_only=False,from_file=False)

#Settings
details=True

print(Fore.BLUE+'###################\nCOMPARING PRODUCTS\n###################')
compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','stock','price','availability_name','delivery_name'],True,details)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))