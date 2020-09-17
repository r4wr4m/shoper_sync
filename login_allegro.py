from functions import *
start = time.time()

if len(sys.argv)>=2:
    domain=sys.argv[1]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain'.format(sys.argv[0]))
    sys.exit(0)

#Load products information
page=None
if domain == pages[0][0]:
            page=pages[0]
if domain == pages[1][0]:
            page=pages[1]
if not page:
    print(Fore.RED+'[!] Page {} not found!'.format(domain))
    sys.exit(1)

print(Fore.BLUE+'###################\nCOPYING STOCKS FROM {} TO ALLEGRO\n###################'.format(page[0]))
allegro_api_login(page)
print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
