from functions import *
start = time.time()

from_file=False
change=False

if 'offline' in sys.argv:
    from_file=True
if 'change' in sys.argv:
    change=True
print_only=not change

if len(sys.argv)>=2:
    domain=sys.argv[1]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain [offline] [change] '.format(sys.argv[0]))
    sys.exit(0)


products,availabilities,deliveries,name_dict1,name_dict2,auctions = load_data(from_file,False) 
page=None
if domain == pages[0][0]:
            page=pages[0]
            auctions = auctions[0]
            products=products[0]
            name_dict = name_dict1
if domain == pages[1][0]:
            page=pages[1]
            auctions = auctions[1]
            products=products[1]
            name_dict = name_dict2
if not page:
    print(Fore.RED+'[!] Page {} not found!'.format(domain))
    sys.exit(1)



#Settings
changes_file = changes_filename(domain)
write2file(changes_file,'CHANGING VALUES: '+str(change))
print(Fore.BLUE+'###################\nCOPYING STOCKS FROM {} TO ALLEGRO\n###################'.format(page[0]))
changes=0

allegro_auctions = allegro_get_auctions(page).json()
if 'count' in allegro_auctions and allegro_auctions['count'] > 0:
    print(Fore.GREEN+'[+] Downloaded {} auctions'.format(len(allegro_auctions['offers'])))
    allegro_auctions=allegro_auctions['offers']
    print("[i] Auctions on Shoper:", len(auctions))
    print("[i] Auctions on Allegro:", len(allegro_auctions))
    for auction in auctions: #shoper_auctions
        paired=False
        for allegro_auction in allegro_auctions: 
            if auction['real_auction_id'] == allegro_auction['id']:
                product={}
                for p in products:
                    if int(p['id']) == int(auction['product_id']):
                        product=p
                        break
                paired = True
                shoper_stock = product['stock']
                allegro_stock = allegro_auction['stock']['available']
                active = allegro_auction["publication"]["status"]
                if active == "ENDED":
                    allegro_stock = 0
                if int(shoper_stock) != int(allegro_stock):
                    changes+=1
                    if active == "ENDED":
                        text='[i] {} Changing stock in Allegro ({}) {}->{} ({}) https://allegro.pl/oferta/{}'.format(changes,page[0],allegro_stock,shoper_stock,product['name'],auction['real_auction_id'])
                        text+='\n[i] Activating auction - stock may not be updated!'
                    else:
                        text='[i] {} Changing stock in Allegro ({}) {}->{} ({}) https://allegro.pl/oferta/{}'.format(changes,page[0],allegro_stock,shoper_stock,product['name'],auction['real_auction_id'])
                    print(text,end='')
                    write2file(changes_file,text)
                    if change:
                        if allegro_set_stock(page,auction['real_auction_id'],allegro_stock,shoper_stock):
                            print(Fore.GREEN+' DONE')
                        else:
                            print(Fore.RED+' ERROR') 
                    else:
                        print()
                break
        if not paired:
            print(Fore.RED+'[-] Auction ' + auction['real_auction_id'] + ' not found on Allegro')





print('Changes:',changes)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
