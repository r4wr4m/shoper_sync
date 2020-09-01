from functions import *
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator, Address
from InvoiceGenerator.pdf import SimpleInvoice
from decimal import Decimal
import datetime

if len(sys.argv)==5:
    domain=sys.argv[1]
    order_number=sys.argv[2]
    invoice_number=sys.argv[3]
    filename=sys.argv[4]
else:
    print(Fore.RED+'[i] Usage:\n\t{} domain order_number invoice_number filename'.format(sys.argv[0]))
    sys.exit(0)


start = time.time()

os.environ["INVOICE_LANG"] = "pl"

provider = Provider('My company', 
    address='test address',
    city='Testcity', 
    zip_code='00-000',
    phone='123-456-789',
    email='test@email.test',
    bank_name='TestBank', 
    bank_account='01234567890123456789012345',
    bank_code='PL',
    note='TestNote\nTestNote', 
    logo_filename='/home/user/Downloads/logo.png',
    vat_note='TestVatNote')
creator = Creator('John Doe', stamp_filename='')

page=None
for p in pages:
    if domain == p[0]:
        page=p
if not page:
    print(Fore.RED+'[!] Page {} not found!'.format(domain))
    sys.exit(1)

token = api_login(page[0],page[1],page[2])
ordered_products = get_ordered_products(page[0],token,order_number)
order_info = get_order_info(page[0],token,order_number)
print(Fore.GREEN+'[+] Order {} info downloaded from {}'.format(order_number,page[0]))

clientname=''
if order_info['billing_address']['company'] != '':
    clientname = order_info['billing_address']['company']
if order_info['billing_address']['firstname'] !='':
    if clientname != '':
        clientname += '\n'
    clientname +=order_info['billing_address']['firstname'] + ' ' + order_info['billing_address']['lastname']

client = Client(clientname, 
    address=order_info['billing_address']['street1']+'\n'+order_info['billing_address']['street2'], 
    city=order_info['billing_address']['city'], 
    zip_code=order_info['billing_address']['postcode'],
    phone=order_info['billing_address']['phone'],
    email=order_info['email'], 
    bank_name='TestBank', 
    bank_account='TestBankAccount', 
    bank_code='PL',
    note='TestNote\nTestNote', 
    #vat_id='TestVatId', 
    #ir='TestOrderInfo',
    logo_filename='', 
    vat_note='TestVatNote')

clientname=''
client = Client(clientname, 
    address='ulica testowa 32', 
    city='testowo', 
    zip_code='00-000',
    phone='123-456-789',
    email='testowo@testowo.testowo', 
    bank_name='TestBank', 
    bank_account='TestBankAccount', 
    bank_code='PL',
    note='TestNote\nTestNote', 
    #vat_id='TestVatId', 
    #ir='TestOrderInfo',
    logo_filename='', 
    vat_note='TestVatNote')


invoice = Invoice(client, provider, creator)
invoice.currency = 'zł'
invoice.currency_locale = 'pl_PL.UTF-8'
invoice.number = invoice_number
invoice.date = datetime.datetime.now()
for product in ordered_products:
    invoice.add_item(Item(product['quantity'], product['price'], description=product['name'], unit=product['unit'], tax=Decimal(product['tax_value'])))
invoice.add_item(Item(1, order_info['shipping_cost'], description='Dostawa ({})'.format(order_info['shipping_name']), unit='', tax=Decimal(order_info['shipping_tax_value'])))


pdf = SimpleInvoice(invoice)
pdf.gen(filename, generate_qr_code=False)
print(Fore.GREEN+'[+] Invoice generated into file: {}'.format(filename))


print('###################\nDone in {} seconds.'.format(round(time.time()-start,3)))