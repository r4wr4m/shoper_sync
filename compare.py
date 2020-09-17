from functions import *
from_file=False
details=False
active_only=False
print_sets=False

if 'offline' in sys.argv:
    from_file=True
if 'details' in sys.argv:
    details=True
if 'active' in sys.argv:
    active_only=True
if 'sets' in sys.argv:
    print_sets=True


start = time.time()
products,availabilities,deliveries,name_dict1,name_dict2,auctions = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)

#COMPARING PRODUCTS
compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],['active','stock','price','availability_name','delivery_name'],True,details)

if print_sets:
    print_sets_of_products(products[0],products[1],pages[0][0],pages[1][0]) #prints sets and stocks of products



print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))