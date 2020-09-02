import os,sys,shutil
for path in sys.path:
	if os.path.isdir(path+'/InvoiceGenerator/'):
		shutil.copyfile('./pdf.py',path+'/InvoiceGenerator/pdf.py')
		print("Polish language installed")
		sys.exit(1)
print('Directory InvoiceGenerator doesn\'t exist!')
print('Try to install InvoiceGenerator library (python3 -m pip install InvoiceGenerator)')
