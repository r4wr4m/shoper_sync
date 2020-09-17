import os,sys,subprocess

#Python 3 detection
pythoncmd=''
for cmd in ['python3','python']:
    try:
        p = subprocess.Popen([cmd, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        outerr=(out+err).decode("utf-8") 
        if outerr[:6]=='Python':
            if outerr[7]=='3':
                pythoncmd = cmd
    except:
        pass
if pythoncmd=='':
    print('Python 3 not found!')
    sys.exit(1)

def get_args(options): # [('arg1','description'), ... ]
    args = ''
    offline=False
    for option in options:
        if option[0] != "active" or (option[0] == "active" and not offline):
            a=''
            while a=='':
                while a not in ['t','n']:
                    a = input(option[1]+ ' (t/n)\n=>')
                    if a not in ['t','n']:
                        print('Nie ma takiej opcji')
            if a=='t' and option[0]=='offline':
                offline = True
            if a=='t' and option[0]=='change': #Sure? 
                b = ''
                while b not in ['t','n']:
                    b = input('Czy NA PEWNO wprowadzać zmiany?? (t/n)\n=>')
                    if b not in ['t','n']:
                        print('Nie ma takiej opcji')
                if b == 'n':
                    a = 'n'
            if a=='t':
                args += " " + option[0]

    return args

while True:
    print("=======================================")
    print('Co chcesz zrobić?')
    print("=======================================")
    print('1. Porównać stany na dwóch sklepach')
    print('2. Skopiować informacje o produktach z jednego sklepu do drugiego')
    print('3. Uruchomić synchronizację produktów')
    print('4. Wygenerować fakturę')
    print('5. Zainstalować język polski w generowanych fakturach')
    print('6. Zapisać nazwy produktów do pliku')
    print('7. Zapisać zamówione produkty (z paszportami roślin) do pliku')
    print('8. Zapisać w sklepie paszporty roślin z pliku')
    print('9. Skopiować stany ze sklepu do Allegro')
    print('10. Zalogować do Allegro')
    print('11. Usunąć zapisane w przeszłości dane (dane są potrzebne do synchronizacji)')
    print('0. Nic')
    choice = input('=>')
    if choice not in ['1','2','3','4','5','6','7','8','9','10','11','0']:
        print('Nie ma takiej opcji')
        continue
    print("=======================================")
    cmd = pythoncmd
    if choice == '1':
        cmd += ' compare.py'
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?'),
            ('details','Czy wyświetlać różnice między sklepami?'),
            ('sets','Czy wyświetlać informacje o zestawach?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '2':
        cmd += ' copy_attributes.py'
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?'),
            ('change','Czy wprowadzać zmiany w sklepach?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '3':
        cmd += ' sync_stock.py'
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?'),
            ('change','Czy wprowadzać zmiany w sklepach?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '4':
        cmd += ' invoice.py ' # domena numer_zamówienia numer_faktury nazwa_pliku
        domain = input('Podaj domenę sklepu (np. google.com)\n=>')
        order_id = input('Podaj numer zamówienia\n=>')
        invoice_id = input('Podaj numer faktury\n=>')
        file = input('Podaj nazwę pliku, do którego zostanie zapisana faktura\n(bez rozszerzenia pliku)\n=>')
        print("=======================================")
        print(cmd + domain + ' ' + order_id + ' ' + invoice_id + ' ' + file + '.pdf')
        os.system(cmd + domain + ' ' + order_id + ' ' + invoice_id + ' ' + file + '.pdf')    
    if choice == '5':
        cmd += ' install_polish_invoice.py'
        print("=======================================")
        print(cmd)
        os.system(cmd)   
    if choice == '6':
        cmd += ' products2file.py' #python products2file.py [offline [active]]
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '7': #python orders2file.py domena data_od data_do nazwa_pliku [offline] [active]
        cmd += ' orders2file.py'
        domain = input('Podaj domenę sklepu (np. google.com)\n=>')
        date_from = input('Zamówienia od - podaj datę (np. "2020-09-11 12:00:00", "2020-09-11 12", 2020-09-11, 2020-09)\n=>')
        date_to = input('Zamówienia do - podaj datę (np. "2020-09-11 12:00:00", "2020-09-11 12", 2020-09-11, 2020-09)\n=>')
        filename = input('Podaj nazwę pliku\n=>')
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku? (wczytanie danych jest niezbędne do zapisania informacji o paszportach)'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?')])
        print("=======================================")
        print(cmd+ ' ' + domain + ' ' + date_from + ' ' + date_to + ' ' + filename + args)
        os.system(cmd+ ' ' + domain + ' ' + date_from + ' ' + date_to + ' ' + filename + args)
    if choice == '8':
        cmd += ' set_passports.py' #python set_passports.py domena [offline] [active] [change]
        domain = input('Podaj domenę sklepu (np. google.com)\n=>')
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?'),
            ('change','Czy wprowadzać zmiany w sklepie?')])
        print("=======================================")
        print(cmd + ' ' + domain + args)
        os.system(cmd + ' ' + domain + args)
    if choice == '9':
        cmd += ' copy_auction_stocks.py' #python copy_auction_stocks.py domena [offline] [change]
        domain = input('Podaj domenę sklepu (np. google.com)\n=>')
        args = get_args([
            ('offline','Czy wczytać dane o produktach z pliku?'),
            ('change','Czy wprowadzać zmiany w sklepie?')])
        print("=======================================")
        print(cmd + ' ' + domain + args)
        os.system(cmd + ' ' + domain + args)
    if choice == '10':
        cmd += ' login_allegro.py' #python copy_auction_stocks.py domena [offline] [change]
        domain = input('Podaj domenę sklepu (np. google.com)\n=>')
        print("=======================================")
        print(cmd + ' ' + domain)
        os.system(cmd + ' ' + domain)
    if choice == '11':
        b = ''
        while b not in ['t','n']:
            b = input('Czy NA PEWNO usunąć dane z przeszłości?? (t/n)\n(dane są potrzebne do synchonizacji)\n=>')
            if b not in ['t','n']:
                print('Nie ma takiej opcji')
        if b=='t':
            print("=======================================")
            print(cmd + ' sync_stock.py delete')
            os.system(cmd + ' sync_stock.py delete')    
    if choice == '0':
        print("Kończę pracę")
        break
