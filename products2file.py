from functions import *
from_file=False
active_only=False


if 'offline' in sys.argv:
    from_file=True
if 'active' in sys.argv:
    active_only=True


filename='products'

start = time.time()
products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)

if compare_products(products[0],products[1],name_dict1,name_dict2,pages[0][0],pages[1][0],availabilities[0],availabilities[1],deliveries[0],deliveries[1],[],False,False):
	product_names=[]
	for product in products[0]:
		product_names.append(product['name'])
	save_columns2xls([product_names],filename)
	print(Fore.GREEN+'[+] File {}.xls saved.'.format(filename))
else:
	print(Fore.RED+'[-] Different products in shops')

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))