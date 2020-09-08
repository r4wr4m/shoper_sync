from functions import *

if len(sys.argv)==5:
    domain=sys.argv[1]
    date_from=sys.argv[2]
    date_to=sys.argv[3]
    filename=sys.argv[4]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain date_from date_to filename'.format(sys.argv[0]))
    sys.exit(0)


filename='products'

start = time.time()
    

page=None
for p in pages:
       if domain == p[0]:
        page=p
if not page:
    print(Fore.RED+'[!] Page {} not found!'.format(domain))
    sys.exit(1)

token = api_login(page[0],page[1],page[2])

#order_info = get_order_info(page[0],token,9302)
#ordered_products = get_ordered_products(page[0],token,9302)
table_rows=[]
orders = get_orders(page[0],token,date_from,date_to)
for order in orders:
    ordered_products = get_ordered_products(page[0],token,order['order_id'])
    
 #save2xls([product_names],filename)
    #print(Fore.GREEN+'[+] File {}.xls saved.'.format(filename))


print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))