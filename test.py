from functions import *
start = time.time()

def test(page):
    print(Fore.BLUE+'###################\nTEST\n###################')
    token = api_login(page[0],page[1],page[2])
    headers = {'User-Agent': ua,'Authorization':'Bearer '+token}
    #print('[+] Downloading product information from: '+ page)
    #print_pretty_json(requests.get('https://'+page+'/webapi/rest/products?limit=1&page=1&filters={"product_id":7169,"translations": {"pl_PL": {"active": "1"}}}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/products?filters={"product_id":3038}',headers=headers,proxies=proxies,verify=verify).text)
    #j=json.loads(requests.get('https://'+page[0]+'/webapi/rest/products?filters={"product_id":3038}',headers=headers,proxies=proxies,verify=verify).text)
    #print(j['list'][0])
    #print(requests.get('https://'+page+'/webapi/rest/product-stocks?limit=1&page=1',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/products?limit=1&page=1&filters={"product_id":7019}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/shippings',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/attributes?filters={"name":"kod"}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/availabilities',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/deliveries',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/auctions?filters={"title":"Czosnek Ozdobny błękitny Caeruleum (5szt.)"}',headers=headers,proxies=proxies,verify=verify).text)
    #print_pretty_json(requests.get('https://'+page[0]+'/webapi/rest/auctions/2',headers=headers,proxies=proxies,verify=verify).text)
    #data = '{"real_auction_id": "9619741059","auction_house_id": "1"    ,"sales_format": "1","title": "Czosnek Ozdobny b\u0142\u0119kitny Caeruleum (5szt.)","product_id": "7042","quantity":14}'
    #print_pretty_json(requests.put('https://'+page[0]+'/webapi/rest/auctions/',data=data.encode('utf-8'),headers=headers,proxies=proxies,verify=verify).text)
    #print(get_availabilities(page,token))
    #print(get_deliveries(page,token))
    
    #UPDATES    
    #update_value(pages[1][0],pages[1][3],7169,'stock',13)
    #update_value(pages[1][0],pages[1][3],7169,'active',0)
    #update_value(pages[1][0],pages[1][3],7169,'availability_id',6)
    #update_value(pages[1][0],pages[1][3],7169,'delivery_id',8)
    #update_value(pages[1][0],pages[1][3],7169,'price',8)
    #a = get_auctions(page[0],token)
    #for i in a:
    #    print(i)
    #print(len(a))

#products,availabilities,deliveries,name_dict1,name_dict2 = load_data(from_file=False) #load_data(active_only=False,from_file=False)

#test(pages[0])
products,availabilities,deliveries,name_dict1,name_dict2,auctions = load_data(True,False) #load_data(active_only=False,from_file=False)
#auctions = get_auctions(pages[0][0],pages[0][3])
#print(auctions[0][0]['real_auction_id'])
a = allegro_set_stock(pages[0],'9545005146',0,3)
#print_pretty_json(a)
#allegro_api_login(pages[1])
#allegro_refresh_token(pages[0])

#write2file(changes_filename(),'TEST')
#write2file(changes_filename(),'TEST2')
'''

import smtplib

mail_creds=['','']
to = ['']



def send_mail(mail_creds,to,text):
    sent_from = mail_creds[0]
    subject = 'POWIADOMIENIE ZE SKRYPTU SHOPERUJACEGO'
    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}\n'.format(mail_creds[0], ", ".join(to), subject, text)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mail_creds[0],mail_creds[1])
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        print('Email not sent: ' + str(e))
send_mail(mail_creds,to,'TEST')



token = api_login(pages[1][0],pages[1][1],pages[1][2])
ordered_products = get_ordered_products(pages[1][0],token,9299)
order_info = get_order_info(pages[1][0],token,9299)
for i in order_info:
    print(i, order_info[i])

print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))
'''
