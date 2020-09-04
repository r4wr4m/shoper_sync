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
    for option in options:
        a=''
        while a=='':
            while a not in ['t','n']:
                a = input(option[1]+ ' (t/n)\n=>')
                if a not in ['t','n']:
                    print('Nie ma takiej opcji')
        if a=='t' and option[0]=='change':
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
    print('5. Usunąć zapisane w przeszłości dane (dane są potrzebne do synchronizacji)')
    print('6. Nic')
    choice = input('=>')
    if choice not in ['1','2','3','4','5']:
        print('Nie ma takiej opcji')
        continue
    print("=======================================")
    cmd = pythoncmd
    if choice == '1':
        cmd += ' compare.py'
        args = get_args([
            ('offline','Czy wczytać dane z pliku?'),
            ('active','Czy brać pod uwagę tylko aktywne produkty?'),
            ('details','Czy wyświetlać różnice między sklepami?'),
            ('sets','Czy wyświetlać informacje o zestawach?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '2':
        cmd += ' copy_attributes.py'
        args = get_args([
            ('offline','Czy wczytać dane z pliku?'),
             ('active','Czy brać pod uwagę tylko aktywne produkty?'),
             ('change','Czy wprowadzać zmiany w sklepach?')])
        print("=======================================")
        print(cmd+args)
        os.system(cmd+args)
    if choice == '3':
        cmd += ' sync_stock.py'
        args = get_args([
            ('offline','Czy wczytać dane z pliku?'),
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
        b = ''
        while b not in ['t','n']:
            b = input('Czy NA PEWNO usunąć dane z przeszłości?? (t/n)\n(dane są potrzebne do synchonizacji)\n=>')
            if b not in ['t','n']:
                print('Nie ma takiej opcji')
        if b=='t':
            print("=======================================")
            print(cmd + ' sync_stock.py delete')
            os.system(cmd + ' sync_stock.py delete')    
    if choice == '6':
        print("Kończę pracę")
        break
