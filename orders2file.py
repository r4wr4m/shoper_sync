from functions import *

from_file=False
active_only=False
if 'offline' in sys.argv:
    from_file=True
if 'active' in sys.argv:
    active_only=True

if len(sys.argv)>=5:
    domain=sys.argv[1]
    date_from=sys.argv[2]
    date_to=sys.argv[3]
    filename=sys.argv[4]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain date_from date_to filename [offline] [active]'.format(sys.argv[0]))
    sys.exit(0)


start = time.time()
    
#Loading product information (needed for passport numbers)
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

token = api_login(page[0],page[1],page[2])

table_rows=[['NAZWA ODBIORCY','NAZWA ROŚLINY','PASZPORT','CENA','ILOŚĆ','JEDNOSTKA','STATUS','DATA ZMIANY STATUSU','DATA DOSTAWY','INFO']]
orders = get_orders(page[0],token,date_from,date_to)
for order in orders:
    clientname=''
    if order['company'] != '':
        clientname = order['company']
    if order['firstname'] !='':
        if clientname != '':
            clientname += ' | '
        clientname += order['firstname'] + ' ' + order['lastname']
    status_date=order['status_date']
    confirm_date=order['confirm_date']
    delivery_date=order['delivery_date']
    status_id=order['status']
    
    ordered_products = get_ordered_products(page[0],token,order['order_id'])
    for product in ordered_products:
        price=product['price']
        quantity=product['quantity']
        unit=product['unit']

        passport=''
        for p in products: 
            if p['id']==product['product_id']:
                passport = p['passport']
                
                break
        info=''
        if product['set']:
            info = 'ZESTAW'
        if product['part_of_set']:
            info = 'CZĘŚĆ ZESTAWU'
        table_rows.append([clientname,product['name'],passport,price,quantity,unit,status_id,status_date,delivery_date,info])
#for row in table_rows:
#    print(row)

save_rows2xls(table_rows,filename)
print(Fore.GREEN+'[+] File {}.xls saved.'.format(filename))


print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
