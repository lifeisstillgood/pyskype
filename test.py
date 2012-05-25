import pyskype

p = pyskype.pySkype()
p.start()
print p.invoke('GET USERSTATUS')

p.close()
