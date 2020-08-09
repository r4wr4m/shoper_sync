# Shoper synchronization script
Script description

## Installation
1. Install Python 3 
2. Download repository
3. Install requirements (python -m pip install -r requirements.txt)
4. Provide shops information in creds.py

## Usage

### Comparing product information
Script compares product information in two shops (quantities, names, availabilities, deliveries, sets of products, product duplicated names, attributes: active, stock, price, availability, delivery).
> ```python compare.py [options]```

Available options:
* offline - read product information from file (product information file is saved automatically)
* details - print differences
* active - download active products information only
* sets - print information about sets of products

### Copying product information from one shop to the other
```python copy_attributes.py [options]```

Available options:
* offline - read product information from file (product information file is saved automatically)
* active - download active products information only
* change - make the changes (script prints possible changes by default)

### Synchronizing stock information between shops

> python sync_stock.py [options]

Available options:
* offline - read product information from file (product information file is saved automatically)
* active - download active products information only
* change - make the changes (script prints possible changes by default)
* delete - delete past product information
