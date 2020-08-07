from functions import *
start = time.time()

def test(page):
    print(Fore.BLUE+'###################\nTEST\n###################')
    token = api_login(page[0],page[1],page[2])
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    #print('[+] Downloading product information from: '+ page)
    #print_pretty_json(requests.get('https://'+page+'/webapi/rest/products?limit=1&page=1&filters={"product_id":7169,"translations": {"pl_PL": {"active": "1"}}}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/products?filters={"product_id":6979}',headers=headers,proxies=proxies,verify=verify).text)
    #j=json.loads(requests.get('https://'+page[0]+'/webapi/rest/products?filters={"product_id":6979}',headers=headers,proxies=proxies,verify=verify).text)
    #print(j['list'][0])
    #print(requests.get('https://'+page+'/webapi/rest/product-stocks?limit=1&page=1',headers=headers,proxies=proxies,verify=verify).text)
    print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/products?limit=1&page=1&filters={"product_id":7019}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/availabilities',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/deliveries',headers=headers,proxies=proxies,verify=verify).text)
    #print(get_availabilities(page,token))
    #print(get_deliveries(page,token))
    
    #UPDATES    
    #update_value(pages[1][0],pages[1][3],7169,'stock',13)
    #update_value(pages[1][0],pages[1][3],7169,'active',0)
    #update_value(pages[1][0],pages[1][3],7169,'availability_id',6)
    #update_value(pages[1][0],pages[1][3],7169,'delivery_id',8)
    #update_value(pages[1][0],pages[1][3],7169,'price',8)

#products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file=False) #load_data(active_only=False,from_file=False)

test(pages[1])

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
