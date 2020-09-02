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

Available options:
* offline - załaduj informacje o produktach z pliku (pliki zapisywane są automatycznie)
* active - ściągaj informacje tylko o aktywnych produktach
* change - wprowadzaj zmiany (bez tej opcji skrypt tylko wyświetla możliwe zmiany)
* delete - usuń informację zapisane wcześniej informacje o produktach

### Generowanie faktury
Skrypt generuje fakturę na podstawie podanego numeru zamówienia. Przed generowaniem faktury, należy wprowadzić dane sprzedawcy w pliku invoice.py.

```python invoice.py domena numer_zamówienia numer_faktury nazwa_pliku```

domena - np. google.pl
