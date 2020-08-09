# Shoper synchronization scripts
Scripts allow to manage (comparing, copying product attributes, synchronizing) product information in two shops created in shoper.pl platform.  

## Installation
1. Install Python 3 
2. Download repository
3. Install requirements (python -m pip install -r requirements.txt)
4. Provide shops information in creds.py

## Usage

### Comparing product information
Script compares product information in two shops (quantities, names, availabilities, deliveries, sets of products, product duplicated names, attributes: active, stock, price, availability, delivery).

```python compare.py [options]```

Available options:
* offline - read product information from file (product information file is saved automatically)
* details - print differences
* active - download active products information only
* sets - print information about sets of products

### Copying product information from one shop to the other
Scripts copies product attributes from the first defined shop to the other (prints possible changes by default).  

```python copy_attributes.py [options]```

Available options:
* offline - read product information from file (product information file is saved automatically)
* active - download active products information only
* change - make the changes (script prints possible changes by default)

### Synchronizing stock information between shops
Script checks if product information is synchronized, saves synchornized information to file (data/past_data). 
If the file past_data exists, script loads information from both shops, compares product stocks with past data, and synchronizes stocks (prints possible changes by default).

```python sync_stock.py [options]```

Available options:
* offline - read product information from file (product information file is saved automatically)
* active - download active products information only
* change - make the changes (script prints possible changes by default)
* delete - delete past product information
