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

products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file,active_only) #load_data(active_only=False,from_file=False)

#Settings

print(Fore.BLUE+'###################\nCOPYING ATTRIBUTES FROM {} TO {}\n###################'.format(pages[0][0],pages[1][0]))
changes=0
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'active',print_only)
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'stock',print_only)
#changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'price',print_only)
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'availability_name',print_only,availabilities[1])
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'delivery_name',print_only,deliveries[1])
print('Changes:',changes)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
