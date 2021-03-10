from functions import *
from_file=False
active_only=False
change=False


if 'offline' in sys.argv:
    from_file=True
if 'active' in sys.argv:
    active_only=True
if 'change' in sys.argv:
    change=True

if len(sys.argv)>=2:
    domain=sys.argv[1]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain [offline] [active] [change]'.format(sys.argv[0]))
    sys.exit(0)

#Load products information
products,availabilities,deliveries,name_dict1,name_dict2,auctions = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)
page=None
if domain == pages[0][0]:
            page=pages[0]
            products = products[0]
            name_dict=name_dict1
if domain == pages[1][0]:
            page=pages[1]
            products = products[1]
            name_dict=name_dict2
if not page:
    print(Fore.RED+'[!] Page {} not found!'.format(domain))
    sys.exit(1)

filename='products'

start = time.time()
#if not from_file:
#    page[3] = api_login(page[0],page[1],page[2]) #TOKEN1

#Read file with product names and passports
table = read_rows(filename)
for row in table: #row = [product_name,passport]
    product=name_dict[row[0]]
    if len(row) == 1:
        set_passport(page[0],page[3],product,'',change)
    else:
        set_passport(page[0],page[3],product,row[1],change)
        
print(Fore.GREEN+'[+] Done')
print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
