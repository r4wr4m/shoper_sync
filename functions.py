import sys,requests,re,json,time,pickle,time,os
from math import ceil
from creds import pages #pages=[['domain','user','pass','token'], ['','','','']]
from colorama import Fore, init 
init(autoreset=True)
#init(autoreset=True,convert=True) #in windows??

#############################################
################ SETTINGS ###################
#############################################
ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
headers = {'User-Agent': ua}
proxy=False
if proxy:
    proxies = {'http': 'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
    verify=False
else:
    proxies = {}
    verify=True

#############################################
################## LOGIN ####################
#############################################
def api_login(page,usr,pwd): #returns token
    creds={'client_id':usr, 'client_secret': pwd}
    headers = {'User-Agent': ua}
    login=requests.post('https://'+page+'/webapi/rest/auth',data=creds,headers=headers,proxies=proxies,verify=verify).text
    if len(re.findall('access_token":"(.{40})"' ,login))>0:
        token=re.findall('access_token":"(.{40})"' ,login)[0]
        print(Fore.GREEN+'[+] Logged into: '+page)
        return token
    else:
        print(Fore.RED+'[!] Login error: ' + page)
        sys.exit(1)
 
#############################################
#### DOWNLOADING & PARSING PRODUCTS DATA ####
#############################################
def extract_data(text,availabilities,deliveries): #returns list [{'id':id,'name':name,...},...]
#Scraping data
    products=[]
    try:
        j=json.loads(text)
    except:
        print('[-] Error parsing JSON (extracting_data)')
        sys.exit(1)
    for item in j['items']: #for every 25 responses
        if 'error' in item['body']: #in case of timeouts
            print('[-] Error downloading products data:',item['body']['error'])
            sys.exit(1)
        for product in item['body']['list']: #for products in single response
            id=int(product['product_id'])
            name=product['translations']['pl_PL']['name']
            stock=product['stock']['stock']
            active=product['translations']['pl_PL']['active']
            price=product['stock']['price']
            delivery_id=product['stock']['delivery_id'] #DIFFERENT IDS ON PAGES
            availability_id=product['stock']['availability_id'] #DIFFERENT IDS ON PAGES
            is_set=False
            children=[]
            if 'children' in product.keys():
                is_set=True
                for child in product['children']:
                    children.append(int(child['product_id']))

            if availability_id==None:
                availability_name='null'
            else:
                availability_name=get_key(availabilities,availability_id)
            if delivery_id==None:
                delivery_name='null'
            else:
                delivery_name=get_key(deliveries,delivery_id)
            products.append({
                'id':id,
                'name':name,
                'stock':stock,
                'active':active,
                'price':price,
                'availability_name':availability_name,
                'delivery_name':delivery_name,
                'delivery_id':delivery_id,
                'availability_id':availability_id,
                'is_set':is_set,
                'children':children
                })
    return products

def api_get_products(page,token,availabilities,deliveries,active_only=False): #returns list of products [{'id':id,'name':name,...},...]
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    print(Fore.GREEN+'[+] Downloading product information from: '+ page)

    products_per_request = 50   #MAX 50 (https://developers.shoper.pl/developers/api/resources/products/list)
    requests_per_bulk = 25  #MAX 25 (https://developers.shoper.pl/developers/api/bulk)

    #Grabing info about pages
    try:
        j = json.loads(requests.get('https://'+page+'/webapi/rest/product-stocks?limit={}&page=99999'.format(products_per_request),headers=headers,proxies=proxies,verify=verify).text)
        count=j['count']
        pages=j['pages']
    except:
        print(Fore.RED+'[-] Error parsing JSON (pages info)')
        sys.exit(1)
   
    #Downloading products info
    requests_count=int(ceil(int(pages)/float(requests_per_bulk)))
    products=[]

    for i in range(requests_count):
        print('[i] {}\t{}/{}'.format(page,i+1,requests_count))
        request_body='['
        for j in range(requests_per_bulk):
            #downloading info about 25*50 products at once (25 requests in bulk, 50 products in one request
            page_number=requests_per_bulk*i+j
            if page_number != 0: #Page 0 returns the same results as page 1 
                if active_only: #filters={"translations.pl_PL.active":"1"}
                    request_body+='{"id": "products","path": "/webapi/rest/products","method": "GET","params": {"filters":{"translations.pl_PL.active":"1"},"limit": "'+str(products_per_request)+'","page": '+str(page_number)+'}},' #single response ~3,5MB, full product information
                else:
                    request_body+='{"id": "products","path": "/webapi/rest/products","method": "GET","params": {"limit": "'+str(products_per_request)+'","page": '+str(page_number)+'}},' #single response ~3,5MB, full product information
                #request_body+='{"id": "products","path": "/webapi/rest/product-stocks","method": "GET","params": {"limit": "50","page": ' + str(page_number) + '}},' #response ~840kB, doesn't contain names
        request_body=request_body.rstrip(',')
        request_body+=']'
        text = requests.post('https://'+page+'/webapi/rest/bulk',data=request_body,headers=headers,proxies=proxies,verify=verify).text
        products += extract_data(text,availabilities,deliveries)
    return products         

def create_name_dict(products,page): #creates product name dictionary {name:{'id':id,'stock':stock,'active':active},...} (Duplicated products are removed)
    dictionary={}
    duplicates=False
    for i in products:
        if i['name'] in dictionary:
            duplicates=True 
        else:
            dictionary[i['name']]=i
    if duplicates:
        print(Fore.YELLOW+'[!] Duplicates detected creating a dictionary - duplicates are skipped ({})'.format(page))
    print(Fore.GREEN+'[+] Dictionary created ({})'.format(page))
    return dictionary

def get_availabilities(page,token): #returns availabilities dictionary {name:id, ...}
    print(Fore.GREEN+'[+] Downloading availabilities information from: '+ page)
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    dictionary={'null':'null'} #availability_id can be null
    #try:    
    j = json.loads(requests.get('https://'+page+'/webapi/rest/availabilities',headers=headers,proxies=proxies,verify=verify).text)
    for availability in j['list']: 
        availability_id=availability['availability_id']
        name=availability['translations']['pl_PL']['name']
        dictionary[name]=availability_id
    return dictionary

def get_deliveries(page,token): #returns deliveries dictionary {name:id, ...}
    print(Fore.GREEN+'[+] Downloading deliveries information from: '+ page)
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    dictionary={'null':'null'} #delivery_id can be null
    #try:    
    j = json.loads(requests.get('https://'+page+'/webapi/rest/deliveries',headers=headers,proxies=proxies,verify=verify).text)
    for delivery in j['list']: 
        delivery_id=delivery['delivery_id']
        name=delivery['translations']['pl_PL']['name']
        dictionary[name]=delivery_id
    return dictionary

def get_key(dictionary,value): #returns key of given value in dictionary
    for key, val in dictionary.items(): 
        if  value == val:
            return key
    print(Fore.RED+'[-] Error: There is no value {} in dictionary {}'.format(value,dictionary))
    sys.exit(1)


def save_products(products,filename):
    if not os.path.isdir('data'):
        os.mkdir('data')
    pickle.dump(products, open('data/' + filename, 'wb'))
    print(Fore.GREEN+'[+] Products saved to file: ' + filename)

def load_products(filename):
    if not (os.path.isdir('data') and os.path.isfile('data/' + filename)):
        print(Fore.RED+'[-] Path data/' + filename+' doesn\'t exist')
        sys.exit(1)
    products = pickle.load(open('data/' + filename, 'rb'))
    print(Fore.GREEN+'[+] Products loaded from file: '+ filename)
    return products

def print_pretty_json(text):
    print(json.dumps(json.loads(text), indent=2))

def load_data(active_only=False,from_file=False):
    start = time.time()
    print(Fore.BLUE+'###################\nLOADING DATA\n###################')

    if not from_file:
        pages[0][3] = api_login(pages[0][0],pages[0][1],pages[0][2]) #TOKEN1
        pages[1][3] = api_login(pages[1][0],pages[1][1],pages[1][2]) #TOKEN2

        availabilities=[
                    get_availabilities(pages[0][0],pages[0][3]),
                    get_availabilities(pages[1][0],pages[1][3])
            ]
        deliveries=[
                    get_deliveries(pages[0][0],pages[0][3]),
                    get_deliveries(pages[1][0],pages[1][3])
            ]
        products=[
                    api_get_products(pages[0][0],pages[0][3],availabilities[0],deliveries[0],active_only),
                    api_get_products(pages[1][0],pages[1][3],availabilities[1],deliveries[1],active_only)  
                 ]

        #SAVING TO FILE
        save_products((products[0],availabilities[0],deliveries[0]),pages[0][0])
        save_products((products[1],availabilities[1],deliveries[1]),pages[1][0])
    else:
        #LOADING PRODUCTS FROM FILE
        products1,availabilities1,deliveries1 = load_products(pages[0][0])
        products2,availabilities2,deliveries2 = load_products(pages[1][0])
        products=[products1,products2]
        availabilities=[availabilities1,availabilities2]
        deliveries=[deliveries1,deliveries2]
        pages[0][3] = api_login(pages[0][0],pages[0][1],pages[0][2]) #TOKEN1
        pages[1][3] = api_login(pages[1][0],pages[1][1],pages[1][2]) #TOKEN2

    name_dict1 = create_name_dict(products[0],pages[0][0]) #creating dictionary without duplicates, name oriented
    name_dict2 = create_name_dict(products[1],pages[1][0]) #creating dictionary without duplicates, name oriented
    print('###################\nData loaded in {} seconds.'.format(round(time.time()-start,3)))
    return (products,availabilities,deliveries,name_dict1,name_dict2)

#############################################
############ COMPARING PRODUCTS #############
#############################################
def find_duplicates(products,page,print_duplicates=True): #prints duplicates in list of products
    count={} #{'name1':3,...} dictionary with occurences
    duplicates=False
    for i in products:
        if i['name'] in count:
            count[i['name']]+=1
            duplicates = True
        else:
            count[i['name']]=1
    if duplicates:
        if print_duplicates:
            print(Fore.YELLOW+'[-] Duplicates in {}:'.format(page))
            for name in count:
                if count[name]>1:
                    print(count[name],name)
        return False
    else:
        if print_duplicates:
            print(Fore.GREEN+'[+] No duplicates found in',page)
        return True

def compare_product_quantities(products1,products2,page1,page2,print_diff=True):
    if print_diff:
        print('[i] Products in',page1+':',len(products1))
        print('[i] Products in',page2+':',len(products2))
    if len(products1)!=len(products2):
        return False
    else:
        return True

def compare_dictionary_names(dictionary1,dictionary2,page1,page2,dictionary_content,print_diff=True): #compare product names in dictionaries
    set1=set(dictionary1.keys())
    set2=set(dictionary2.keys())
    
    diff1=set1-set2
    diff2=set2-set1
    
    if len(diff1)>0 or len(diff2)>0:
        if print_diff:
            print(Fore.RED+'[-] Unique {} in {} ({}):'.format(dictionary_content,page1,len(diff1)))
            for i in diff1:
                print('{}(hex:{})'.format(i,i.encode('utf-8').hex()))

            print(Fore.RED+'[-] Unique {} in {} ({}):'.format(dictionary_content, page2,len(diff2)))
            for i in diff2:
                print('{}(hex:{})'.format(i,i.encode('utf-8').hex()))
        return False
    else:
        return True

def diff(name_dict1,name_dict2,attribute,common_only=False,verbose=True): #returns differences of given attribute [[product_name,value1,value2,id1,id2], ...]
    diffs=[]
    for name in name_dict1.keys():
        if name in name_dict2: #if product exists in both
            if name_dict1[name][attribute] != name_dict2[name][attribute]:#if attributes are different
                diffs.append([name,name_dict1[name][attribute],name_dict2[name][attribute],name_dict1[name]['id'],name_dict2[name]['id']])
        else: #if product exists only in name_dict1
            if not common_only:
                diffs.append([name,name_dict1[name][attribute],'NULL',name_dict1[name]['id'],'NULL'])
    if not common_only:
        for name in name_dict2.keys():
            if name not in name_dict1: #if product exists only in name_dict2
                diffs.append([name,'NULL',name_dict2[name][attribute],'NULL',name_dict2[name]['id']])
    if len(diffs)>0:
        if verbose:
            print(Fore.RED+'[-] There are {} attribute diffs'.format(attribute))
            for d in diffs:
                print('Not equal {}: {} != {} ({})'.format(attribute,d[1],d[2],d[0]))
    else:
        if verbose:
            print(Fore.GREEN+'[+] There are no {} attribute diffs'.format(attribute))
    return diffs

def compare_products(products1,products2,name_dict1,name_dict2,page1,page2,availabilities1,availabilities2,deliveries1,deliveries2,attributes,verbose,print_details):
    tests=[]
    tests.append(['Equal product quantities:',compare_product_quantities(products1,products2,page1,page2,print_details)])
    tests.append(['Equal product names:',compare_dictionary_names(name_dict1,name_dict2,page1,page2,'products',print_details)])
    tests.append(['Equal product availabilities:',compare_dictionary_names(availabilities1,availabilities2,page1,page2,'availabilities',print_details)])
    tests.append(['Equal product deliveries:',compare_dictionary_names(availabilities1,availabilities2,page1,page2,'deliveries',print_details)])
    tests.append(['Equal sets of products:',compare_sets(name_dict1,name_dict2,print_details)])
    tests.append(['No product duplicates in '+page1+':',find_duplicates(products1,page1,print_details)])
    tests.append(['No product duplicates in '+page2+':',find_duplicates(products2,page2,print_details)])


    for attribute in attributes:    
            tests.append(['Values of ' +attribute+ ' attribute: ',not bool(diff(name_dict1,name_dict2,attribute,False,print_details))])
    
    if verbose:
        for i in tests:
            if i[1]:
                print(Fore.GREEN+i[0]+'\t\t'+str(i[1]))
            else:
                print(Fore.RED+i[0]+'\t\t'+str(i[1]))
        same=all([i[1] for i in tests])
        if same:
            print(Fore.GREEN+'EQUAL DATABASES:\t\t'+str(same))
        else:
            print(Fore.RED+'EQUAL DATABASES:\t\t'+str(same))
    return all([i[1] for i in tests]) #if all tests are True 

def compare_sets(name_dict1,name_dict2,verbose=True):
    equal = True
    for product in name_dict1:
        if name_dict1[product]['is_set']:
            if not compare_lists(name_dict1[product]['children'],name_dict2[product]['children']):
                equal=False
                if verbose:
                    print('Not equal set:',product)
    return equal

def compare_lists(list1,list2):
    return sorted(list1) == sorted(list2)

#############################################
############# UPDATING PRODUCTS #############
#############################################
def update_value(page,token,id,field,value):
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    
    fields={
            'stock':'{"stock":{"stock":'+str(value)+'}}',
            'active':'{"translations": {"pl_PL": {"active": "'+str(value)+'"}}}',
            'price':'{"stock":{"price":'+str(value)+'}}',
            'delivery_id':'{"stock":{"delivery_id":'+str(value)+'}}',
            'availability_id':'{"stock":{"availability_id":'+str(value)+'}}',
            }
    text=''
    for i in range(3):
        r = requests.put('https://'+page+'/webapi/rest/products/'+str(id),data=fields[field],headers=headers,proxies=proxies,verify=verify)
        if r.status_code == 200:
            text=r.text
            break
        else:
            print(Fore.YELLOW +'|Retrying {}|'.format(i),end='')
            time.sleep(1)
    if text == '1':
        return True
    else:
        return False

def copy_attribute(page1,page2,name_dict1,name_dict2,attribute,print_only=True,id_dict=None): #copies active statuses from page1 to page2
    diffs = diff(name_dict1,name_dict2,attribute,True) 
    i=0
    if len(diffs)>0:
        for d in diffs:  # d = [product_name,value1,value2,id1,id2]
            i+=1
            if attribute not in ['availability_name','delivery_name']:
                print('[i] {}/{} Changing product {} in {} {} attribute: {}->{}\t({})'.format(i,len(diffs),d[4],page2[0],attribute,d[2],d[1],d[0]),end='')
            else:   #['availability_name','delivery_name']
                id1=name_dict2[d[0]][attribute.split('_')[0]+'_id'] #name_dict2['product_name']['delivery_id']  
                id2=id_dict[d[1]]
                print('[i] {}/{} Changing product {} in {} {} attribute: {}->{} (ID:{}->ID:{})\t({})'.format(i,len(diffs),d[4],page2[0],attribute,d[2],d[1],id1,id2,d[0]),end='')
            if print_only:
                print('') #newline
            else:
                if attribute not in ['availability_name','delivery_name']:
                    updated = update_value(page2[0],page2[3],d[4],attribute,d[1]) #page,token,id,field,value 
                else: #['availability_name','delivery_name']
                    updated = update_value(page2[0],page2[3],d[4],attribute.split('_')[0]+'_id',id_dict[d[1]]) #page,token,id,field,value                            
                if  updated: 
                    print(Fore.GREEN + ' DONE')
                else:
                    if name_dict2[d[0]]['is_set']:
                        print(Fore.RED + ' (IS SET, UPDATE PRODUCTS IN SET FIRST)',end='')
                    print(Fore.RED + ' ERROR')
    return len(diffs)