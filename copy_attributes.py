from functions import *
start = time.time()
products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file=False) #load_data(active_only=False,from_file=False)

#Settings
print_only=True

print(Fore.BLUE+'###################\nCOPYING ATTRIBUTES FROM {} TO {}\n###################'.format(pages[0][0],pages[1][0]))
changes=0
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'active',print_only)
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'stock',print_only)
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'price',print_only)
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'availability_name',print_only,availabilities[1])
changes += copy_attribute(pages[0],pages[1],name_dict1,name_dict2,'delivery_name',print_only,deliveries[1])
print('Changes:',changes)

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))