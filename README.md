# Skrypty synchronizujące bazy produktów na platformie shoper.pl
Skrypty ułatwiają zarządzanie produktami (porównywanie, kopiowanie atrybutów, synchronizowanie stanów magazynowych) w dwóch sklepach stworzonych na platformie shoper.pl.  
Działa na zarówno na systemach Windows i Linux.

## Instalacja
1. Zainstaluj Python 3 (https://www.python.org/downloads/)
2. Ściągnij repozytorium (komenda 'git clone https://github.com/r4wr4m/shoper_sync.git' lub ściągając plik [zip_file](https://github.com/r4wr4m/shoper_sync/archive/master.zip "repo"))
3. Zainstaluj zależności (komenda python -m pip install -r requirements.txt)
4. Uzupełnij informacje o sklepach w pliku creds.py
5. (Opcjonalnie) Zainstaluj poprawkę biblioteki InvoiceGenerator, umożliwiającej generowanie faktur w języku polskim (python3 install_polish_invoice.py)

## Wykorzystanie

### Uruchomienie interaktywnego menu 
Skrypt ułatwia korzystanie z poszczególnych funkcji

```python menu.py```


### Porównywanie produktów
Skrypt porównuje informacje o produktach w dwóch sklepach (ilości, nazwy, dostepności, dostawy, zestawy produktów, duplikaty nazw produktów, atrybuty: active, stock, price, availability, delivery).

```python compare.py [options]```

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* details - wyświetl różnice
* active - ściągaj informacje tylko o aktywnych produktach
* sets - wyświetl zestawy produktów

### Kopiowanie informacji o produktach z jednego sklepu do drugiego
Skrypty kopiują informacje o produktach z pierwszego zdefiniowanego sklepu do drugiego (domyślnie tylko wyświetla możliwe zmiany). 

```python copy_attributes.py [options]```

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach
* change - wprowadzaj zmiany (bez tej opcji skrypt tylko wyświetla możliwe zmiany)

### Synchronizowanie stanów magazynowych między dwoma sklepami
Skrypt sprawdza, czy produkty są takie same w obu bazach i w przypadku zgodności - zapisuje informację o produktach do pliku (data/past_data). 
Przy kolejnych uruchomieniach skryptu, jeżeli plik past_data istnieje, skrypt pobiera informację o stanach magazynowych z obu sklepów, porównuje je ze stanem zapisanym wcześniej i w przypadku wystąpienia różnic - synchronizuje (domyślnie tylko wyświetla możliwe zmiany).

```python sync_stock.py [options]```

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach
* change - wprowadzaj zmiany (bez tej opcji skrypt tylko wyświetla możliwe zmiany)
* delete - usuń informację zapisane wcześniej informacje o produktach

### Generowanie faktury
Skrypt generuje fakturę na podstawie podanego numeru zamówienia. Przed generowaniem faktury, należy wprowadzić dane sprzedawcy w pliku invoice.py.

```python invoice.py domena numer_zamówienia numer_faktury nazwa_pliku```

domena - np. google.pl

### Zapisywanie nazw produktów do pliku
Skrypt zapisuje nazwy produktów do pliku products.xls.
Nazwy zapisywane są w pierwszej kolumnie.

```python products2file.py [offline [active]]```

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach

### Zapisywanie zamówionych produktów (z paszportami roślin) do pliku
Skrypt zapisuje nazwę zamawiającego, zamówione produkty oraz paszporty roślin do pliku xls.

```python orders2file.py domena data_od data_do nazwa_pliku [offline] [active]```

domena - np. google.pl

data_od, data_do - data w formacie yyyy-MM-dd HH:mm:ss (przykłady: "2020-09-11 12:00:00", "2020-09-11 12", 2020-09-11, 2020-09, 2020)

nazwa_pliku - nazwa pliku, do którego zostaną zapisane dane

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach

### Zapisywanie w sklepie paszportów roślin z pliku
Skrypt zapisuje w wybranym sklepie paszporty roślin wczytane z pliku products.xls. 
W pierwszej kolumnie powinny zostać wpisane nazwy produktów, w drugiej paszporty do przypisania.

```python set_passports.py domena [offline] [active] [change]```

domena - np. google.pl

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach
* change - wprowadzaj zmiany (bez tej opcji skrypt tylko wyświetla możliwe zmiany)

### Kopiowanie stanów produktów z wybranego sklepu na konto Allegro
Skrypt kopiuje stany produktów z wybranego sklepu na konto Allegro.

```python copy_auction_stocks.py domena [offline] [change]```

domena - np. google.pl

Dostępne opcje:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* change - wprowadzaj zmiany (bez tej opcji skrypt tylko wyświetla możliwe zmiany)

### Logowanie do Allegro
Skrypt wykorzystuje client_id oraz client_secret zarejestrowanej w Allegro aplikacji (https://apps.developer.allegro.pl) do wygenerowania kodu urządzenia. Uwierzytelniony użytkownik Allegro musi zezwolić urządzeniu na dostęp do konta (wykorzystując link wygenerowany przez skrypt). Po udzieleniu dostępu, skrypt pobiera token umożliwiający zarządzanie produktami w Allegro i zapisuje go do pliku. Token jest ważny 12h, w przypadku jego unieważnienia jest odświeżany przez dowolny skrypt korzystający z tokena (token odświeżający ma ważność 3 miesiące od ostatniego odświeżenia).

```python login_allegro.py domena```

domena - np. google.pl


